# SPDX-License-Identifier: GPL-3.0-only
# Orion System
#
# Copyright (C) 2026 0x4248
# Copyright (C) 2026 4248 Systems
#
# Orion is free software; you may redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 only,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import threading
import datetime
import time

from fastapi import Request, UploadFile
from core.registry import registry
from core.commands import Command
from core import page


global heartbeats_database
heartbeats_database = {
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
        time.sleep(0.75)

def calculate_average_heartbeat_bpm():
    if len(heartbeats_database["timestamp"]) < 2:
        return 0
    first_time = datetime.datetime.fromisoformat(heartbeats_database["timestamp"][0])
    last_time = datetime.datetime.fromisoformat(heartbeats_database["timestamp"][-1])
    total_seconds = (last_time - first_time).total_seconds()
    total_beats = len(heartbeats_database["timestamp"]) - 1
    if total_seconds == 0:
        return 0
    bpm = (total_beats / total_seconds) * 60
    return round(bpm, 2)
def return_bpm(request: Request):
    bpm = calculate_average_heartbeat_bpm()
    return page.message(
        request,
        "HEARTBEAT",
        f"Average server heart rate: {bpm} BPM",
    )

def return_heart_database(request: Request):
    bpm = calculate_average_heartbeat_bpm()
    return page.message(
        request,
        "HEARTBEAT",
        f"{heartbeats_database}",
    )

registry.register(Command(
    name="heart.bpm",
    handler=return_bpm,
    summary="Show server heartbeat rate",
    mode="cli",
))

registry.register(Command(
    name="heart.db_debug",
    handler=return_heart_database,
    summary="Show server heartbeat database",
    mode="cli",
))



heart = threading.Thread(target=heartbeat, daemon=True)
heart.start()

MOD_META = {
    "name": "System Heartbeats",
    "loc": "commands.system.heartbeats",
    "description": "Module that tracks server heartbeats.",
    "author": "0x4248",
    "version": "1.0.0",
    "license": "GPLv3",
}