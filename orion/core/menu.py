"""
Menu manager for Orion.

Plugins and modules can register menus and menu entries. Entries may be of
type `command` (references a registered command name) or `link` (external or
internal href). The MenuManager provides a small runtime API: `register`,
`append_entry`, and `get_menu`.
"""
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MenuEntry:
    def __init__(self, entry_id: str, label: str, kind: str = "link", target: str = "", meta: Optional[Dict[str, Any]] = None):
        self.id = entry_id
        self.label = label
        self.kind = kind  # 'link' or 'command'
        self.target = target
        self.meta = meta or {}

    def to_tuple(self, menu_id: str) -> tuple[str, str]:
        # Returns (label, href) suitable for page.menu rendering. Menu actions
        # are routed through /menu/{menu_id}/run/{entry_id}
        if self.kind == "link":
            return (self.label, self.target)
        # if args provided in meta, include them as repeated query params
        args = self.meta.get("args")
        if args and isinstance(args, (list, tuple)) and len(args) > 0:
            qs = "&".join(f"args={a}" for a in args)
            return (self.label, f"/menu/{menu_id}/run/{self.id}?{qs}")
        return (self.label, f"/menu/{menu_id}/run/{self.id}")


class Menu:
    def __init__(self, menu_id: str, title: str = "Menu"):
        self.id = menu_id
        self.title = title
        self.entries: List[MenuEntry] = []

    def add_entry(self, entry: MenuEntry) -> None:
        # ensure unique id
        if any(e.id == entry.id for e in self.entries):
            raise ValueError(f"Duplicate menu entry id: {entry.id}")
        self.entries.append(entry)

    def list_entries(self) -> List[MenuEntry]:
        return list(self.entries)


class MenuManager:
    def __init__(self):
        self._menus: Dict[str, Menu] = {}

    def register(self, menu_id: str, title: str = "Menu") -> Menu:
        if menu_id in self._menus:
            logger.info("Menu %s already registered", menu_id)
            return self._menus[menu_id]
        m = Menu(menu_id, title)
        self._menus[menu_id] = m
        logger.info("Registered menu %s", menu_id)
        return m

    def append_entry(self, menu_id: str, entry_id: str, label: str, kind: str = "link", target: str = "", meta: Optional[Dict[str, Any]] = None) -> MenuEntry:
        if menu_id not in self._menus:
            raise KeyError(f"Unknown menu: {menu_id}")
        entry = MenuEntry(entry_id, label, kind=kind, target=target, meta=meta)
        self._menus[menu_id].add_entry(entry)
        logger.info("Appended entry %s to menu %s", entry_id, menu_id)
        return entry

    def get_menu(self, menu_id: str) -> Optional[Menu]:
        return self._menus.get(menu_id)

    def list_menus(self) -> List[Menu]:
        return list(self._menus.values())


# singleton instance for importable API
manager = MenuManager()

__all__ = ["manager", "MenuManager", "Menu", "MenuEntry"]
