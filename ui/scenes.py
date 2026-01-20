from __future__ import annotations
from typing import Any, Dict, List, Optional
import random
import pygame

from tetris.ui.renderer_base import RendererBase
from tetris.ui.input_controller import InputController
from tetris.io.json_storage import JsonStorage
from tetris.core.board import Board
from tetris.core.vec2 import Vec2
from tetris.core.tetromino import Tetromino
from tetris.core.pieces import random_bag
from tetris.core.rules import score_for_lines, level_for_total_lines, drop_interval_ms, check_tspin
from tetris.utils.timer import DropTimer

class Scene:
    def __init__(self, manager: "SceneManager"):
        self.m = manager

    def handle_event(self, ev: Any) -> None:
        pass

    def update(self, dt_ms: int) -> None:
        pass

    def draw(self) -> None:
        pass

class SceneManager:
    def __init__(self, renderer: RendererBase, storage: JsonStorage, input_controller: InputController, audio_manager):
        self.renderer = renderer
        self.storage = storage
        self.input = input_controller
        self.audio = audio_manager
        self.scene: Scene | None = None
        self.running = True

    def set_scene(self, scene: Scene) -> None:
        self.scene = scene

    def quit(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            dt = self.renderer.tick()
            for ev in self.renderer.poll_events():
                if ev.type == pygame.QUIT:
                    self.running = False
                    break
                # F11 to toggle fullscreen
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                    self.renderer.toggle_fullscreen()
                if self.scene:
                    self.scene.handle_event(ev)
            if self.scene:
                self.scene.update(dt)
                self.scene.draw()

class MenuScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.player_name = str(self.m.storage.load_settings().get("player_name", "Player"))
        self.hint = ""
        self.highscores = self.m.storage.load_highscores()
        
        # Volume control
        settings = self.m.storage.load_settings()
        self.music_volume = float(settings.get("music_volume", 0.5))
        self.sfx_volume = float(settings.get("sfx_volume", 0.5))
        
        # Play menu music
        self.m.audio.play_bgm("tetoris.mp3")

    def handle_event(self, ev: Any) -> None:
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                settings = self.m.storage.load_settings()
                settings["player_name"] = self.player_name.strip() or "Player"
                settings["music_volume"] = self.music_volume
                settings["sfx_volume"] = self.sfx_volume
                self.m.storage.save_settings(settings)
                self.m.set_scene(GameScene(self.m))
                return
            if ev.key == pygame.K_ESCAPE:
                self.m.quit()
                return
            if ev.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
                return
            
            # Volume controls
            if ev.key == pygame.K_UP:
                # Increase music volume
                self.music_volume = min(1.0, self.music_volume + 0.1)
                self.m.audio.set_music_volume(self.music_volume)
                self.m.audio.play_sfx("SFX_ButtonUp.ogg")
                return
            if ev.key == pygame.K_DOWN:
                # Decrease music volume
                self.music_volume = max(0.0, self.music_volume - 0.1)
                self.m.audio.set_music_volume(self.music_volume)
                self.m.audio.play_sfx("SFX_ButtonUp.ogg")
                return
            if ev.key == pygame.K_RIGHT:
                # Increase SFX volume
                self.sfx_volume = min(1.0, self.sfx_volume + 0.1)
                self.m.audio.set_sfx_volume(self.sfx_volume)
                self.m.audio.play_sfx("SFX_ButtonUp.ogg")
                return
            if ev.key == pygame.K_LEFT:
                # Decrease SFX volume
                self.sfx_volume = max(0.0, self.sfx_volume - 0.1)
                self.m.audio.set_sfx_volume(self.sfx_volume)
                self.m.audio.play_sfx("SFX_ButtonUp.ogg")
                return

            ch = ev.unicode
            if ch and ch.isprintable() and len(self.player_name) < 16 and ch not in ["\r", "\n", "\t"]:
                self.player_name += ch

    def draw(self) -> None:
        self.m.renderer.draw_menu(self.player_name, self.hint, self.highscores, self.music_volume, self.sfx_volume)

class GameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.settings = self.m.storage.load_settings()
        self.rng = random.Random()

        self.board = Board(cols=10, rows=20)

        self.score = 0
        self.total_lines = 0
        self.level = 0

        self.paused = False

        self.bag: List[str] = []
        self.next_queue: List[str] = []
        self._fill_queue()

        self.active = self._spawn_piece()
        self.hold_kind: Optional[str] = None
        self.hold_locked = False  # Only allow hold once per piece from spawn to lock

        self.timer = DropTimer(drop_interval_ms(self.level))
        self.soft_drop_held = False
        
        # Track whether last action was a rotation (for T-spin detection)
        self.last_action_was_rotate = False
        
        # Play game music
        self.m.audio.play_bgm("tetoris.mp3")
        self.m.audio.play_sfx("SFX_GameStart.ogg")

        if not self.board.can_place(self.active):
            self._game_over()

    def _fill_queue(self) -> None:
        need = max(5, int(self.settings.get("next_count", 3)) + 2)
        while len(self.next_queue) < need:
            if not self.bag:
                self.bag = random_bag(self.rng)
            self.next_queue.append(self.bag.pop(0))

    def _spawn_piece(self, kind: Optional[str] = None) -> Tetromino:
        self._fill_queue()
        k = kind if kind is not None else self.next_queue.pop(0)
        self._fill_queue()

        pos = Vec2(self.board.cols // 2, 0)
        if k in ["I", "O"]:
            pos = Vec2(self.board.cols // 2 - 1, 0)
        return Tetromino(kind=k, pos=pos, rot=0)

    def _try_move(self, dx: int, dy: int) -> bool:
        np = self.active.pos + (dx, dy)
        if self.board.can_place(self.active, pos=np):
            self.active.pos = np
            # Movement resets rotation flag
            if dx != 0:  # Only horizontal movement resets
                self.last_action_was_rotate = False
                self.m.audio.play_sfx("SFX_PieceMoveLR.ogg")
            return True
        return False

    def _try_rotate(self, dir: int) -> bool:
        nr = self.active.rotated(dir)
        # Simple wall-kick
        kicks = [(0,0), (1,0), (-1,0), (2,0), (-2,0)]
        for kx, ky in kicks:
            np = self.active.pos + (kx, ky)
            if self.board.can_place(self.active, pos=np, rot=nr):
                self.active.pos = np
                self.active.rot = nr
                # Mark last action as rotation
                self.last_action_was_rotate = True
                self.m.audio.play_sfx("SFX_PieceRotateLR.ogg")
                return True
        return False

    def _hard_drop(self) -> None:
        while self._try_move(0, 1):
            pass
        self.m.audio.play_sfx("SFX_PieceHardDrop.ogg")
        self._lock_and_continue()

    def _lock_and_continue(self) -> None:
        # Detect T-spin
        is_tspin, is_mini = check_tspin(self.board, self.active, self.last_action_was_rotate)
        
        self.board.lock(self.active)
        cleared = self.board.clear_lines()
        
        if cleared:
            # Play line clear sound effect
            if is_tspin:
                if cleared == 3:
                    self.m.audio.play_sfx("SFX_SpecialTSpinTriple.ogg")
                elif cleared == 2:
                    self.m.audio.play_sfx("SFX_SpecialTSpinDouble.ogg")
                elif cleared == 1:
                    self.m.audio.play_sfx("SFX_SpecialTSpinSingle.ogg")
                else:
                    self.m.audio.play_sfx("SFX_SpecialTSpin.ogg")
            elif cleared == 4:
                self.m.audio.play_sfx("SFX_SpecialTetris.ogg")
            elif cleared == 3:
                self.m.audio.play_sfx("SFX_SpecialLineClearTriple.ogg")
            elif cleared == 2:
                self.m.audio.play_sfx("SFX_SpecialLineClearDouble.ogg")
            else:
                self.m.audio.play_sfx("SFX_SpecialLineClearSingle.ogg")
            
            old_level = self.level
            self.score += score_for_lines(cleared, self.level, is_tspin, is_mini)
            self.total_lines += cleared
            self.level = level_for_total_lines(self.total_lines)
            
            # Level up sound effect
            if self.level > old_level:
                self.m.audio.play_sfx("SFX_LevelUp.ogg")
            
            self.timer.set_interval(drop_interval_ms(self.level))

        self.active = self._spawn_piece()
        self.hold_locked = False
        self.last_action_was_rotate = False  # Reset rotation flag

        if not self.board.can_place(self.active):
            self._game_over()

    def _hold(self) -> None:
        if self.hold_locked:
            return

        cur_kind = self.active.kind
        if self.hold_kind is None:
            self.hold_kind = cur_kind
            self.active = self._spawn_piece()
        else:
            swap_kind = self.hold_kind
            self.hold_kind = cur_kind
            self.active = self._spawn_piece(kind=swap_kind)

        self.hold_locked = True
        self.last_action_was_rotate = False  # Reset rotation flag
        self.m.audio.play_sfx("SFX_PieceHold.ogg")
        
        if not self.board.can_place(self.active):
            self._game_over()

    def _ghost_cells(self) -> List[tuple[int,int]] | None:
        if not bool(self.settings.get("show_ghost", True)):
            return None
        p = self.active.pos
        while self.board.can_place(self.active, pos=p + (0, 1)):
            p = p + (0, 1)
        return [(c.x, c.y) for c in self.active.cells(pos=p)]

    def _game_over(self) -> None:
        self.m.audio.play_sfx("SFX_GameOver.ogg")
        settings = self.m.storage.load_settings()
        name = str(settings.get("player_name", "Player"))
        max_rows = int(settings.get("max_highscores", 10))
        highscores = self.m.storage.add_highscore(name=name, score=self.score, max_rows=max_rows)
        self.m.set_scene(GameOverScene(self.m, self.score, self.level, self.total_lines, highscores))

    def handle_event(self, ev: Any) -> None:
        if ev.type == pygame.KEYUP and ev.key == pygame.K_DOWN:
            self.soft_drop_held = False

        act = self.m.input.map_event(ev)
        if act is None:
            return

        self._process_action(act)

    def _process_action(self, act) -> None:
        if act.name == "back":
            self.m.set_scene(MenuScene(self.m))
            return

        if act.name == "pause":
            self.paused = not self.paused
            if self.paused:
                self.m.audio.pause_bgm()
            else:
                self.m.audio.unpause_bgm()
            return

        if self.paused:
            return

        if act.name == "left":
            self._try_move(-1, 0)
        elif act.name == "right":
            self._try_move(1, 0)
        elif act.name == "rotate":
            self._try_rotate(+1)
        elif act.name == "soft_drop":
            self.soft_drop_held = True
            self._try_move(0, 1)
        elif act.name == "hard_drop":
            self._hard_drop()
        elif act.name == "hold":
            self._hold()

    def update(self, dt_ms: int) -> None:
        if self.paused:
            return

        # Handle DAS (continuous movement)
        repeated_actions = self.m.input.update(dt_ms)
        for act in repeated_actions:
            self._process_action(act)

        if self.soft_drop_held:
            steps = max(1, dt_ms // 16)
            for _ in range(min(steps, 4)):
                if not self._try_move(0, 1):
                    self._lock_and_continue()
                    return

        if self.timer.tick(dt_ms):
            if not self._try_move(0, 1):
                self._lock_and_continue()

    def draw(self) -> None:
        ghost = self._ghost_cells()
        self.m.renderer.draw_game(
            board=self.board,
            active=self.active,
            ghost_cells=ghost,
            next_kinds=self.next_queue[: int(self.settings.get("next_count", 3))],
            hold_kind=self.hold_kind,
            score=self.score,
            level=self.level,
            total_lines=self.total_lines,
            paused=self.paused,
        )

class GameOverScene(Scene):
    def __init__(self, manager: SceneManager, score: int, level: int, total_lines: int, highscores: List[Dict[str, Any]]):
        super().__init__(manager)
        self.score = score
        self.level = level
        self.total_lines = total_lines
        self.highscores = highscores
        
        # Play game over music
        self.m.audio.play_bgm("tetoris.mp3", loop=False)

    def handle_event(self, ev: Any) -> None:
        act = self.m.input.map_event(ev)
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.m.set_scene(MenuScene(self.m))
            return
        if act and act.name == "restart":
            self.m.set_scene(GameScene(self.m))
            return

    def draw(self) -> None:
        self.m.renderer.draw_game_over(self.score, self.level, self.total_lines, self.highscores)
