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
print(r"""
   ____  _____  _____ ____  _   _ 
  / __ \|  __ \|_   _/ __ \| \ | |
 | |  | | |__) | | || |  | |  \| |
 | |  | |  _  /  | || |  | | . ` |
 | |__| | | \ \ _| || |__| | |\  |
  \____/|_|  \_\_____\____/|_| \_|
""")
import datetime
print(f"Orion System init called at {datetime.datetime.now().isoformat()}")
print("")
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from orion.core.logbridge import logBridge
from orion.pages import command, about, console
from orion.pages import menu as menu_pages
from orion.core import auth, console
from orion.core import page as p
from commands.system import manual
from config.modules import MODULES
from config.plugins import ENABLED_MODULES
from config.rules.preload import PRELOAD_TASKS
from config import globals
from config.plugins import ENABLED_MODULES
from orion.core.plugins import PluginManager

# Load modules via the PluginManager which supports enable/disable controls.
pm_modules = PluginManager(MODULES, ENABLED_MODULES)
console.logger.info(m="Loading modules via PluginManager", caller="Main.ModuleLoader")
pm_modules.load_all()
for info in pm_modules.list():
    console.logger.info(m=f"Plugin: {info.path} enabled={info.enabled} loaded={info.loaded}", caller="Main.PluginStatus")


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


for target in PRELOAD_TASKS:
    console.logger.info(m=f"Preloading: {target.__name__}", caller="Preloader")
    target()

app = FastAPI()

console.logger.info(m="Including routers and middleware...", caller="Main")

app.middleware("http")(auth.auth_middleware)

app.include_router(auth.router)
app.include_router(command.router)
app.include_router(about.router)
app.include_router(manual.router)
app.include_router(menu_pages.router)

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

@app.get("/")
async def index(request: Request):
    return p.static(
        request,
        "ORION SYSTEM",
        "<h1>Welcome to Orion System</h1>"
        "<a href='/command'>[ RUN COMMAND ]</a><br>"
        "<a href='/menus'>[ OPEN MENUS ]</a><br>"
        "<a href='/search_forms'>[ OPEN A FORM ]</a><br>"
        "<a href='/about'>[ ABOUT SYSTEM ]</a><br>"
        "<a href='/logout'>[ LOGOUT ]</a><br>"
    )

if __name__ == "__main__":
    import uvicorn
    console.logger.info(m="Orion setup almost complete, starting uvicorn server...", caller="Main")
    console.logger.info(m=f"Running Orion on {globals.ORION_HOST}:{globals.ORION_PORT}", caller="Main")
    uvicorn.run(
        app,
        host=globals.ORION_HOST,
        port=globals.ORION_PORT,
        log_config=None,
        access_log=True,
    )
