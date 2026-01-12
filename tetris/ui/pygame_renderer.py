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
        pygame.display.set_caption("Tetris (Group Project)")
        self.settings = settings

        self.cell = int(settings.get("cell_size", 30))
        self.cols, self.rows = 10, 20

        self.panel_w = self.cell * 6
        self.w = self.cell * self.cols + self.panel_w
        self.h = self.cell * self.rows

        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)
        self.font_big = pygame.font.SysFont(None, 40)

        self.bg = (18, 18, 18)
        self.grid_line = (40, 40, 40)
        self.panel_bg = (24, 24, 24)
        self.text_color = (230, 230, 230)

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

    def shutdown(self) -> None:
        pygame.quit()

    def _draw_text(self, text: str, x: int, y: int, big: bool = False) -> None:
        surf = (self.font_big if big else self.font).render(text, True, self.text_color)
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

    def draw_menu(self, player_name: str, hint: str, highscores: List[Dict[str, Any]]) -> None:
        self.begin_frame()
        self._draw_text("TETRIS", 30, 20, big=True)
        self._draw_text("Enter：開始", 30, 80)
        self._draw_text("ESC：退出", 30, 110)
        self._draw_text("輸入玩家名（可直接打字、Backspace刪除）：", 30, 160)
        self._draw_text(f"> {player_name}", 30, 190)
        if hint:
            self._draw_text(hint, 30, 230)

        px = self.cell * self.cols + 20
        self._draw_text("High Scores (Top 10)", px, 20)
        y = 60
        for i, row in enumerate(highscores[:10], start=1):
            self._draw_text(f"{i:2d}. {row['name']:<10} {row['score']}", px, y)
            y += 24

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

        px = self.cell * self.cols + 20
        self._draw_text(f"Score: {score}", px, 20)
        self._draw_text(f"Level: {level}", px, 50)
        self._draw_text(f"Lines: {total_lines}", px, 80)

        self._draw_text("Next", px, 130)
        y = 150
        for k in next_kinds[:3]:
            self._draw_mini_piece(k, y)
            y += 90

        self._draw_text("Hold (C)", px, 420)
        if hold_kind:
            self._draw_mini_piece(hold_kind, 440)
        else:
            self._draw_text("(empty)", px, 450)

        self._draw_text("P：Pause", px, 560)
        self._draw_text("Space：Hard Drop", px, 584)
        self._draw_text("ESC：Menu", px, 608)

        if paused:
            overlay = pygame.Surface((self.cell * self.cols, self.h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))
            self._draw_text("PAUSED", self.cell * 3, self.cell * 9, big=True)

        self.end_frame()

    def draw_game_over(self, score: int, level: int, total_lines: int, highscores: List[Dict[str, Any]]) -> None:
        self.begin_frame()
        self._draw_text("GAME OVER", 30, 30, big=True)
        self._draw_text(f"Score: {score}", 30, 90)
        self._draw_text(f"Level: {level}", 30, 120)
        self._draw_text(f"Lines: {total_lines}", 30, 150)
        self._draw_text("R：Restart", 30, 200)
        self._draw_text("ESC：Menu", 30, 230)

        px = self.cell * self.cols + 20
        self._draw_text("High Scores (Top 10)", px, 20)
        y = 60
        for i, row in enumerate(highscores[:10], start=1):
            self._draw_text(f"{i:2d}. {row['name']:<10} {row['score']}", px, y)
            y += 24

        self.end_frame()
