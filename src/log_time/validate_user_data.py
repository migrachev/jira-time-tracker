from utils import isProperWorkWeek, areJiraIdentifierValid, areTimesValid, isFullyLoggedWeek, isInConflictWithPreviousExecution
from mytypes import UserData

def validateUserData(userData: UserData, logsHash: list[str]):
    isValid = True

    if not isProperWorkWeek(userData):
        print("\033[31mWeek days defined in the input data are improper!\033[0m")
        isValid = False
    elif not areJiraIdentifierValid(userData):
        print("\033[31mJIRA identifier of the provided logs are missing or improper!\033[0m")
        isValid = False
    elif not areTimesValid(userData):
        print("\033[31mLog times provided in the data are missing or improper!\033[0m")
        isValid = False
    elif not isFullyLoggedWeek(userData):
        print("\033[31mThe total sum of worked hours is not 40!\033[0m")
        isValid = False
    elif isInConflictWithPreviousExecution(logsHash):
        print("\033[31mInput data have already been process!\033[0m")
        isValid = False

    return isValid
