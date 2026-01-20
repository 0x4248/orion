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

from fastapi import Request, UploadFile
from core.registry import registry
from core.commands import Command
from core import page


def hello_cli(request: Request, *args):
    name = args[0] if args else "world"
    return page.message(request, "HELLO (CLI)", f"hello {name}")

registry.register(Command(
    name="hello",
    handler=hello_cli,
    summary="CLI-only hello",
    mode="cli",
))

def ui_only(request: Request, text: str = ""):
    return page.message(
        request,
        "UI ONLY",
        f"You typed: {text or '(empty)'}"
    )

registry.register(Command(
    name="uionly",
    handler=ui_only,
    summary="UI-only command",
    mode="ui",
    form_fields=[
        {"name": "text", "type": "text"},
    ],
))

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
        {"name": "extra", "type": "time"}
    ],
))


def both_plus(
    request: Request,
    value: str = "",
    enable: str | None = None,
    payload: UploadFile | None = None,
):
    flags = []
    if enable:
        flags.append("enable")

    file_info = "(none)"

    file_data = payload.file.read() if payload else None
    if payload:
        file_info = payload.filename

    return page.message(
        request,
        "BOTH+",
        f"value={value}\nflags={flags}\nfile={file_data}"
    )


registry.register(Command(
    name="both_plus",
    handler=both_plus,
    summary="CLI + UI + checkbox + file",
    mode="both",
    form_fields=[
        {"name": "value", "type": "text"},
        {"name": "enable", "type": "checkbox"},
        {"name": "payload", "type": "file"},
    ],
))


def file_demo(request: Request, upload: UploadFile | None = None):
    if not upload:
        return page.message(
            request,
            "FILE DEMO",
            error="No file uploaded"
        )

    data = upload.file.read()
    return page.message(
        request,
        "FILE DEMO",
        f"Uploaded file: {upload.filename} ({len(data)} bytes)"
    )

