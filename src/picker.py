import pygame
import src.utils as utils
import static.colors as colors
import static.settings as settings


class MenuOption:
    def __init__(self, option: str, width: int, height: int, pos: tuple, offset: int):
        self.option = option
        self.width = width
        self.height = height
        self.pos = pos
        self.offset = offset
        self.buffer = 20
        self.selected = False
    
    def render(self, screen: pygame.display) -> None:
        p = utils.add_twoples(self.pos, ((self.buffer+self.width)*self.offset, 0))
        r = pygame.rect.Rect(p[0], p[1], self.width, self.height)
        pygame.draw.rect(screen, colors.RED, r)


class Picker:
    def __init__(self, width: int, height: int, pos: tuple):
        self.width = width
        self.height = height
        self.pos = pos
        self.options = []
        self.options_size = settings.PICKER_OPTION_SIZE
        self.menu_open = False
        self._build_options(["ONE", "TWO", "THREE"])
    
    def render(self, screen: pygame.display) -> None:
        r = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        pygame.draw.rect(screen, colors.BLUE, r)
        if self.menu_open:
            self._render_menu_options(screen)

    def contains_click(self, pos: tuple, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            return (pos[0] >= self.pos[0] and
                    pos[0] <= self.pos[0]+self.width and
                    pos[1] >= self.pos[1] and
                    pos[1] <= self.pos[1]+self.width)

    def open_pick_menu(self) -> None:
        self.menu_open = True
    
    def close_pick_menu(self) -> None:
        self.menu_open = False

    # helpers

    def _build_options(self, options: list[str]) -> list[MenuOption]:
        for i in range(len(options)):
            self.options.append(self._build_option(options[i], self.options_size, self.options_size, i))
    
    def _build_option(self, option: str, width: int, height: int, offset: int) -> MenuOption:
        pos = utils.add_twoples(self.pos, (0, self.height))
        return MenuOption(option, width, height, pos, offset)
    
    def _render_menu_options(self, screen: pygame.display) -> None:
        if not self.menu_open:
            return
        for o in self.options:
            o.render(screen)

    def _pick_option(self, option: MenuOption) -> None:
        pass
