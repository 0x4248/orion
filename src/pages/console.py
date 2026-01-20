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

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from core import page as p
from core.registry import registry
from core.commands import Command
from core import console


router = APIRouter()

@router.get("/console")
async def console_page(request: Request):
    body = "<h2>System Logs</h2>\n"
    body += "<span class='grey-text'>Press F4 to exit</span>\n"
    body += "<pre>\n"
    for log_id in sorted(console.log_db.logs.keys(), reverse=True):
        entry = console.log_db.logs[log_id]
        level = entry['level']
        level_class = level.lower()
        body += (
            f"[{entry['timestamp']}] "
            f"<span class='log-{level_class}'>[{level}]</span> "
            f"{entry['caller'].replace('BRIDGE', '<span style=\"color:lime;\">BRIDGE</span>')}: "
            f"{entry['message']}\n"
        )
    body += "</pre>\n"
    return p.static(
        request,
        "SYSTEM CONSOLE",
        body
    )

registry.register(Command(
    name="console",
    handler=console_page,
    summary="Show system logs",
    mode="cli"
))

registry.register(Command(
    name="c",
    handler=console_page,
    summary="Show system logs",
    mode="cli"
))
