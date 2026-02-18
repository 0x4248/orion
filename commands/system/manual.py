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

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from orion.core.registry import registry
from orion.core.commands import Command
from orion.core import page

from orion.core.manual import manual_registry
from orion.core.commands import Command

router = APIRouter()
@router.get("/man/{name}")
def manual_page_api(request: Request, name: str):
    return manual_page(request, name)

def manual_page(request: Request, name: str = ""):
    if name == "":
        # show forum
        return RedirectResponse(url="/forum/man")
    man = manual_registry.get(name)
    if not man:
        return page.message(
            request,
            "MANUAL",
            error=f"No manual page for: {name}"
        )
    
    return page.static(request, f"MANUAL PAGE FOR: {man.name.upper()}", html=f"""
    <h1 style="text-align: center; text-transform: uppercase;">{man.name}</h1>
<pre>{man.text}</pre>

<a href="javascript:history.back()" style="text-align:center">[ BACK ]</a>
                       """, buttons=page.with_nav(page.DEFAULT_NAV))


def man_list(request: Request, startswith_filter: str = ""):
    page_entries = ""
    entries = manual_registry.all()
    for entry in entries:
        if startswith_filter == "":
            pass
        else:
            if not entry.name.startswith(startswith_filter.lower()):
                continue
        entry.name = entry.name.upper()
        page_entries += f"<li><a href=\"/man/{entry.name.lower()}\">{entry.name}</a></li>"
    if page_entries == "":
        page_entries = "<li><i>No manual entries found.</i></li>"
    return page.static(request, "MANUAL INDEX", html=f"""
        <h1 style="text-align: center;">MANUAL INDEX</h1>
        <ul>
            {page_entries}
        </ul>
    """, buttons=page.with_nav(page.DEFAULT_NAV))

registry.register(Command(
    name="man",
    handler=manual_page,
    summary="Show manual page for command",
    mode="both",
    form_fields=[
        {"name": "name", "type": "text"},
    ],
))

registry.register(Command(
    name="man.list",
    handler=man_list,
    summary="List all manual pages",
    mode="both",
    form_fields=[
        {"name": "startswith_filter", "type": "text"},
    ],
))

### ALIASES ###

registry.register(Command(
    name="?",
    handler=manual_page,
    summary="Show manual page for command",
    mode="both",
    form_fields=[
        {"name": "name", "type": "text"},
    ],
))


registry.register(Command(
    name="help",
    handler=manual_page,
    summary="Show manual page for command",
    mode="both",
    form_fields=[
        {"name": "name", "type": "text"},
    ],
))
