import pygame
import src.utils as utils
import static.colors as colors
import static.settings as settings


class MenuOption:
    def __init__(self, option: str, width: int, height: int, pos: tuple):
        self.option = option
        self.width = width
        self.height = height
        self.pos = pos
        self.selected = False
    
    def render(self, screen: pygame.display, font: pygame.font.Font) -> None:
        # p = utils.add_twoples(self.pos, ((self.buffer+self.width)*self.offset, 0))
        r = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        pygame.draw.rect(screen, colors.RED, r)
        self._render_option_text(screen, font)
    
    def _render_option_text(self, screen: pygame.display, font: pygame.font.Font) -> None:
        f = font.render(self.option, True, colors.BLACK)
        screen.blit(f, self.pos)


class Picker:
    def __init__(self, width: int, height: int, pos: tuple):
        self.width = width
        self.height = height
        self.pos = pos
        self.options = []
        self.options_size = settings.PICKER_OPTION_SIZE
        self.menu_open = False
        self.margin = 20
        self.font = self._init_font()
        self.menu_title = "Actions"
        self._build_options(["ONE", "TWO", "THREE"])
        self.selected_option = None if len(self.options) < 1 else self.options[0]
    
    def render(self, screen: pygame.display) -> None:
        r = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        pygame.draw.rect(screen, colors.BLUE, r)
        self._render_menu_text(screen)
        if self.menu_open:
            self._render_menu_options(screen)

    def contains_click(self, pos: tuple, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            return (pos[0] >= self.pos[0] and
                    pos[0] <= self.pos[0]+self.width and
                    pos[1] >= self.pos[1] and
                    pos[1] <= self.pos[1]+self.width)
    
    def contains_option_click(self, pos: tuple, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            o: MenuOption
            for o in self.options:
                if (pos[0] >= o.pos[0] and
                    pos[0] <= o.pos[0]+o.width and
                    pos[1] >= o.pos[1] and
                    pos[1] <= o.pos[1]+o.width):
                    self._pick_option(o)
                    return True
        return False

    def open_pick_menu(self) -> None:
        self.menu_open = True
    
    def close_pick_menu(self) -> None:
        self.menu_open = False

    # helpers

    def _init_font(self) -> pygame.font.Font:
        pygame.init()
        pygame.font.init()
        return pygame.font.Font(
            pygame.font.get_default_font(), settings.FONT_SIZE)
    
    def _render_menu_options(self, screen: pygame.display) -> None:
        if not self.menu_open:
            return
        for o in self.options:
            o.render(screen, self.font)
    
    def _render_menu_text(self, screen: pygame.display) -> None:
        f = self.font.render(self.menu_title, True, colors.BLACK)
        screen.blit(f, self.pos)
        f = self.font.render(self.selected_option.option, True, colors.BLACK)
        screen.blit(f, utils.add_twoples(self.pos, (0, settings.FONT_SIZE)))

    def _build_options(self, options: list[str]) -> list[MenuOption]:
        for i in range(len(options)):
            self.options.append(self._build_option(options[i], self.options_size, self.options_size, i))
    
    def _build_option(self, option: str, width: int, height: int, offset: int) -> MenuOption:
        p1 = utils.add_twoples(self.pos, (self.width+self.margin, int(self.margin/2)))
        pos = utils.add_twoples(p1, ((self.margin+self.width)*offset, 0))
        return MenuOption(option, width, height, pos)

    def _pick_option(self, option: MenuOption) -> None:
        self.selected_option = option
