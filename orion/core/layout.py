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

STLYLE_PATH = "orion/static/css/main.css"
SCRIPT_PATH = "orion/static/js/main.js"

with open(STLYLE_PATH, "r") as f:
    STYLE = f"<style>\n{f.read()}\n</style>"
  
with open(SCRIPT_PATH, "r") as f:
    SCRIPT = f"<script>\n{f.read()}\n</script>"



def layout(request: Request, title: str, buttons: list[tuple[str, str]], header_html: str | None, body_html: str) -> str:
    nav = " ".join(f"[<a href='{href}'>{label}</a>]" for label, href in buttons)
    header = header_html if header_html is not None else f"<div class='header'><strong>ORION SYSTEM:</strong> {title}<br>{nav}</div>"
    return f"""
    <html>
      <head>
      <title>ORION SYSTEM: {title}</title>
      {STYLE}
      </head>
      <body>
        {header}
        <hr/>
        {body_html}
      </body>
      {SCRIPT}
    </html>
    """
