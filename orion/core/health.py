import threading
import datetime
import time
import requests
from orion.core.console import logger
from config import globals

global heartbeats_database
heartbeats_database = {
    "id": [],
    "timestamp": [],
    "status": []
}

global http_heartbeats_database
http_heartbeats_database = {
    "id": [],
    "timestamp": [],
    "status": []
}

def heartbeat():
    heartbeat_id = 0
    while True:
        heartbeats_database["id"].append(heartbeat_id)
        heartbeats_database["timestamp"].append(datetime.datetime.now().isoformat())
        heartbeats_database["status"].append("alive")
        heartbeat_id += 1
        if not threading.main_thread().is_alive():
            break
        time.sleep(0.74)

def http_heartbeat():
    heartbeat_id = 0
    while True:
        try:
            response = requests.get(f"http://{globals.ORION_HOST}:{globals.ORION_PORT}")
            status = "alive" if response.status_code == 200 else "unreachable"
        except requests.RequestException:
            status = "unreachable"
        http_heartbeats_database["id"].append(heartbeat_id)
        http_heartbeats_database["timestamp"].append(datetime.datetime.now().isoformat())
        http_heartbeats_database["status"].append(status)
        heartbeat_id += 1
        if not threading.main_thread().is_alive():
            break
        time.sleep(5)



def check_heartbeat():
    if len(heartbeats_database["timestamp"]) < 2:
        return
    first_time = datetime.datetime.fromisoformat(heartbeats_database["timestamp"][-2])
    last_time = datetime.datetime.fromisoformat(heartbeats_database["timestamp"][-1])
    total_seconds = (last_time - first_time).total_seconds()
    if total_seconds == 0:
        return
    bpm = (1 / total_seconds) * 60
    return round(bpm, 2)



def check_heartbeats_thread():
    faults_detected = 0
    while True:
        bpm = check_heartbeat()
        if bpm is not None and bpm < 70:
            logger.warning(f"Low server heartbeat detected: {bpm} BPM")
        if not threading.main_thread().is_alive():
            break
        time.sleep(5)
    
heart = threading.Thread(target=heartbeat, daemon=True)
heart.start()

heart_check = threading.Thread(target=check_heartbeats_thread, daemon=True)
heart_check.start()

