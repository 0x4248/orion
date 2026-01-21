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

from orion.core import manual

manual.manual_registry.register(
    name="echo",
    text="""
DESCRIPTION:
    Echo back the provided text.

USAGE:
    echo <text>

EXAMPLE:
    $ echo Hello, World!
    Hello, World!

ALIASES:
    none
"""
)