import sys
from get_user_data import getUserData
from parse_user_data import parseUserData
from validate_user_data import validateUserData
from log_jira_time import logJiraTime
from generate_hash import generateHash
from save_generated_hash import saveGeneratedHash

jiraHostName = ""; defaultFileLocation = ""
commandLineArguments = sys.argv[1:]
print(f"\033[31mArguments: {commandLineArguments}\033[0m")
for argument in commandLineArguments:
    flagName, flagValue = argument.split("=")
    if flagName == "--jira" or flagName == "-j":
        jiraHostName = flagValue
    elif flagName == "--default-log-file-location" or flagName == "-l":
        defaultFileLocation = flagValue

if not jiraHostName:
    print("\033[31mMissing required flag --jira! We need to know your jira hostname to log you time!\033[0m")
else:
    data: str = getUserData(defaultFileLocation)

    if data:
        formattedData = parseUserData(data)
        logsHash = generateHash(formattedData)
        isValidData = validateUserData(formattedData, logsHash)
        if isValidData:
            print("\033[32mData is valid!\033[0m")
            isSuccessfullyLogged = logJiraTime(formattedData, jiraHostName)
            if isSuccessfullyLogged:
                saveGeneratedHash(logsHash)