import static.colors as colors
from static.settings import Settings as settings
from dataclasses import dataclass
from styles.styles import Style

@dataclass
class SidePanelStyle(Style):
    WIDTH = 240
    HEIGHT = settings.WINDOW_HEIGHT
    BORDER_WIDTH = 0
    ALPHA = 0

@dataclass
class PanelButtonStyle(Style):
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
    ALPHA = 200

@dataclass
class MiniMapStyle(Style):
    WIDTH = 240
    HEIGHT = 240
    COLOR = colors.WHITE

@dataclass
class MiniMapCursorStyle(Style):
    BORDER_WIDTH = 1
    ALPHA = 10

@dataclass
class BottomPanelStyle(Style):
    HEIGHT = 240
    WIDTH = settings.WINDOW_WIDTH-HEIGHT
    ALPHA = 200