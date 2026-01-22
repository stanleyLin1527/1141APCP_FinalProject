from __future__ import annotations
import json
import os
from typing import Any, Dict, List
from datetime import datetime

from tetris.errors.exceptions import ConfigError, SaveFileError, CorruptedDataError
from tetris.io.storage_base import StorageBase

DEFAULT_SETTINGS: Dict[str, Any] = {
    "cell_size": 30,
    "fps": 60,
    "music_volume": 0.0,
    "sfx_volume": 0.0,

    "player_name": "Player",

    "keymap": {
        "left": "LEFT",
        "right": "RIGHT",
        "rotate": "UP",
        "soft_drop": "DOWN",
        "hard_drop": "SPACE",
        "hold": "c",
        "pause": "p",
        "back": "ESCAPE",
        "restart": "r",
    },

    "show_ghost": True,
    "next_count": 3,
    "max_highscores": 10,
}

class JsonStorage(StorageBase):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.settings_path = os.path.join(self.data_dir, "settings.json")
        self.highscores_path = os.path.join(self.data_dir, "highscores.json")
        os.makedirs(self.data_dir, exist_ok=True)

    def load_settings(self) -> Dict[str, Any]:
        if not os.path.exists(self.settings_path):
            self.save_settings(dict(DEFAULT_SETTINGS))
            return dict(DEFAULT_SETTINGS)

        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise CorruptedDataError(f"settings.json parse failed：{e}") from e
        except OSError as e:
            raise SaveFileError(f"read settings.json failed：{e}") from e

        merged = dict(DEFAULT_SETTINGS)
        merged.update(data if isinstance(data, dict) else {})
        if isinstance(data, dict) and "keymap" in data and isinstance(data["keymap"], dict):
            merged["keymap"] = dict(DEFAULT_SETTINGS["keymap"])
            merged["keymap"].update(data["keymap"])
        return merged

    def save_settings(self, settings: Dict[str, Any]) -> None:
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise SaveFileError(f"write settings.json failed：{e}") from e

    def load_highscores(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.highscores_path):
            self.save_highscores([])
            return []

        try:
            with open(self.highscores_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise CorruptedDataError(f"highscores.json parse failed：{e}") from e
        except OSError as e:
            raise SaveFileError(f"read highscores.json failed：{e}") from e

        if not isinstance(data, list):
            raise ConfigError("highscores.json format is invalid (should be a list)")

        rows: List[Dict[str, Any]] = []
        for row in data:
            if not isinstance(row, dict):
                continue
            name = str(row.get("name", "Player"))[:24]
            score = int(row.get("score", 0))
            ts = str(row.get("time", ""))
            rows.append({"name": name, "score": score, "time": ts})
        rows.sort(key=lambda r: r["score"], reverse=True)
        return rows

    def save_highscores(self, rows: List[Dict[str, Any]]) -> None:
        try:
            with open(self.highscores_path, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise SaveFileError(f"write highscores.json failed：{e}") from e

    def add_highscore(self, name: str, score: int, max_rows: int) -> List[Dict[str, Any]]:
        rows = self.load_highscores()
        rows.append({
            "name": str(name)[:24],
            "score": int(score),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        rows.sort(key=lambda r: r["score"], reverse=True)
        rows = rows[:max_rows]
        self.save_highscores(rows)
        return rows
