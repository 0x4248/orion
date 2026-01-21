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

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any, Literal

Mode = Literal["cli", "ui", "both"]
ParseModes = Literal["shlex", "raw"]
@dataclass
class Command:
    name: str
    handler: Callable[..., Any]
    summary: str = ""
    mode: Mode = "cli"
    form_fields: List[Dict[str, Any]] = field(default_factory=list)
    parse_mode: ParseModes = "shlex"
    custom_attributes: Dict[str, Any] = field(default_factory=dict)

    def supports_cli(self) -> bool:
        return self.mode in ("cli", "both")

    def supports_ui(self) -> bool:
        return self.mode in ("ui", "both")
