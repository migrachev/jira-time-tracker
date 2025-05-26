import re
import subprocess
import platform
import requests
import itertools
import sys
import time
import threading
from requests.auth import HTTPBasicAuth
from datetime import datetime
from pathlib import Path
from typing import KeysView
from mytypes import UserData, WorkLog
from subprocess import CompletedProcess
from requests import Response

def parseIsoDate(date_str: str) -> tuple[int, int, int]:
    year, month, day = map(int, date_str.split("-"))
    return year, month, day

def isValidDate(date_str: str) -> bool:
    try:
        date_str = '-'.join([str(int(part)) for part in date_str.split('-')])
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def splitWorkLog(s: str) -> tuple[str, str, str]:
    if s.startswith('-'):
        s = s[1:]
    s = s.strip()
    
    first_space_index: int = s.find(' ')
    last_space_index: int = s.rfind(' ')
    
    if first_space_index == -1:
        return s, '', ''
    
    first_part: str = s[:first_space_index]
    second_part: str = s[first_space_index + 1:last_space_index] if last_space_index != first_space_index else ''
    third_part: str = s[last_space_index + 1:]
    
    return first_part, second_part, third_part

def isProperWorkWeek(data: UserData) -> bool:
    dates: KeysView = data.keys()
    date_objects: list[datetime] = [datetime(year=y, month=m, day=d) for (y, m, d) in dates]
    first_week: int = date_objects[0].isocalendar()[1]
    working_days: set = set()

    for date in date_objects:
        if date.weekday() < 5:
            if date.isocalendar()[1] != first_week:
                return False
            working_days.add(date.weekday())
    
    return len(working_days) == 5

def areJiraIdentifierValid(data: UserData) -> bool:
    result: bool = True
    pattern = r'^[A-Z]{1,10}-\d+$'

    issues: list = []; value: tuple[str, str, str]
    for _, value in data.items():
        issue: str
        for _, _, issue in value:
            issues.append(issue)

    for issue in issues:
        issue: str
        if not re.match(pattern, issue):
            result = False

    return result

def areTimesValid(data: UserData) -> bool:
    result: bool = True

    times: list = []; value: tuple[str, str, str]
    for _, value in data.items():
        time: str
        for time, _, _ in value:
            times.append(time)

    for time in times:
        time: str
        if not time.endswith('h'):
            result = False
            break

        time = time[:-1]
        if not re.match(r'^\d+(\.5)?$', time):
            result = False
            break

        timeValue = float(time)
        if timeValue <= 0 or timeValue > 8:
            result = False
            break

    return result

def isFullyLoggedWeek(data: UserData): #expects already checked data with areTimesValid
    total: float = 0; value: tuple[str, str, str]
    for _, value in data.items():
        time: str
        for time, _, _ in value:
            total = total + float(time[:-1])

    return total == 40

def isReachable(hostname: str) -> bool:
    # Define the ping command based on the operating system
    flag: str = "-c" if platform.system() != "Windows" else "-n"
    ping_command: list[str] = ["ping", flag, "1", hostname]

    try:
        result: CompletedProcess = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    
def isInConflictWithPreviousExecution(logs: list[str]) -> bool:
    scriptDir: Path = Path(__file__).parent
    rootDir: Path = scriptDir.parent.parent
    filePath: Path = rootDir / "data-hash-logs.log"
    with open(filePath, "r") as logsFile:
        result = False
        for line in list(logsFile):
            if line in logs:
                result = True
        return result

def isValidJiraAuthentication(auth: HTTPBasicAuth, jiraHostName: str) -> bool:
    url = f"https://{jiraHostName}:443/rest/api/2/myself"
    try:
        response: Response = requests.get(url, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return True
    except requests.RequestException:
        return False 
    
def addWorklog(url: str, body: WorkLog, auth: HTTPBasicAuth):
    try:
        response: Response = requests.post(url, auth=auth, json=body, timeout=90) # sometimes JIRA is slow (old tickets)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return True
    except requests.RequestException:
        return False
    
def spinner(LoadingEvent):
    for symbol in itertools.cycle(["Processing |", "Processing /", "Processing -", "Processing \\"]):
        if LoadingEvent.is_set():
            break
        sys.stdout.write(f"\r{symbol}")
        sys.stdout.flush()
        time.sleep(0.2)  #Speed of rotation

def startSpinnedThread(LoadingEvent):
    spinner_thread = threading.Thread(target=spinner, args=(LoadingEvent,), daemon=True)
    spinner_thread.start()