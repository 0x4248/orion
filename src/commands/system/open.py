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
from fastapi.responses import RedirectResponse
from core.registry import registry
from core.commands import Command
from core import page


def open_page(request: Request, name: str = ""):
    if not name:
        return page.message(
            request,
            "OPEN",
            "usage: open <page>"
        )

    cmd = registry.get(name)
    if not cmd or not cmd.supports_ui():
        return page.message(
            request,
            "OPEN",
            f"No UI page for: {name}"
        )

    return RedirectResponse(f"/command/{name}", status_code=303)

def goto(request: Request, name: str = ""):
    return RedirectResponse(f"/{name}", status_code=303)

registry.register(Command(
    name="open",
    handler=open_page,
    summary="Open a UI page",
    mode="cli",
))


registry.register(Command(
    name="goto",
    handler=goto,
    summary="Jumps to a url",
    mode="cli",
))

registry.register(Command(
    name="g",
    handler=goto,
    summary="Jumps to a url",
    mode="cli",
))
