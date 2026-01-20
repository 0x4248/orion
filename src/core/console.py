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

import datetime
from typing import Dict
import traceback

from core.page import message

global logger
global log_db

import sys

def _get_caller():
    f = sys._getframe(2)
    module = f.f_globals.get("__name__", "<unknown>")
    func = f.f_code.co_name
    return f"{module}.{func}()"


class LogDatabase:
    def __init__(self):
        self.logs = {}

    def add_entry(self, level: str, caller: str, message: str) -> int:
        log_id = len(self.logs) + 1
        timestamp = datetime.datetime.now().isoformat()
        self.logs[log_id] = {
            "id": log_id,
            "timestamp": timestamp,
            "level": level,
            "caller": caller,
            "message": message
        }
        return log_id
    
class Logger:
    def __init__(self, bark: bool = True, log_db_inp: LogDatabase | None = None):
        self.bark = bark
        self.log_db = log_db_inp
    def log(self, caller: str = "Unknown", m: str | None = None, level: str = "INFO") -> int:
        if self.log_db is None:
            raise ValueError("No log database provided")
        if m is None:
            m = "No message provided"
        if self.bark:
            print(f"[{level}] {caller}: {m}")
        log_id = log_db.add_entry(level, caller, m)
        return log_id
    
    def debug(self, caller: str | None = None, m: str | None = None) -> int:
        if caller is None:
            caller = _get_caller()
        return self.log(caller, m, "DEBUG")

    def info(self, caller: str | None = None, m: str | None = None) -> int:
        if caller is None:
            caller = _get_caller()
        return self.log(caller, m, "INFO")
    
    def warning(self, caller: str | None = None, m: str | None = None) -> int:
        if caller is None:
            caller = _get_caller()
        return self.log(caller, m, "WARNING")
    
    def error(self, caller: str | None = None, m: str | None = None) -> int:
        if caller is None:
            caller = _get_caller()
        return self.log(caller, m, "ERROR")
    
    def critical(self, caller: str | None = None, m: str | None = None) -> int:
        if caller is None:
            caller = _get_caller()
        return self.log(caller, m, "CRITICAL")
    
    def alarm(self, caller: str | None = None, m: str | None = None) -> int:
        if caller is None:
            caller = _get_caller()
        return self.log(caller, m, "ALARM")

# If already imported dont reinit
if 'logger' not in globals():
    log_db = LogDatabase()
    logger = Logger(bark=True, log_db_inp=log_db)
    logger.info(m="Logger initialized successfully")
else:
    logger.info(m="Logger already initialized, skipping reinitialization")