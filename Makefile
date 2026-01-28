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

PYTHON=python3

# HACK: If on macOS, use Homebrew Python path because 3.9 is not supported
ifeq ($(shell uname), Darwin)
	PYTHON=/opt/homebrew/bin/python3
endif


S := @

all:
	$(S)echo "MAKE: All"
	$(S)$(PYTHON) -m orion
	$(S)echo "MAKE: Server closed"
