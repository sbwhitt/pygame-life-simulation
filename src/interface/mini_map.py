import pygame
import static.colors as colors
import static.settings as settings
from src.window import Window
from src.entities.entity import Entity


class MiniMap:
    def __init__(self, screen: pygame.display, window: Window):
        self.screen = screen
        self.window = window
        self.map_ratio = (settings.STATS_WIDTH / settings.WORLD_SIZE)
        self.map_edges = []
        self.cursor_width = 0
        self.cursor_height = 0
        self.cursor_edges = []

    def update(self) -> None:
        self.cursor_width = int(self.window.width * self.map_ratio)
        self.cursor_height = int(self.window.height * self.map_ratio)
        self._build_map_edges()
        self._build_cursor_edges()

    def render(self, entities: list[Entity]) -> None:
        self._render_small_entities(entities)
        self._render_map_border()
        self._render_cursor()
    
    def _render_map_border(self) -> None:
        for l in self.map_edges:
            pygame.draw.lines(self.screen, colors.BLACK, True, l, 2)
    
    def _render_cursor(self) -> None:
        for l in self.cursor_edges:
            pygame.draw.lines(self.screen, colors.BLACK, True, l, 1)
    
    def _render_small_entities(self, entities: list[Entity]) -> None:
        for e in entities:
            copy = e.rect.copy()
            adj_left_top = (copy.left * self.map_ratio + self.window.width , copy.top * self.map_ratio + (self.window.height - settings.STATS_WIDTH))
            # copy.scale_by(self.map_ratio, self.map_ratio)
            copy.update(adj_left_top, (copy.width * self.map_ratio, copy.height * self.map_ratio))
            if e.dna.diseased and settings.IN_GAME_SETTINGS["MARK_DISEASED"]:
                pygame.draw.rect(self.screen, colors.BLACK,
                                 copy, border_radius=0)
            else:
                pygame.draw.rect(self.screen, e.dna.color, 
                                 copy, border_radius=0)
    
    def _build_map_edges(self) -> None:
        # up left down right line segments
        self.map_edges = [
            (
                # top left point
                (self.window.width, self.window.height - settings.STATS_WIDTH),
                # top right point
                (self.window.width + settings.STATS_WIDTH, self.window.height - settings.STATS_WIDTH)
            ),
            (
                # top left point
                (self.window.width, self.window.height - settings.STATS_WIDTH),
                # bottom left point
                (self.window.width, self.window.height)
            ),
            (
                # bottom left point
                (self.window.width, self.window.height - 2),
                # bottom right point
                (self.window.width + settings.STATS_WIDTH, self.window.height + settings.STATS_WIDTH - 2)
            ),
            (
                # top right point
                (self.window.width + settings.STATS_WIDTH - 2, self.window.height - settings.STATS_WIDTH),
                # bottom right point
                (self.window.width + settings.STATS_WIDTH - 2, self.window.height + settings.STATS_WIDTH)
            )
        ]
    
    def _build_cursor_edges(self) -> None:
        offset_x_adj = int(self.window.offset[0] * self.map_ratio)
        offset_y_adj = int(self.window.offset[1] * self.map_ratio)
        # up left down right line segments
        self.cursor_edges = [
            (
                # top left point
                (self.window.width + offset_x_adj, self.window.height - settings.STATS_WIDTH + offset_y_adj),
                # top right point
                (self.window.width + self.cursor_width + offset_x_adj, self.window.height - settings.STATS_WIDTH + offset_y_adj)
            ),
            (
                # top left point
                (self.window.width + offset_x_adj, self.window.height - settings.STATS_WIDTH + offset_y_adj),
                # bottom left point
                (self.window.width + offset_x_adj, self.window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj)
            ),
            (
                # bottom left point
                (self.window.width + offset_x_adj, self.window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj),
                # bottom right point
                (self.window.width + self.cursor_width + offset_x_adj, self.window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj)
            ),
            (
                # top right point
                (self.window.width + self.cursor_width + offset_x_adj, self.window.height - settings.STATS_WIDTH + offset_y_adj),
                # bottom right point
                (self.window.width + self.cursor_width + offset_x_adj, self.window.height - settings.STATS_WIDTH + self.cursor_height + offset_y_adj)
            )
        ]
