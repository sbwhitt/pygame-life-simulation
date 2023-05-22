import pygame
import src.utils.utils as utils
import static.colors as colors
import static.settings as settings


class MenuOption:
    def __init__(self, option: str, width: int, height: int, pos: tuple):
        self.option = option
        self.width = width
        self.height = height
        self.pos = pos
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.selected = False
        self.font = self._init_font()
    
    def render(self, screen: pygame.display) -> None:
        if utils.within_rect(pygame.mouse.get_pos(), self.rect):
            pygame.draw.rect(screen, colors.RED, self.rect)
            pygame.draw.lines(screen, colors.BLACK, True, utils.get_rect_outline(self.rect), 2)
        else:
            utils.draw_rect_alpha(screen, utils.get_color_transparent(colors.RED, 200), self.rect)
        self._render_option_text(screen)
    
    # helpers
    
    def _init_font(self) -> pygame.font.Font:
        pygame.init()
        pygame.font.init()
        return pygame.font.Font(
            pygame.font.get_default_font(), settings.FONT_SIZE_SMALLER)

    def _render_option_text(self, screen: pygame.display) -> None:
        f = self.font.render(self.option, True, colors.BLACK)
        screen.blit(f, self.pos)


class Picker:
    def __init__(self, width: int, height: int, pos: tuple):
        self.width = width
        self.height = height
        self.pos = pos
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.options = []
        self.options_size = settings.PICKER_OPTION_SIZE
        self.menu_open = False
        self.margin = 20
        self.font = self._init_font()
        self.menu_title = "Actions"
        self._build_options([settings.ACTION_MENU_OPTIONS[0],
                             settings.ACTION_MENU_OPTIONS[1],
                             settings.ACTION_MENU_OPTIONS[2]])
        self.selected_option = None if len(self.options) < 1 else self.options[0]
    
    def render(self, screen: pygame.display) -> None:
        color = colors.GRAY
        if self._contains_mouse(pygame.mouse.get_pos()) or self.menu_open:
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.lines(screen, colors.BLACK, True, utils.get_rect_outline(self.rect), 2)
        else:
            color = utils.get_color_transparent(colors.GRAY, 200)
            utils.draw_rect_alpha(screen, color, self.rect, 3)
        self._render_menu_text(screen)
        if self.menu_open:
            self._render_menu_options(screen)

    def contains_click(self, pos: tuple, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            return utils.within_rect(pos, self.rect)
    
    def contains_option_click(self, pos: tuple, button: int) -> bool:
        if button == settings.LEFT_CLICK:
            o: MenuOption
            for o in self.options:
                if utils.within_rect(pos, o.rect):
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
        o: MenuOption
        for o in self.options:
            o.render(screen)
    
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
    
    def _contains_mouse(self, pos: tuple) -> bool:
        return (pos[0] >= self.pos[0] and
                pos[0] <= self.pos[0]+self.width and
                pos[1] >= self.pos[1] and
                pos[1] <= self.pos[1]+self.width)
