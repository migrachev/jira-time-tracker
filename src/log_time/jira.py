import subprocess
import platform
import requests
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from requests.auth import HTTPBasicAuth
from prompt_toolkit import prompt
from datetime import date
from threading import Event
from subprocess import CompletedProcess
from requests import Response
from mytypes import UserData, WorkLog, WorkLogRequest
from utils import start_spinner_thread

def log_time(user_data: UserData, jira_host_name: str) -> bool:
    loading_reachable_check_event: Event = Event()
    start_spinner_thread(loading_reachable_check_event)
    if not is_reachable(jira_host_name):
        print("\033[31m\rJIRA instalation unreachable! Check your VPN status and/or connectivity!\033[0m")
        return False
    else:
        print("\r                                                      ")
        loading_reachable_check_event.set()
        while True:
            username: str = prompt("We will need your JIRA username: ")
            password: str = prompt("We will need your JIRA password: ", is_password=True)
            auth: HTTPBasicAuth = HTTPBasicAuth(username, password)
            loading_credentials_check_event: Event = Event()
            start_spinner_thread(loading_credentials_check_event)
            if is_valid_authentication(auth, jira_host_name):
                break
            else:
                print("\033[31m\rIncorrect credentials!\033[0m")
            loading_credentials_check_event.set()

        print("\r                                                      ")
        requests: list[WorkLogRequest] = []
        day_tuple: tuple[int, int, int]; logs_tuple: tuple[str, str, str]
        for day_tuple, logs_tuple in user_data.items():
            day: date = date(*day_tuple)
            time: str; comment: str; issue: str
            for time, comment, issue in logs_tuple:
                started: str = f"{day.isoformat()}T10:00:00.000+0000"
                time_spent_hours: float = float(time[:-1])
                time_spent_seconds: float = time_spent_hours * 60 * 60
                print(f"About to log \033[32m{time}\033[0m hours for \033[32m{day}\033[0m in issue \033[32m{issue}\033[0m with comment \033[32m{comment}\033[0m")
                request: WorkLogRequest = {
                    "url": f"https://{jira_host_name}:443/rest/api/2/issue/{issue}/worklog",
                    "body": {
                        "started": started,
                        "comment": comment,
                        "timeSpentSeconds": time_spent_seconds
                    }
                }
                requests.append(request)
        print("\033[33m=============================================================================================================================================\033[0m")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures: dict[Future[bool], str] = {}
            for request in requests:
                request: WorkLogRequest
                url: str = request["url"]
                body: WorkLog = request["body"]
                future: Future[bool] = executor.submit(add_worklog, url, body, auth)
                futures[future] = url

            for future in as_completed(futures):
                url: str = futures[future]
                try:
                    is_successful: bool = future.result()
                    if is_successful:
                        print(f"\033[32mSuccessfully logged time @{url}\033[0m")
                    else:
                        print(f"\033[33mFiled to log time @{url}\033[0m")
                except:
                    print(f"\033[31mUnhandled exception during adding time log @{url}\033[0m")
        return True
    
def is_reachable(hostname: str) -> bool:
    # Define the ping command based on the operating system
    flag: str = "-c" if platform.system() != "Windows" else "-n"
    ping_command: list[str] = ["ping", flag, "1", hostname]

    try:
        result: CompletedProcess = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    
def is_valid_authentication(auth: HTTPBasicAuth, jira_host_name: str) -> bool:
    url = f"https://{jira_host_name}:443/rest/api/2/myself"
    try:
        response: Response = requests.get(url, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return True
    except requests.RequestException:
        return False 
    
def add_worklog(url: str, body: WorkLog, auth: HTTPBasicAuth):
    try:
        response: Response = requests.post(url, auth=auth, json=body, timeout=90) # sometimes JIRA is slow (old tickets)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return True
    except requests.RequestException:
        return False