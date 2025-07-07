import json
from datetime import datetime

def validate(data: str) -> bool:
    return is_old_teams_format(data) or is_new_teams_format(data)

def is_new_teams_format(data: str) -> bool:
    result = True
    try:
        jsondata = json.loads(data)
        if isinstance(jsondata, dict):
            jsondata = jsondata["Body"]["Items"]
        if isinstance(jsondata, list):
            for item in jsondata:
                startTime = item["Start"]
                endTime = item["End"]
                subject = item["Subject"]
                organizer = item["Organizer"]
                if not startTime or not endTime or not organizer or not subject:
                    result = False
                    break
                datetime.fromisoformat(startTime)
                datetime.fromisoformat(endTime)
        else:
            result = False
    except Exception as _:
        result = False

    return result

def is_old_teams_format(data: str) -> bool:
    result = True
    try:
        jsondata = json.loads(data)
        if isinstance(jsondata, dict) and "value" in jsondata:
            jsondata = jsondata["value"]
        if isinstance(jsondata, list):
            for item in jsondata:
                startTime = item["startTime"]
                endTime = item["endTime"]
                utcOffset = item["utcOffset"]
                subject = item["subject"]
                if not startTime or not endTime or not utcOffset or not subject:
                    result = False
                    break
                datetime.fromisoformat(startTime)
                datetime.fromisoformat(endTime)
        else:
            result = False
    except Exception as _:
        result = False

    return result