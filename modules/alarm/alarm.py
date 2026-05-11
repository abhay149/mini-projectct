import json
from datetime import datetime

def set_alarm(text):
    time = "07:00"  # simple demo

    alarm = {
        "time": time,
        "created": str(datetime.now())
    }

    try:
        with open("data/alarms.json", "r") as f:
            alarms = json.load(f)
    except:
        alarms = []

    alarms.append(alarm)

    with open("data/alarms.json", "w") as f:
        json.dump(alarms, f, indent=4)

    return f"Alarm set for {time}"