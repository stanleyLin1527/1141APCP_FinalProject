"""
Audio Manager
Supports playing sound effects and background music
"""
from __future__ import annotations
import pygame
from typing import Dict, Any, Optional
import os


class AudioManager:
    """Manages game sound effects and background music"""
    
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.music_volume = float(settings.get("music_volume", 0.5))
        self.sfx_volume = float(settings.get("sfx_volume", 0.5))
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
        except Exception:
            self.enabled = False
            return
        
        # Sound effect cache
        self.sfx_cache: Dict[str, pygame.mixer.Sound] = {}
        
        # Currently playing BGM
        self.current_bgm: Optional[str] = None
        
    def set_music_volume(self, volume: float) -> None:
        """Set background music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume: float) -> None:
        """Set sound effect volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def play_bgm(self, name: str, loop: bool = True) -> None:
        """
        Play background music
        name: Music filename (without path, will search in sounds/music/ directory)
        loop: Whether to loop playback
        """
        if not self.enabled or self.music_volume == 0:
            return
        
        if self.current_bgm == name and pygame.mixer.music.get_busy():
            return
        
        # Try multiple possible paths
        possible_paths = [
            os.path.join("sounds", "music", name),
            os.path.join("tetris", "audio", name),
            name  # Direct path
        ]
        
        music_path = None
        for path in possible_paths:
            if os.path.exists(path):
                music_path = path
                break
        
        if not music_path:
            return
        
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_bgm = name
        except Exception:
            pass
    
    def stop_bgm(self) -> None:
        """Stop background music"""
        if self.enabled:
            pygame.mixer.music.stop()
            self.current_bgm = None
    
    def pause_bgm(self) -> None:
        """Pause background music"""
        if self.enabled:
            pygame.mixer.music.pause()
    
    def unpause_bgm(self) -> None:
        """Resume background music"""
        if self.enabled:
            pygame.mixer.music.unpause()
    
    def play_sfx(self, name: str) -> None:
        """
        Play sound effect
        name: Sound effect filename (without path, will search in sounds/sfx/ directory)
        """
        if not self.enabled or self.sfx_volume == 0:
            return
        
        # Load from cache or create new Sound object
        if name not in self.sfx_cache:
            # Try multiple possible paths
            possible_paths = [
                os.path.join("sounds", "sfx", name),
                os.path.join("tetris", "audio", "tetris sfx", name),
                name  # Direct path
            ]
            
            sfx_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    sfx_path = path
                    break
            
            if not sfx_path:
                return
            
            try:
                sound = pygame.mixer.Sound(sfx_path)
                self.sfx_cache[name] = sound
            except Exception:
                return
        
        sound = self.sfx_cache[name]
        sound.set_volume(self.sfx_volume)
        sound.play()
    
    def shutdown(self) -> None:
        """Shut down audio system"""
        if self.enabled:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
