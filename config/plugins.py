"""
Plugin configuration for Orion.

Admins can toggle modules by adding entries to `ENABLED_MODULES` where the
key is the import path and the value is a boolean. This file is optional; if
absent or a module missing here, the default is to enable the module.
"""

# Example:
ENABLED_MODULES = {
    "orion.plugins.demo": False,
}

