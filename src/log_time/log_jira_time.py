from utils import isReachable, isValidJiraAuthentication, addWorklog, startSpinnedThread
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPBasicAuth
from prompt_toolkit import prompt
from datetime import date
import threading

def logJiraTime(data: dict, jiraHostName: str) -> bool:
    loadingReachableCheckEvent = threading.Event()
    startSpinnedThread(loadingReachableCheckEvent)
    if not isReachable(jiraHostName):
        print("\033[31m\rJIRA instalation unreachable! Check your VPN status and/or connectivity!\033[0m")
        return False
    else:
        print("\r                                                      ")
        loadingReachableCheckEvent.set()
        while True:
            username = prompt("We will need your JIRA username: ")
            password = prompt("We will need your JIRA password: ", is_password=True)
            auth = HTTPBasicAuth(username, password)
            loadingCredentialsCheckEvent = threading.Event()
            startSpinnedThread(loadingCredentialsCheckEvent)
            if isValidJiraAuthentication(auth, jiraHostName):
                break
            else:
                print("\033[31m\rIncorrect credentials!\033[0m")
            loadingCredentialsCheckEvent.set()

        print("\r                                                      ")
        requests: list = []
        for dayTuple, logsList in data.items():
            day = date(*dayTuple)
            for time, comment, issue in logsList:
                started = f"{day.isoformat()}T10:00:00.000+0000"
                timeSpentHours = float(time[:-1])
                timeSpentSeconds = timeSpentHours * 60 * 60
                print(f"About to log \033[32m{time}\033[0m hours for \033[32m{day}\033[0m in issue \033[32m{issue}\033[0m with comment \033[32m{comment}\033[0m")
                request: dict = {
                    "url": f"https://{jiraHostName}:443/rest/api/2/issue/{issue}/worklog",
                    "body": {
                        "started": started,
                        "comment": comment,
                        "timeSpentSeconds": timeSpentSeconds
                    }
                }
                requests.append(request)
        print("\033[33m=============================================================================================================================================\033[0m")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures: dict = {}
            for request in requests:
                url, body = request.values()
                future = executor.submit(addWorklog, url, body, auth)
                futures[future] = url

            for future in as_completed(futures):
                url = futures[future]
                try:
                    isSuccessful: bool = future.result()
                    if isSuccessful:
                        print(f"\033[32mSuccessfully logged time @{url}\033[0m")
                    else:
                        print(f"\033[33mFiled to log time @{url}\033[0m")
                except:
                    print(f"\033[31mUnhandled exception during adding time log @{url}\033[0m")

        return True