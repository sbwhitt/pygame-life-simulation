import pygame
import static.colors as colors
import static.settings as settings
from src.window import Window


class MiniMap:
    def __init__(self):
        self.map_ratio = (settings.STATS_WIDTH / settings.WORLD_SIZE)
        self.map_edges = []
        self.cursor_width = 0
        self.cursor_height = 0
        self.cursor_edges = []

    def update(self, window: Window) -> None:
        self.cursor_width = int(window.width * self.map_ratio)
        self.cursor_height = int(window.height * self.map_ratio)
        self._build_map_edges(window)
        self._build_cursor_edges(window)

    def render(self, screen: pygame.display) -> None:
        self._render_map_border(screen)
        self._render_cursor(screen)
    
    def _render_map_border(self, screen: pygame.display) -> None:
        for l in self.map_edges:
            pygame.draw.lines(screen, colors.BLACK, True, l, 2)
    
    def _render_cursor(self, screen: pygame.display) -> None:
        for l in self.cursor_edges:
            pygame.draw.lines(screen, colors.BLACK, True, l, 1)
    
    def _build_map_edges(self, window: Window) -> None:
        # up left down right line segments
        self.map_edges = [
            (
                # top left point
                (window.width, window.height - settings.STATS_WIDTH),
                # top right point
                (window.width + settings.STATS_WIDTH, window.height - settings.STATS_WIDTH)
            ),
            (
                # top left point
                (window.width, window.height - settings.STATS_WIDTH),
                # bottom left point
                (window.width, window.height)
            ),
            (
                # bottom left point
                (window.width, window.height - 2),
                # bottom right point
                (window.width + settings.STATS_WIDTH, window.height + settings.STATS_WIDTH - 2)
            ),
            (
                # top right point
                (window.width + settings.STATS_WIDTH - 2, window.height - settings.STATS_WIDTH),
                # bottom right point
                (window.width + settings.STATS_WIDTH - 2, window.height + settings.STATS_WIDTH)
            )
        ]
    
    def _build_cursor_edges(self, window: Window) -> None:
        offset_x_adj = int(window.offset[0] * self.map_ratio)
        offset_y_adj = int(window.offset[1] * self.map_ratio)
        # up left down right line segments
        self.cursor_edges = [
            (
                # top left point
                (window.width + offset_x_adj, window.height - settings.STATS_WIDTH + offset_y_adj),
                # top right point
                (window.width + self.cursor_width + offset_x_adj, window.height - settings.STATS_WIDTH + offset_y_adj)
            ),
            (
                # top left point
                (window.width + offset_x_adj, window.height - settings.STATS_WIDTH + offset_y_adj),
                # bottom left point
                (window.width + offset_x_adj, window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj)
            ),
            (
                # bottom left point
                (window.width + offset_x_adj, window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj),
                # bottom right point
                (window.width + self.cursor_width + offset_x_adj, window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj)
            ),
            (
                # top right point
                (window.width + self.cursor_width + offset_x_adj, window.height - settings.STATS_WIDTH + offset_y_adj),
                # bottom right point
                (window.width + self.cursor_width + offset_x_adj, window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj)
            )
        ]
