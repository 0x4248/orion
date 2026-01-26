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

import json
from pathlib import Path
from datetime import datetime
from orion.core import console

JSONDB_VERSION = "1.0.0"

class JsonDatabase:
    def __init__(self, path):
        console.logger.info(m=f"Initializing JSON Database at {path}", caller="JsonDatabase")
        self.path = Path(path)
        self.data = {}

        if self.path.exists():
            console.logger.info(m="Database file found. Loading data.", caller="JsonDatabase")
            self.load()

    def is_initialized(self):
        return self.path.exists()
    
    def load(self):
        console.logger.info(m="Loading data from JSON Database", caller="JsonDatabase")
        with self.path.open("r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self, managed_by_self=False):
        if not managed_by_self:
            self.generate_metadata("write")
        console.logger.info(m="Saving data to JSON Database", caller="JsonDatabase")
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        console.logger.debug(m=f"Retrieving key '{key}' from JSON Database", caller="JsonDatabase")
        self.generate_metadata("read")
        return self.data.get(key, default)

    def set(self, key, value):
        console.logger.debug(m=f"Setting key '{key}' in JSON Database", caller="JsonDatabase")
        self.data[key] = value
        self.generate_metadata("write")
        self.save(managed_by_self=True)
    
    def unique_set(self, key, value):
        if key in self.data:
            raise ValueError("key already exists")
        self.set(key, value)

    def delete(self, key):
        console.logger.debug(m=f"Deleting key '{key}' from JSON Database", caller="JsonDatabase")
        if key in self.data:
            del self.data[key]
            self.generate_metadata("write")
            self.save(managed_by_self=True)

    def generate_metadata(self, mode):
        if "metadata" not in self.data:
            self.data["metadata"] = {
                "writes": 0,
                "reads": 0,
                "creation_date": datetime.now().isoformat(),
                "last_modified_date": datetime.now().isoformat(),
                "last_accessed_date": datetime.now().isoformat(),
                "version": JSONDB_VERSION,
            }
        else:
            if mode == "read":
                self.data["metadata"]["reads"] += 1
                self.data["metadata"]["last_accessed_date"] = datetime.now().isoformat()
            elif mode == "write":
                self.data["metadata"]["writes"] += 1
                self.data["metadata"]["last_modified_date"] = datetime.now().isoformat()

    def all(self):
        self.generate_metadata("read")
        return self.data