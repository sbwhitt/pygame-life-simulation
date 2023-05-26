from dataclasses import dataclass
import static.colors as colors
import static.settings as settings

@dataclass
class Style:
    WIDTH = 0
    HEIGHT = 0
    COLOR = colors.WHITE
    FONT_COLOR = colors.BLACK
    BORDER_COLOR = colors.BLACK
    BORDER_WIDTH = 2
    MARGIN = (0, 0)
    ALPHA = 200

@dataclass
class MouseCursorStyle(Style):
    WIDTH = settings.ENT_WIDTH
    HEIGHT = settings.ENT_WIDTH
    BORDER_WIDTH = 1
    ALPHA = 0

@dataclass
class SidePanelStyle(Style):
    WIDTH = 240
    HEIGHT = settings.WINDOW_HEIGHT
    BORDER_WIDTH = 0
    ALPHA = 0

@dataclass
class SidePanelButtonStyle(Style):
    WIDTH = 40
    HEIGHT = 40
    COLOR = colors.RED
    BORDER_WIDTH = 2
    ALPHA = 100

@dataclass
class StatsPanelStyle(Style):
    WIDTH = 240
    HEIGHT = settings.WINDOW_HEIGHT
    COLOR = colors.WHITE

@dataclass
class PickerMenuOptionStyle(Style):
    WIDTH = 80
    HEIGHT = 80
    COLOR = colors.RED
    MARGIN = (10, 10)

@dataclass
class PickerMenuStyle(Style):
    WIDTH = 100
    HEIGHT = 100
    COLOR = colors.GRAY
    MARGIN = (10, 10)

@dataclass
class MiniMapStyle(Style):
    WIDTH = 240
    HEIGHT = 240
    COLOR = colors.WHITE

@dataclass
class MiniMapCursorStyle(Style):
    BORDER_WIDTH = 1
    ALPHA = 10