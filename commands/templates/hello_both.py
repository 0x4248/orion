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

def both(request: Request, value: str = "", extra: str = ""):
    return page.message(
        request,
        "BOTH",
        f"value = {value or '(none)'} | extra = {extra or '(none)'}"
    )

registry.register(Command(
    name="both",
    handler=both,
    summary="CLI + UI command",
    mode="both",
    form_fields=[
        {"name": "value", "type": "text"},
        {"name": "extra", "type": "date"}
    ],
))