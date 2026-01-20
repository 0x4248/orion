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
from core.registry import registry
from core.commands import Command
from core import page
import manpages.echo

def echo(request: Request, text: str = ""):
    if not text:
        return page.message(request, "ECHO", "No text provided")
    return page.message(request, "ECHO", text)

registry.register(Command(
    name="echo",
    handler=echo,
    summary="Echo back text",
    mode="both",
    form_fields=[
        {"name": "text", "type": "text"}
    ]
))
