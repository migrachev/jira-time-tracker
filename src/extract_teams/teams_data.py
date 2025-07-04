import json
from box import Box
from datetime import datetime
from functools import reduce
from typing import Callable

from ..console import demand_clipboard, demand_choice, clear_screen
from .utils import get_calendar_date, find_jira_id, get_duration, group_overlapping_events, remove_pattern_with_neighbors
from .validators import validate, is_new_teams_format, is_old_teams_format

def get() -> list[dict]:
    label: str = "\033[34mMake sure your clipboard contains your teams events data and press Enter\033[0m"
    warn: str = "We expect Enter, any other input is ignored!"
    invalid: str = "The data in clipboard content is invalid. Please check it and try again!"
    data = demand_clipboard(label, warn, invalid, validate)

    result = Box(json.loads(data))
    events: list = []
    fields: list[tuple[str, str]] = []
    if is_old_teams_format(data):
        events = result["value"] if isinstance(result, dict) else result
        fields: list[tuple[str, str]] = [
            ("isCancelled", "isCancelled"), 
            ("subject", "subject"), 
            ("startTime", "startTime"), 
            ("endTime", "endTime")
        ]
    elif is_new_teams_format(data):
        events = result["Body"]["Items"] if isinstance(result, dict) else result
        fields: list[tuple[str, str]] = [
            ("isCancelled", "IsCancelled"), 
            ("subject", "Subject"), 
            ("startTime", "Start"), 
            ("endTime", "End")
        ]

    if len(events) and len(fields):
        def extractor(item: dict) -> dict:
            result: dict = {}
            for field in fields:
                result_field, item_field = field
                if item_field in item:
                    result[result_field] = item[item_field]
            return result
        events = list(map(extractor, events))
    
    return events

def prepare(events: list[dict], period: tuple[str, str]) -> list[dict]:
    result = apply_period(events, period)
    result = ignore_cancelled(result)
    result = process_conventions(result)
    result = resolve_conflicts(result)
    result = simplify(result)

    result.sort(key=lambda item: datetime.fromisoformat(item["start"]))

    return result

def apply_period(events: list[dict], period: tuple[str, str]) -> list[dict]:
    start, end = period
    result: list[dict] = []

    for event in  events:
        event_date = get_calendar_date(event["startTime"]) # Events are always constraint in one day
        if event_date >= start and event_date <= end:
            result.append(event)

    return result

def ignore_cancelled(events: list[dict]) -> list[dict]:
    to_delete: set[int] = set([])

    for i, event in enumerate(events):
        if ("isCancelled" in event) and event["isCancelled"]:
            to_delete.add(i)

    to_delete_list: list[int] = list(to_delete)
    to_delete_list.sort(reverse = True)
    for index in to_delete_list:
        del events[index]

    return events

def process_conventions(events: list[dict]) -> list[dict]:
    index_to_delete: set[int] = set([])
    for i, outer_event in enumerate(events):
        for inner_event in events:
            subject = outer_event["subject"].strip()
            outer_start = outer_event["startTime"]
            outer_end = outer_event["endTime"]
            inner_start = inner_event["startTime"]
            inner_end = inner_event["endTime"]

            is_continue = subject.lower() in ["continue", "continuation", "cont"]
            is_prepare = subject.lower() in ["prepare", "preparation", "prep"]

            if is_continue and outer_start == inner_end:
                inner_event["endTime"] = outer_event["endTime"]
                index_to_delete.add(i)

            if is_prepare and outer_end == inner_start:
                inner_event["startTime"] = outer_event["startTime"]
                index_to_delete.add(i)

    to_delete_list: list[int] = list(index_to_delete)
    to_delete_list.sort(reverse = True)
    for to_delete in to_delete_list:
        del events[to_delete]

    return events

def resolve_conflicts(events: list[dict]) -> list[dict]:
    message = "\033[34mThese two event intersect in your calendar! Please let us know which one of they you want to keep\033[0m"
    grouped = group_overlapping_events(events)

    def resolve_group(accum: list[dict], group: list[dict]) -> list[dict]:
        options: dict = {}
        length = len(group)

        if length > 1:
            for i, event in enumerate(group):
                options[i] = event["subject"]
            all = "All" if length > 2 else "Both"
            options["all"] = all
            
            choice = demand_choice(message, options)
            if choice == "all":
                accum.extend(group)
            else:
                accum.append(group[int(choice)])
        else:
            accum.extend(group)

        return accum

    reduced = reduce(resolve_group, grouped, [])

    return list(reduced)

def simplify(events: list[dict]) -> list[dict]:
    def trim(event): # Trim unwanted data
        result: Box = Box()

        if ("startTime" in event) and ("endTime" in event) and ("subject" in event):
            result.start = get_calendar_date(event["startTime"])
            result.duration = get_duration(event["startTime"], event["endTime"], roundup=True) #TODO: Consider config for round
            
            jira_id = find_jira_id(event["subject"])
            if jira_id:
                result.subject = remove_pattern_with_neighbors(event["subject"], jira_id)
            else:
                result.subject = event["subject"]
            result.jira = jira_id
            
        return dict(result)
    
    return list(map(trim, events))

def parse(prepared: list[dict]) -> list[str]:
    result: list[str] = []
    day: str = ""
    for item in prepared:
        if not day or day != item["start"]:
            day = item["start"]
            result.append(day)
        duration = f"{item["duration"]:g}"
        subject = item["subject"]
        jira = f" {item["jira"]}" if item["jira"] else ""
        result.append(f"- {duration}h {subject}{jira}")

    return result

def output(parsed: list[str], period: tuple[str, str]):
    clear_screen()
    start, end  = period
    if len(parsed):
        print(f"\033[34mHere are the resulting events from {start} to {end}\033[0m")
    else:
        print(f"\033[33mNo events were found from {start} to {end}!\033[0m")
    for item in parsed:
        print(item)
