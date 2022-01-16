import atexit
from datetime import datetime
import json
import os
import requests
import schedule
import time

#categories available: AGE12TO17, Communities, Targeted, MODERNASECONDPUBLIC

global DATA_DIR
global LAST_RUN_JSON

#api-endpoint
VACCINETO_API_SLOTS="https://vaccineto.ca/api/slots"

def get_open_slots(time):
    global DATA_DIR
    global LAST_RUN_JSON
    
    counter = 0
    name = ""

    with open(os.path.join(DATA_DIR, LAST_RUN_JSON)) as last_run_json_file:
        last_run_json = json.load(last_run_json_file)

    response = requests.get(url = VACCINETO_API_SLOTS)
    full_data = response.json()
    data = full_data["data"]
    parsed_data = {}
    parsed_data["date_fetched"] = datetime.now(time).strftime("%Y-%d-%mT%H:%M:%S")
    parsed_data["data"] = {}

    for clinic in data:
        total_open_slots = 0
        clinic_data = {}
        clinic_data["name"] = data[clinic]["name"]
        clinic_data["open_slots"] = {}
        clinic_open_slots = {}
        clinic_open_slots_group = {}

        for group in data[clinic]['availabilities']:
            open_slots = 0
            clinic_open_slots_group_open_slots = {}
            for slot in data[clinic]["availabilities"][group]:
                open_slots = data[clinic]["availabilities"][group][slot]
                trimmed_datetime = slot.split("T")[0]
                clinic_open_slots_group_open_slots[trimmed_datetime] = open_slots
                total_open_slots += open_slots
            clinic_open_slots_group[group] = clinic_open_slots_group_open_slots

        clinic_data["open_slots"] = clinic_open_slots_group
        clinic_data["total_open_slots"] = total_open_slots
        parsed_data["data"][clinic] = clinic_data

    date_time_obj = datetime.now(time)
    output_json_file = "{}.json".format(date_time_obj.strftime("%Y-%d-%m_%H-%M-%S"))

    for clinic in parsed_data["data"]:

        total_open_slots = parsed_data["data"][clinic]["total_open_slots"]
        if clinic in last_run_json["data"]:
            last_run_total_open_slots = last_run_json["data"][clinic]["total_open_slots"]
            total_diff_since_last_run = total_open_slots - last_run_json["data"][clinic]["total_open_slots"] 
        else:
            last_run_total_open_slots = total_open_slots
            total_diff_since_last_run = total_open_slots
        parsed_data["data"][clinic]["change_since_last_fetch"] = total_open_slots - last_run_total_open_slots

        counter = 1;

        if(total_open_slots < 200):
            continue

        for group in parsed_data["data"][clinic]["open_slots"]:
            group_summary_msg = "Group: {}\n".format(group)
            are_slots_available = False
            for date in parsed_data["data"][clinic]["open_slots"][group]:
                available_slots = parsed_data["data"][clinic]["open_slots"][group][date]
                if (available_slots > 0):
                    are_slots_available = True
                    if (clinic in last_run_json["data"]) and (group in last_run_json["data"][clinic]["open_slots"]) and (date in last_run_json["data"][clinic]["open_slots"][group]):
                        diff_since_last_run_slot = available_slots - last_run_json["data"][clinic]["open_slots"][group][date]
                    else:
                        diff_since_last_run_slot = available_slots
                    group_summary_msg += "{} : {} ({:+})\n".format(date, available_slots, diff_since_last_run_slot)
        
        if(total_open_slots > 200):
            name = parsed_data["data"][clinic]["name"]
        else:
            continue

        if counter == 1:
            break;

    with open(os.path.join(DATA_DIR, output_json_file), 'w') as output_json:
        json.dump(parsed_data, output_json, indent=4)
    LAST_RUN_JSON = output_json_file

    return name

