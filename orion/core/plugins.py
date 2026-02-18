"""
Simple plugin loader for Orion.

This loader supports loading modules listed in `config.modules.MODULES` while
allowing enable/disable control from `config.plugins.ENABLED_MODULES` or by
allowing each module to be a dict with an `enabled` key. It keeps backwards
compatibility with the current list-of-strings format.

The loader imports enabled modules (so they can register themselves) and
exposes a small API to list what was attempted/loaded.
"""
from typing import Any, Dict, List, Optional
import importlib
import logging

logger = logging.getLogger(__name__)


class PluginInfo:
    def __init__(self, path: str, enabled: bool = True, meta: Optional[Dict[str, Any]] = None):
        self.path = path
        self.enabled = enabled
        self.meta = meta or {}
        self.loaded = False
        self.error: Optional[Exception] = None

    def __repr__(self) -> str:
        return f"PluginInfo(path={self.path!r}, enabled={self.enabled}, loaded={self.loaded})"


class PluginManager:
    def __init__(self, modules: List[Any], enabled_map: Optional[Dict[str, bool]] = None):
        # modules may be a list of strings or dicts with { 'path': ..., 'enabled': bool }
        self.modules = modules
        self.enabled_map = enabled_map or {}
        self.plugins: List[PluginInfo] = []

    def _normalize(self) -> None:
        self.plugins = []
        for entry in self.modules:
            if isinstance(entry, str):
                path = entry
                enabled = self.enabled_map.get(path, True)
                meta = {}
            elif isinstance(entry, dict):
                path = entry.get("path")
                enabled = entry.get("enabled", self.enabled_map.get(path, True))
                meta = {k: v for k, v in entry.items() if k not in ("path", "enabled")}
            else:
                continue
            self.plugins.append(PluginInfo(path=path, enabled=bool(enabled), meta=meta))

    def load_all(self) -> None:
        self._normalize()
        for p in self.plugins:
            if not p.enabled:
                logger.info("Skipping disabled plugin: %s", p.path)
                continue
            try:
                importlib.import_module(p.path)
                p.loaded = True
                logger.info("Loaded plugin: %s", p.path)
            except Exception as e:  # keep import errors local
                p.loaded = False
                p.error = e
                logger.exception("Error loading plugin %s: %s", p.path, e)

    def list(self) -> List[PluginInfo]:
        return list(self.plugins)


__all__ = ["PluginManager", "PluginInfo"]
