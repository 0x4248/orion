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
import base64
from core.registry import registry
from core.commands import Command


router = APIRouter()

# The mascot looks like Wheatley from Portal 2, Because hes cute!
mascot_image_path = "./static/mascot.png"
with open(f"{mascot_image_path}", "rb") as f:
    mascot_image_data = base64.b64encode(f.read()).decode("utf-8")

with open("COPYRIGHT.txt", "r") as f:
    LEGAL = f.read()

@router.get("/about")
async def about_page(request: Request):
    return p.static(
        request,
        title="ABOUT",
        html=f"""
<h1 style="text-align: center;">ORION SYSTEM</h1>
<img
  src="data:image/png;base64,{mascot_image_data}"
  alt="Orion Mascot"
  style="display:block; width:400px; image-rendering: pixelated; margin: 0 auto;"
>
<br>
<p style="text-align: center">{LEGAL}</p>
<pre>

Version: 0.8.4
Engine: OrionEngine
Online Users: 1
© 2026 0x4248
</pre>
"""
    )

async def about_alias(request: Request):
    return RedirectResponse(url="/about", status_code=302)

registry.register(Command(
    name="about",
    handler=about_alias,
    summary="Show information about Orion",
    mode="cli"
))
