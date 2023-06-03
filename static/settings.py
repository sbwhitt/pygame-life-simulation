# window settings
# both settings have to be divisible by 20
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

# world settings
WORLD_SIZE = 2000

# ui settings
FONT_SIZE = 20
FONT_SIZE_BIGGER = 40
FONT_SIZE_SMALLER = 16

# menu options
ACTION_MENU_OPTIONS = {0: "Select", 1: "Create", 2: "Delete", 3: "Copy"}
COLOR_PICKER_OPTIONS = {0: "Red", 1: "Green", 2: "Blue"}
CHOOSER_OPTIONS = {0: "diseased", 1: "immune", 2: "immortal", 3: "immobile", 4: "sterile", 5: "unbindable"}

# input settings
LEFT_CLICK = 0
MIDDLE_CLICK = 1
RIGHT_CLICK = 2
SCROLL_IN = 4
SCROLL_OUT = 5
SCROLL_SPEED = 2

# clock settings
CLOCK_RATE = 60
METRONOME_RATE = 6

# entity settings
AGE_LENGTH = 2000
MOVE_INTERVAL = 50
DIR_INTERVAL = 700
# chances are 1/<value>
MUTATE_CHANCE = 75
DISEASE_SPREAD_CHANCE = 10
ENTITY_LIMIT = 10000
# must divide evenly into window height and width (5, 10, 20, 40...)
ENT_WIDTH = 20
DIRS = [(0, -ENT_WIDTH), (-ENT_WIDTH, 0),
        (0, ENT_WIDTH), (ENT_WIDTH, 0),
        (-ENT_WIDTH, -ENT_WIDTH), (-ENT_WIDTH, ENT_WIDTH),
        (ENT_WIDTH, ENT_WIDTH), (ENT_WIDTH, -ENT_WIDTH)]

# in game settings
IN_GAME_SETTINGS= {"MARK_DISEASED": 1, "LOGGING": 0, "HIGHLIGHT": 1}