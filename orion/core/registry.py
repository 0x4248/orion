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

from typing import Dict, Optional, List
from .commands import Command

class CommandRegistry:
    def __init__(self):
        self._cmds: Dict[str, Command] = {}

    def register(self, cmd: Command):
        if cmd.name in self._cmds:
            raise ValueError(f"Duplicate command: {cmd.name}")
        self._cmds[cmd.name] = cmd

    def get(self, name: str) -> Optional[Command]:
        return self._cmds.get(name)

    def all(self) -> List[Command]:
        return list(self._cmds.values())

registry = CommandRegistry()
