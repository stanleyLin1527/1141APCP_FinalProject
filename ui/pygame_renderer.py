from __future__ import annotations
import pygame
from typing import Any, Dict, List, Optional, Tuple

from tetris.ui.renderer_base import RendererBase
from tetris.core.board import Board
from tetris.core.tetromino import Tetromino
from tetris.core.pieces import PIECE_COLORS, PIECE_DEFS

class PygameRenderer(RendererBase):
    def __init__(self, settings: Dict[str, Any]):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.settings = settings

        self.cell = int(settings.get("cell_size", 40))
        self.cols, self.rows = 10, 20

        self.panel_w = self.cell * 7
        self.w = self.cell * self.cols + self.panel_w
        self.h = self.cell * self.rows

        # Check if fullscreen mode is enabled
        fullscreen = bool(settings.get("fullscreen", False))
        if fullscreen:
            self.screen = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        # Set up fonts
        try:
            self.font = pygame.font.Font('/game_font.otf', 20)
            self.font_big = pygame.font.Font('/game_font.otf', 48)
            self.font_small = pygame.font.Font('/game_font.otf', 16)
        except:
            self.font = pygame.font.Font(None, 20)
            self.font_big = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 16)

        self.bg = (20, 20, 30)
        self.grid_line = (50, 50, 60)
        self.panel_bg = (30, 30, 40)
        self.text_color = (240, 240, 250)
        self.is_fullscreen = fullscreen

    def tick(self) -> int:
        fps = int(self.settings.get("fps", 60))
        return int(self.clock.tick(fps))

    def poll_events(self) -> List[Any]:
        return pygame.event.get()

    def begin_frame(self) -> None:
        self.screen.fill(self.bg)
        pygame.draw.rect(self.screen, self.panel_bg, pygame.Rect(self.cell * self.cols, 0, self.panel_w, self.h))

    def end_frame(self) -> None:
        pygame.display.flip()

    def toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.w, self.h))
    
    def shutdown(self) -> None:
        pygame.quit()

    def _draw_text(self, text: str, x: int, y: int, big: bool = False, small: bool = False) -> None:
        if big:
            font = self.font_big
        elif small:
            font = self.font_small
        else:
            font = self.font
        surf = font.render(text, True, self.text_color)
        self.screen.blit(surf, (x, y))

    def _draw_cell(self, x: int, y: int, color: Tuple[int, int, int], inset: int = 2) -> None:
        r = pygame.Rect(x * self.cell, y * self.cell, self.cell, self.cell)
        pygame.draw.rect(self.screen, color, r.inflate(-inset, -inset))

    def _draw_board_grid(self) -> None:
        for y in range(self.rows):
            for x in range(self.cols):
                r = pygame.Rect(x * self.cell, y * self.cell, self.cell, self.cell)
                pygame.draw.rect(self.screen, self.grid_line, r, 1)

    def _draw_mini_piece(self, kind: str, oy: int) -> None:
        color = PIECE_COLORS[kind]
        offsets = PIECE_DEFS[kind][0]
        xs = [o.x for o in offsets]
        ys = [o.y for o in offsets]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        bw = maxx - minx + 1

        s = self.cell // 2
        ox = self.cell * self.cols
        cx = ox + (self.panel_w - bw * s) // 2
        cy = oy + 10

        for o in offsets:
            mx = cx + (o.x - minx) * s
            my = cy + (o.y - miny) * s
            pygame.draw.rect(self.screen, color, pygame.Rect(mx, my, s, s).inflate(-2, -2))

    def draw_menu(self, player_name: str, hint: str, highscores: List[Dict[str, Any]], 
                  music_volume: float = 0.5, sfx_volume: float = 0.5) -> None:
        self.begin_frame()
        
        # Title and instructions
        self._draw_text("TETRIS", 40, 30, big=True)
        self._draw_text("-" * 30, 40, 95)
        
        self._draw_text("Enter your name:", 40, 120)
        self._draw_text(f">> {player_name}_", 60, 155)
        
        self._draw_text("Controls:", 40, 210)
        self._draw_text("ENTER - Start Game", 60, 240, small=True)
        self._draw_text("ESC - Quit", 60, 260, small=True)
        
        # Volume section
        self._draw_text("Volume:", 40, 310)
        self._draw_text(f"Music (Up/Down): {int(music_volume * 100):3d}%", 60, 340, small=True)
        
        bar_width = 150
        bar_height = 16
        pygame.draw.rect(self.screen, (60, 60, 70), pygame.Rect(240, 340, bar_width, bar_height))
        pygame.draw.rect(self.screen, (100, 200, 100), pygame.Rect(240, 340, int(bar_width * music_volume), bar_height))
        pygame.draw.rect(self.screen, (150, 150, 160), pygame.Rect(240, 340, bar_width, bar_height), 1)
        
        self._draw_text(f"SFX (Left/Right): {int(sfx_volume * 100):3d}%", 60, 375, small=True)
        pygame.draw.rect(self.screen, (60, 60, 70), pygame.Rect(240, 375, bar_width, bar_height))
        pygame.draw.rect(self.screen, (100, 150, 200), pygame.Rect(240, 375, int(bar_width * sfx_volume), bar_height))
        pygame.draw.rect(self.screen, (150, 150, 160), pygame.Rect(240, 375, bar_width, bar_height), 1)
        
        if hint:
            self._draw_text(hint, 40, 425)

        # High scores panel on the right
        px = self.cell * self.cols + 30
        self._draw_text("HIGH SCORES", px, 30)
        self._draw_text("-" * 18, px, 65)
        y = 95
        for i, row in enumerate(highscores[:10], start=1):
            score_text = f"{i:2d}. {row['name']:<12} {row['score']:>8d}"
            self._draw_text(score_text, px, y, small=True)
            y += 25

        self.end_frame()

    def draw_game(
        self,
        board: Board,
        active: Tetromino,
        ghost_cells: List[Tuple[int, int]] | None,
        next_kinds: List[str],
        hold_kind: Optional[str],
        score: int,
        level: int,
        total_lines: int,
        paused: bool,
    ) -> None:
        self.begin_frame()
        self._draw_board_grid()

        for y in range(board.rows):
            for x in range(board.cols):
                c = board.grid[y][x]
                if c is not None:
                    self._draw_cell(x, y, c)

        if ghost_cells:
            for gx, gy in ghost_cells:
                self._draw_cell(gx, gy, (120, 120, 120), inset=10)

        for c in active.cells():
            self._draw_cell(c.x, c.y, active.color)

        px = self.cell * self.cols + 25
        
        # Stats section
        self._draw_text("SCORE", px, 25)
        self._draw_text(str(score), px, 55, big=True)
        
        self._draw_text("LEVEL", px, 115)
        self._draw_text(str(level), px, 145, big=True)
        
        self._draw_text("LINES", px, 205)
        self._draw_text(str(total_lines), px, 235, big=True)

        # Next section
        self._draw_text("NEXT", px, 295)
        y = 330
        for k in next_kinds[:3]:
            self._draw_mini_piece(k, y)
            y += 80

        # Hold section
        self._draw_text("HOLD", px, 570)
        if hold_kind:
            self._draw_mini_piece(hold_kind, 605)
        else:
            self._draw_text("(empty)", px, 610)

        # Controls at bottom
        self._draw_text("P: Pause  C: Hold", px, 710, small=True)
        self._draw_text("ESC: Menu", px, 730, small=True)

        if paused:
            overlay = pygame.Surface((self.cell * self.cols, self.h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))
            self._draw_text("PAUSED", self.cell * 3, self.cell * 9, big=True)

        self.end_frame()

    def draw_game_over(self, score: int, level: int, total_lines: int, highscores: List[Dict[str, Any]]) -> None:
        self.begin_frame()
        self._draw_text("GAME OVER", 40, 40, big=True)
        self._draw_text("─" * 30, 40, 105)
        
        self._draw_text(f"Final Score: {score}", 50, 150)
        self._draw_text(f"Level: {level}", 50, 190)
        self._draw_text(f"Lines: {total_lines}", 50, 230)
        
        self._draw_text("R - Restart  |  ESC - Menu", 50, 300)

        px = self.cell * self.cols + 30
        self._draw_text("HIGH SCORES", px, 40)
        self._draw_text("─" * 18, px, 75)
        y = 105
        for i, row in enumerate(highscores[:10], start=1):
            score_text = f"{i:2d}. {row['name']:<12} {row['score']:>8d}"
            self._draw_text(score_text, px, y, small=True)
            y += 25

        self.end_frame()
