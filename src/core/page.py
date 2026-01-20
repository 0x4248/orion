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
from fastapi.responses import HTMLResponse
from core.layout import layout
from typing import Iterable, Sequence


# ============================================================================
# Core render primitive
# ============================================================================

def render(
    request: Request,
    *,
    title: str,
    body: str,
    buttons: Sequence[tuple[str, str]] | None = None,
    header: str | None = None,
) -> HTMLResponse:
    """
    Lowest-level page renderer.
    Everything funnels through this.
    """
    return HTMLResponse(layout(request, title, buttons, header, body))


# ============================================================================
# Navigation
# ============================================================================

DEFAULT_NAV: list[tuple[str, str]] = [
    ("HOME <span style='color:grey;'>`</span>", "/"),
    ("RUN <span style='color:grey;'>F2</span>", "/command"),
    ("UI", "/search_forms"),
    ("LOGOUT", "/logout"),
    ("EXIT <span style='color:grey;'>F4</span>", "/exit"),
]


def with_nav(
    buttons: Sequence[tuple[str, str]] | None = None,
) -> Sequence[tuple[str, str]]:
    return buttons if buttons is not None else DEFAULT_NAV


# ============================================================================
# Simple pages
# ============================================================================

def static(
    request: Request,
    title: str,
    html: str,
    *,
    buttons: Sequence[tuple[str, str]] | None = None,
):
    return render(
        request,
        title=title,
        body=html,
        buttons=with_nav(buttons),
    )


def message(
    request: Request,
    title: str,
    text: str = "",
    *,
    error: str | None = None,
    ok_href: str = "javascript:history.back()",
    center: bool = True,
    buttons: Sequence[tuple[str, str]] | None = None,
):
    err = (
        f"<pre class='error'><strong>ERROR:</strong>\n{error}</pre>"
        if error
        else ""
    )

    body = f"""
    {err}
    <div class='{'center' if center else ''}'>
      <pre>{text}</pre>
      <a href='{ok_href}' autofocus>[ OK ]</a>
    </div>
    """

    return render(
        request,
        title=title,
        body=body,
        buttons=with_nav(buttons),
    )


# ============================================================================
# Menus / lists
# ============================================================================

def menu(
    request: Request,
    title: str,
    entries: Iterable[tuple[str, str]],
    *,
    buttons: Sequence[tuple[str, str]] | None = None,
):
    lines = []
    first = True
    for label, href in entries:
        if first:
            lines.append(f"<a href='{href}' autofocus>[{label}]</a>")
            first = False
        else:
            lines.append(f"<a href='{href}'>[{label}]</a>")

    body = "<pre>" + "\n".join(lines) + "</pre>"

    return render(
        request,
        title=title,
        body=body,
        buttons=with_nav(buttons),
    )


def sectioned_menu(
    request: Request,
    title: str,
    sections: Iterable[tuple[str, Iterable[tuple[str, str]]]],
    *,
    buttons: Sequence[tuple[str, str]] | None = None,
):
    lines = []
    for section_title, entries in sections:
        lines.append(f"<strong>{section_title}</strong>")
        for label, href in entries:
            lines.append(f"<a href='{href}'>[{label}]</a>")
        lines.append("")

    body = "<pre>" + "\n".join(lines) + "</pre>"

    return render(
        request,
        title=title,
        body=body,
        buttons=with_nav(buttons),
    )


# ============================================================================
# Forms
# ============================================================================

def form(
    request: Request,
    title: str,
    action: str,
    fields: list[dict],
    error: str | None = None,
    msg: str | None = None,
):
    rows = []

    has_file = any(f.get("type") == "file" for f in fields)
    enctype = "multipart/form-data" if has_file else "application/x-www-form-urlencoded"

    for f in fields:
        name = f["name"]
        ftype = f.get("type", "text")

        if ftype == "textarea":
            rows.append(
                f"<label>{name}</label><br/>"
                f"<textarea name='{name}'></textarea>"
            )

        elif ftype == "checkbox":
            rows.append(
                f"<label>"
                f"<input type='checkbox' name='{name}' /> {name}"
                f"</label>"
            )

        elif ftype == "file":
            accept = f.get("accept")
            accept_attr = f" accept='{accept}'" if accept else ""
            rows.append(
                f"<label>{name}</label><br/>"
                f"<input type='file' name='{name}'{accept_attr} />"
            )

        else:
            rows.append(
                f"<label>{name}</label><br/>"
                f"<input name='{name}' type='{ftype}' />"
            )

    err = (
        f"<pre class='error'><strong>ERROR:</strong>\n{error}</pre>"
        if error else ""
    )

    body = f"""
    {err}
    {f"<pre class='msg'>{msg}</pre>" if msg else ""}
    <form method="post" action="{action}" enctype="{enctype}">
      {'<br/>'.join(rows)}
      <br/><input type="submit" value="SUBMIT" />
    </form>
    """
    return render(
        request,
        title=title,
        body=body,
        buttons=with_nav(),
    )


# ============================================================================
# Future-proof helpers (cheap, useful)
# ============================================================================

def redirect_notice(
    request: Request,
    title: str,
    text: str,
    href: str,
):
    """
    Message page that explains a redirect target.
    Useful for permissions, warnings, deprecations.
    """
    body = f"""
    <pre>{text}</pre>
    <a href='{href}' autofocus>[ CONTINUE ]</a>
    """
    return render(
        request,
        title=title,
        body=body,
        buttons=with_nav(),
    )


def empty(
    request: Request,
    title: str = "",
):
    """
    Placeholder page.
    Useful during development.
    """
    return render(
        request,
        title=title,
        body="",
        buttons=with_nav(),
    )
