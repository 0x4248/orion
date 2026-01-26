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
from orion.core import page as p
from orion.core import console
from orion.core.console import logger
import hashlib
router = APIRouter()

from orion.core.jsondb import JsonDatabase  # adjust import as needed

users_db = JsonDatabase("data/auth.json")

def hashing_process(password: str) -> str:
    logger.info(m="Hashing password", caller="Auth_HashingProcess")
    # HACK: This is a custom hashing process for Orion, why? well SHA256 is easy
    # brute force. I plan on using seeds.
    part_a = hashlib.sha256(password.encode()).hexdigest()
    part_b = hashlib.sha256(password[::-1].encode()).hexdigest()
    combined = part_a + part_b
    final_hash = hashlib.sha256(combined.encode()).hexdigest()
    return final_hash

# initialize on first run
if not users_db.is_initialized() or "users" not in users_db.data:
    users_db.set("users", {
        "admin": {
            "password": hashing_process("admin"),
            "roles": ["admin", "user", "db"],
            "email": "admin@orion",
            "telephone": "101",
            "changeme": True
        },
        "user": {
            "password": hashing_process("user"),
            "roles": ["user"],
            "email": "user@orion",
            "telephone": "111",
            "changeme": True
        }
    })


def role_check(user: str, role: str) -> bool:
    logger.info(m=f"Checking role '{role}' for user '{user}'", caller="Auth_RoleCheck")
    users = users_db.data["users"]
    if user in users and role in users[user]["roles"]:
        return True
    return False





async def auth_middleware(request: Request, call_next):
    console.logger.info(m=f"{request.method} {request.url.path} from {request.client.host}. USER: {request.cookies.get('user', 'Anonymous')}", caller="HTTP_Middleware")
    if request.url.path.startswith("/login"):
        return await call_next(request)

    user = request.cookies.get("user")
    users = users_db.data["users"]
    if user and user in users:
        response = await call_next(request)
        return response

    return RedirectResponse(url="/login", status_code=303)

# ---- routes ----

@router.get("/login")
async def login_page(request: Request):
    return p.form(
        request,
        title="LOGIN",
        action="/login",
        fields=[
            {"name": "username"},
            {"name": "password", "type": "password"},
        ],
        msg="Please login with your credentials.",
    )


@router.get("/change_password")
async def change_password_page(request: Request, error: str | None = None):
    error = request.query_params.get("error", "")
    return p.form(
        request,
        title="CHANGE PASSWORD",
        action="/change_password",
        fields=[
            {"name": "new_password", "type": "password"},
            {"name": "confirm_password", "type": "password"},
        ],
        msg="A password change has been requested for your account. Please enter a new password.",
        error=error
    )


@router.post("/change_password")
async def change_password_submit(
    request: Request,
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    user = request.cookies.get("user")
    users = users_db.data["users"]
    if not user or user not in users:
        return RedirectResponse(url="/login", status_code=303)

    if new_password != confirm_password:
        return RedirectResponse(
            url="/change_password?error=Passwords+do+not+match.",
            status_code=303
        )

    users[user]["password"] = hashing_process(new_password)
    users[user]["changeme"] = False

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("user", user, httponly=True)
    return response


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    users = users_db.data["users"]
    user = users.get(username)
    if user and user["password"] == hashing_process(password):
        if user.get("changeme", True):
            response = RedirectResponse(url="/change_password", status_code=303)
            response.set_cookie("user", username, httponly=True)
            return response
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie("user", username, httponly=True)
        return response

    return p.form(
        request,
        title="LOGIN",
        action="/login",
        fields=[
            {"name": "username"},
            {"name": "password", "type": "password"},
        ],
        error="Invalid username or password.",
    )

@router.get("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("user")
    return response
