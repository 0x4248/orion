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

STYLE = """
<style>
html, body {
  background: #000000;
  color: #ffffff;
  margin: 0;
  padding: 0.5em;
}

* {
  font-size: 16px;
  font-family: "Departure Mono", monospace;
}

body {
  max-width: 800px;
  margin: auto;
}

a {
  color: #4da6ff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.header {
  margin-bottom: 0.5em;
}

hr {
  border: none;
  border-top: 1px solid #444;
  margin: 0.5em 0;
}

pre {
  white-space: pre-wrap;
}

input, textarea {
  background: #000000;
  color: #ffffff;
  border: 1px solid #444;
  font-family: monospace;
  padding: 0.2em;
  margin-bottom: 0.5em;
}

input[type=submit] {
  width: 100%;
  color: lime;
  font-weight: bold;
}

input[type=textline] {
  width: 100%;
}

label {
  font-weight: bold;
  text-transform: uppercase;
}


.grey-text {
  color: gray;
  font-style: italic;
}

.log-debug {
  color: gray;
}

.log-info {
  color: #4da6ff;
}
.log-warning {
  color: black;
  background-color: yellow;
}
.log-error {
  color: white;
  background-color: red;
}

.log-error-flash {
  background-color: red;
  color: white;
  padding-top: 0.5em;
  padding-bottom: 0.5em;
  animation: flash-text 1s infinite;
}

.flash {
  animation: flash-text 1s infinite;
}

@keyframes flash-text {
  0% { opacity: 1; }
  49% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 0; }
}

.error {
  background-color: red;
  color: white;
  padding-top: 0.5em;
  padding-bottom: 0.5em;
  animation: pulse_error 1s;
}

.error-flash {
  background-color: red;
  color: white;
  padding-top: 0.5em;
  padding-bottom: 0.5em;
  animation: flash-text 1s infinite;
}

@keyframes pulse_error {
  0% { background-color: #ff8f8f; }
  100% { background-color: red; }
}

.error strong {
  text-decoration: underline;
  text-align: center; 
}

textarea {
  width: 100%;
  height: 6em;
}

.center {
  text-align: center;
}

hr, input, textarea {
  border: 1px solid #fff;
}

a:focus, a:hover {
  background-color: #0044cc;
  color: #ffffff;
  border-radius: 0px;
  border: none;
  # dont add default html stuff
  outline: none;

}

input:focus, textarea:focus {
  outline: none;
  border: 1px solid #4da6ff;
}

input[type=submit]:focus , input[type=submit]:hover {
  border: 1px solid lime;
  animation: pulse 1s infinite;
}
@keyframes pulse {
  0% { border: 1px solid lime; }
  50% { border: 1px solid white; }
  100% { border: 1px solid lime; }
}
</style>
"""

SCRIPT = """
<script>
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.activeElement.blur();
    }

    if (event.key === 'F1') {
        const firstInput = document.querySelector('input, textarea');
        if (firstInput) {
            const commandName = firstInput.value.trim();
            if (commandName) {
                window.location.href = '/man/' + encodeURIComponent(commandName);
            }
        }
    }


    if (event.key === 'F2') {
        window.location.href = '/command';
    }

    if (event.target.tagName.toLowerCase() === 'input' || event.target.tagName.toLowerCase() === 'textarea') {
        return;
    }
    if (event.key === 'F4' || event.key === ',' || event.key === 'Backspace') {
        window.history.back();
    }
    if (event.key === '.') {
        const firstInput = document.querySelector('input, textarea');
        if (firstInput) {
            firstInput.focus();
        }
    }

    if (event.key === '`') {
        const homeLink = document.querySelector('a[href="/"]');
        if (homeLink) {
            homeLink.focus();
        }
    }

});
</script>
"""


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
