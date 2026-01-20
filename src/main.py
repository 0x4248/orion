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

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from core.logbridge import logBridge
from pages import command, about, console
from core import auth, console
from core import page as p
from commands.system import manual
from config.modules import MODULES

def load_commands():
    for module_path in MODULES:
        console.logger.info(m=f"Loading module: {module_path}", caller="ModuleLoader")
        __import__(module_path)

load_commands()

import logging

handler = logBridge(console.logger)
handler.setFormatter(logging.Formatter("%(message)s"))

root = logging.getLogger()
root.handlers.clear()
root.addHandler(handler)
root.setLevel(logging.WARNING)

for name in (
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
    "fastapi",
):
    log = logging.getLogger(name)
    log.handlers.clear()
    log.addHandler(handler)
    log.propagate = False


app = FastAPI()

console.logger.info(m="Starting Orion Web Application")

app.middleware("http")(auth.auth_middleware)

app.include_router(auth.router)
app.include_router(command.router)
app.include_router(about.router)
app.include_router(manual.router)

console.logger.info(m=app.router.routes)

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return p.static(
        request,
        "404 NOT FOUND",
        "<pre class='error'>404 NOT FOUND</pre>"
        "<a href='javascript:history.back()'>[ BACK ]</a>",
    )

@app.exception_handler(500)
async def server_error(request: Request, exc):
    return p.static(
        request,
        "500 SERVER ERROR",
        "<pre class='error'>500 SERVER ERROR</pre><pre class='grey-text'>{}</pre>".format(str(exc)) +
        "<a href='javascript:history.back()'>[ BACK ]</a>",
    )

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("./static/mascot.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
        access_log=True,
    )
