from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from typing import Optional

from orion.core import page as p
from orion.core.menu import manager as menu_manager
from orion.core import dispatcher
from orion.core.registry import registry

router = APIRouter()


@router.get("/menus")
async def menus_list(request: Request):
    menus = menu_manager.list_menus()
    links = "\n".join(f"<li><a href='/menu/{m.id}'>{m.title}</a></li>" for m in menus)
    return p.static(request, title="MENUS", html=f"<ul>{links}</ul>")


@router.get("/menu/{menu_id}")
async def menu_page(request: Request, menu_id: str):
    m = menu_manager.get_menu(menu_id)
    if not m:
        return p.message(request, "ERROR", error=f"Unknown menu: {menu_id}")

    entries = [e.to_tuple(menu_id) for e in m.list_entries()]
    return p.menu(request, title=m.title, entries=entries)


@router.get("/menu/{menu_id}/run/{entry_id}")
async def menu_run(request: Request, menu_id: str, entry_id: str, args: Optional[list[str]] = None):
    m = menu_manager.get_menu(menu_id)
    if not m:
        return p.message(request, "ERROR", error=f"Unknown menu: {menu_id}")

    entry = next((e for e in m.list_entries() if e.id == entry_id), None)
    if not entry:
        return p.message(request, "ERROR", error=f"Unknown menu entry: {entry_id}")

    if entry.kind == "link":
        # direct link
        return RedirectResponse(entry.target, 303)

    if entry.kind == "command":
        cmd = registry.get(entry.target)
        if not cmd:
            return p.message(request, "ERROR", error=f"Unknown command: {entry.target}")

        # If UI form is available, forward to its page
        if cmd.supports_ui() and cmd.form_fields:
            return RedirectResponse(f"/command/{cmd.name}", 303)

        # Collect positional args from query (?args=one&args=two) if present
        raw_args = request.query_params.getlist("args") if request.query_params else []
        if raw_args:
            return await dispatcher.dispatch(cmd.handler, request, *raw_args)

        # No args — call handler with request only
        return await dispatcher.dispatch(cmd.handler, request)
