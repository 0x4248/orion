# SPDX-License-Identifier: GPL-3.0-only
# Orion System
#
# Modules list configuration file
# This file tells orion which modules to load at startup.
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


MODULES = [
    "commands.system.open",
    "commands.system.heartbeats",
    "commands.testing.demo",
    "commands.echo",
    "commands.system.sqldb"
]