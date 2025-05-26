from utils import isReachable, isValidJiraAuthentication, addWorklog, startSpinnedThread
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from requests.auth import HTTPBasicAuth
from prompt_toolkit import prompt
from datetime import date
from threading import Event
from mytypes import UserData, WorkLog, WorkLogRequest

def logJiraTime(userData: UserData, jiraHostName: str) -> bool:
    loadingReachableCheckEvent: Event = Event()
    startSpinnedThread(loadingReachableCheckEvent)
    if not isReachable(jiraHostName):
        print("\033[31m\rJIRA instalation unreachable! Check your VPN status and/or connectivity!\033[0m")
        return False
    else:
        print("\r                                                      ")
        loadingReachableCheckEvent.set()
        while True:
            username: str = prompt("We will need your JIRA username: ")
            password: str = prompt("We will need your JIRA password: ", is_password=True)
            auth: HTTPBasicAuth = HTTPBasicAuth(username, password)
            loadingCredentialsCheckEvent: Event = Event()
            startSpinnedThread(loadingCredentialsCheckEvent)
            if isValidJiraAuthentication(auth, jiraHostName):
                break
            else:
                print("\033[31m\rIncorrect credentials!\033[0m")
            loadingCredentialsCheckEvent.set()

        print("\r                                                      ")
        requests: list[WorkLogRequest] = []
        dayTuple: tuple[int, int, int]; logsTuple: tuple[str, str, str]
        for dayTuple, logsTuple in userData.items():
            day: date = date(*dayTuple)
            time: str; comment: str; issue: str
            for time, comment, issue in logsTuple:
                started: str = f"{day.isoformat()}T10:00:00.000+0000"
                timeSpentHours: float = float(time[:-1])
                timeSpentSeconds: float = timeSpentHours * 60 * 60
                print(f"About to log \033[32m{time}\033[0m hours for \033[32m{day}\033[0m in issue \033[32m{issue}\033[0m with comment \033[32m{comment}\033[0m")
                request: WorkLogRequest = {
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
            futures: dict[Future[bool], str] = {}
            for request in requests:
                request: WorkLogRequest
                url: str = request["url"]
                body: WorkLog = request["body"]
                future: Future[bool] = executor.submit(addWorklog, url, body, auth)
                futures[future] = url

            for future in as_completed(futures):
                url: str = futures[future]
                try:
                    isSuccessful: bool = future.result()
                    if isSuccessful:
                        print(f"\033[32mSuccessfully logged time @{url}\033[0m")
                    else:
                        print(f"\033[33mFiled to log time @{url}\033[0m")
                except:
                    print(f"\033[31mUnhandled exception during adding time log @{url}\033[0m")
        return True