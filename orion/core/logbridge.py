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

import logging

class logBridge(logging.Handler):
    def __init__(self, orionLoggerBridge):
        super().__init__()
        self.orionLoggerBridge = orionLoggerBridge

    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
            self.orionLoggerBridge.log(
                f"BRIDGE -> {record.name}.{record.funcName}()",
                msg,
                record.levelname,
            )
        except Exception:
            self.handleError(record)
