from dataclasses import dataclass
from pygame import Color
import static.colors as colors

@dataclass
class Style:
    WIDTH = 0
    HEIGHT = 0
    COLOR = colors.BLACK
    BORDER_COLOR = colors.BLACK
    BORDER_WIDTH = 2
    MARGIN = (0, 0)
    ALPHA = 200

@dataclass
class PickerMenuOptionStyle(Style):
    WIDTH = 80
    HEIGHT = 80
    COLOR = colors.RED
    MARGIN = (20, 10)

@dataclass
class PickerMenuStyle(Style):
    WIDTH = 100
    HEIGHT = 100
    COLOR = colors.GRAY
    MARGIN = (0, 0)