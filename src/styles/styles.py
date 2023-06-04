from dataclasses import dataclass
import static.colors as colors
from static.settings import Settings as settings

@dataclass
class Style:
    WIDTH = 0
    HEIGHT = 0
    COLOR = colors.WHITE
    FONT_COLOR = colors.BLACK
    BORDER_COLOR = colors.BLACK
    BORDER_WIDTH = 2
    MARGIN = (0, 0)
    ALPHA = 100

@dataclass
class MouseCursorStyle(Style):
    WIDTH = settings.ENT_WIDTH
    HEIGHT = settings.ENT_WIDTH
    BORDER_WIDTH = 1
    ALPHA = 0

@dataclass
class ActionMenuOptionStyle(Style):
    WIDTH = 80
    HEIGHT = 80
    MARGIN = (40, 40)

@dataclass
class ActionMenuStyle(Style):
    WIDTH = 240
    HEIGHT = 240

@dataclass
class ColorPickerStyle(Style):
    WIDTH = 80
    HEIGHT = 60
    MARGIN = (20, 20)

@dataclass
class ColorPickerOptionStyle(Style):
    WIDTH = 80
    HEIGHT = 40
    COLOR = colors.GRAY
    MARGIN = (0, 10)

@dataclass
class CheckboxStyle(Style):
    WIDTH = 20
    HEIGHT = 20

@dataclass
class ChooserStyle(Style):
    WIDTH = 20
    HEIGHT = 20
    MARGIN = (20, 20)