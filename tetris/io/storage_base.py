from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class StorageBase(ABC):
    @abstractmethod
    def load_settings(self) -> Dict[str, Any]: ...
    @abstractmethod
    def save_settings(self, settings: Dict[str, Any]) -> None: ...

    @abstractmethod
    def load_highscores(self) -> List[Dict[str, Any]]: ...
    @abstractmethod
    def save_highscores(self, rows: List[Dict[str, Any]]) -> None: ...
