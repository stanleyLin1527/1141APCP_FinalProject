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
        
        # DAS (Delayed Auto Shift) support
        self.held_keys: Dict[int, float] = {}  # keycode -> time_held_ms
        self.das_delay = int(settings.get("das_delay", 170))  # Initial delay (ms)
        self.das_interval = int(settings.get("das_interval", 50))  # Repeat interval (ms)

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
        self.das_delay = int(self.settings.get("das_delay", 170))
        self.das_interval = int(self.settings.get("das_interval", 50))

    def map_event(self, ev: Any) -> Optional[Action]:
        if ev.type == pygame.KEYDOWN:
            action_name = self.keymap.get(ev.key)
            if action_name:
                # Reset the timer for this key
                self.held_keys[ev.key] = 0.0
                return Action(action_name)
        elif ev.type == pygame.KEYUP:
            # Clear timer when key is released
            if ev.key in self.held_keys:
                del self.held_keys[ev.key]
        return None
    
    def update(self, dt_ms: int) -> list[Action]:
        """Updates key timers and returns actions that should repeat"""
        actions = []
        for keycode in list(self.held_keys.keys()):
            self.held_keys[keycode] += dt_ms
            action_name = self.keymap.get(keycode)
            
            # Only left/right movement supports DAS
            if action_name in ["left", "right"]:
                time_held = self.held_keys[keycode]
                
                # Start repeating after delay
                if time_held >= self.das_delay:
                    # Calculate how many times to execute
                    time_after_delay = time_held - self.das_delay
                    repeat_count = int(time_after_delay / self.das_interval)
                    
                    if repeat_count > 0:
                        actions.append(Action(action_name))
                        # Reset timer, keeping remainder
                        self.held_keys[keycode] = self.das_delay + (time_after_delay % self.das_interval)
        
        return actions
