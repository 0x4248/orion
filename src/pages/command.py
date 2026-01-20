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

import difflib
import shlex
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from core.registry import registry
from core import page as p 
from core import dispatcher

router = APIRouter()

@router.get("/command")
async def command_page(request: Request):
    lines = [
        f"[{c.name}] - {c.summary}"
        for c in registry.all()
        if c.supports_cli()
    ]
    return p.static(
        request,
        title="COMMAND",
        html=f"""
<p>Enter a command below to run. <i style="color:grey;">Usage: &lt;COMMAND&gt; [ARGS...]</i></p>
<form method="post">
<span style="color:grey;">$</span><input name="command" autofocus style="width:98%;border:0;border-bottom:1px solid #fff;">
</form>
<hr>
<pre>{chr(10).join(lines)}</pre>
"""
    )

def find_similar_commands(name: str, cutoff: float = 0.6):
    commands = [c.name for c in registry.all() if c.supports_cli()]
    return difflib.get_close_matches(name, commands, n=3, cutoff=cutoff)


@router.post("/command")
async def command_submit(request: Request, command: str = Form(...)):
    try:
        parts = shlex.split(command)
    except ValueError as e:
        return p.message(request, "ERROR", error=str(e))

    if not parts:
        return p.message(request, "ERROR", error="Empty command")

    name, *args = parts
    cmd = registry.get(name)

    if not cmd or not cmd.supports_cli():
        did_you_mean = find_similar_commands(name)
        if did_you_mean:
            hint = ", ".join(f"<a href='/command'>{cmd}</a>" for cmd in did_you_mean)
        else:
            hint = "no similar commands found"
        return p.message(request, "UNKNOWN", error=f"'{name}' is not a valid CLI command <br>Did you mean? {hint}")

    if cmd.supports_ui() and not args and cmd.form_fields:
        return RedirectResponse(f"/command/{name}", 303)

    if cmd.parse_mode == "raw":
        raw_args = command[len(name):].lstrip()
        args = [raw_args]

    return await dispatcher.dispatch(cmd.handler, request, *args)


@router.get("/command/{name}")
async def command_form(request: Request, name: str):
    cmd = registry.get(name)
    if not cmd or not cmd.supports_ui():
        return RedirectResponse("/command", 303)

    return p.form(
        request,
        title=name.upper(),
        action=f"/command/{name}",
        fields=cmd.form_fields,
        msg=cmd.summary,
    )

@router.post("/command/{name}")
async def command_form_submit(request: Request, name: str):
    cmd = registry.get(name)
    if not cmd or not cmd.supports_ui():
        return RedirectResponse("/command", 303)

    data = await request.form()
    return await dispatcher.dispatch(cmd.handler, request, **data)


@router.get("/list_forms")
async def list_forms(request: Request):
    cmds = [c for c in registry.all() if c.supports_ui()]

    links = "\n".join(
        f"<li><a href='/command/{c.name}'>{c.name}</a> — {c.summary}</li>"
        for c in cmds
    )

    return p.static(
        request,
        title="SEARCH PAGE",
        html=f"""
<p>Select a page to open:</p>
<ul>
{links}
</ul>
"""
    )

@router.get("/search_forms")
async def search_forms_page(request: Request):
    cmds = [c for c in registry.all() if c.supports_ui()]
    lines = [f"[{c.name}] - {c.summary}" for c in cmds]

    return p.static(
        request,
        title="SEARCH FORMS",
        html=f"""
<p>Open a UI page:</p>
<form method="post" action="/search_forms">
    ?<input name="page" type="text"
      style="width:98%;border:0;border-bottom:1px solid #fff;" autofocus />
</form>
<hr/>
<pre>Available:
{chr(10).join(lines)}</pre>
"""
)

@router.post("/search_forms")
async def search_forms_submit(request: Request, page: str = Form(...)):
    name = page.strip()

    if not name:
        return p.message(request, "ERROR", "No page name provided", ok_href="/search_forms")
    cmd = registry.get(name)
    if not cmd or not cmd.supports_ui():
        return p.message(request, "UNKNOWN", error=f"No UI page for: {name}", ok_href="/search_forms")
    return RedirectResponse(f"/command/{name}", 303)
