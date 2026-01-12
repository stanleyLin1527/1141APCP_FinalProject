from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
import pygame

@dataclass(frozen=True)
class Action:
    name: str

class InputController:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.keymap = self._build_keymap(settings.get("keymap", {}))

    def _build_keymap(self, keymap: Dict[str, str]) -> Dict[int, str]:
        out: Dict[int, str] = {}
        for action, key_name in keymap.items():
            try:
                keycode = pygame.key.key_code(key_name)
                out[keycode] = action
            except Exception:
                continue
        return out

    def refresh(self) -> None:
        self.keymap = self._build_keymap(self.settings.get("keymap", {}))

    def map_event(self, ev: Any) -> Optional[Action]:
        if ev.type == pygame.KEYDOWN:
            action_name = self.keymap.get(ev.key)
            if action_name:
                return Action(action_name)
        return None
