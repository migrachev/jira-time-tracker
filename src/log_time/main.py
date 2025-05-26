import sys
from get_user_data import getUserData
from parse_user_data import parseUserData
from validate_user_data import validateUserData
from log_jira_time import logJiraTime
from generate_hash import generateHash
from save_generated_hash import saveGeneratedHash
from mytypes import UserData

jiraHostName: str = ""; defaultFileLocation: str = ""
flagName: str; flagValue: str
commandLineArguments: list[str] = sys.argv[1:]

for argument in commandLineArguments:
    flagName, flagValue = argument.split("=")
    if flagName == "--jira" or flagName == "-j":
        jiraHostName = flagValue
    elif flagName == "--default-log-file-location" or flagName == "-l":
        defaultFileLocation = flagValue

if not jiraHostName:
    print("\033[31mMissing required flag --jira! We need to know your jira hostname to log you time!\033[0m")
else:
    rawData: str = getUserData(defaultFileLocation)

    if rawData:
        userData: UserData = parseUserData(rawData)
        logsHash: list[str] = generateHash(userData)
        isValidData: bool = validateUserData(userData, logsHash)
        if isValidData:
            print("\033[32mData is valid!\033[0m")
            isSuccessfullyLogged: bool = logJiraTime(userData, jiraHostName)
            if isSuccessfullyLogged:
                saveGeneratedHash(logsHash)