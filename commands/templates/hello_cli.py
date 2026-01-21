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

from fastapi import Request
from orion.core.registry import registry
from orion.core.commands import Command
from orion.core import page

def hello_cli(request: Request, *args):
    name = args[0] if args else "world"
    return page.message(request, "HELLO (CLI)", f"hello {name}")

registry.register(Command(
    name="hello.world",
    handler=hello_cli,
    summary="CLI-only hello",
    mode="cli",
))