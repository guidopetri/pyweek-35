import enum


screen_size = (1080, 720)
character_speed = 4

fontname = 'Arial'
fontsize = 32
font_color = '#303030'

dialog_border_color = 'blue'
dialog_box_color = 'yellow'

img_buffer = 2

# TODO: fix folder root
root = '..'
gfx_path = f"{root}/assets/gfx"
sfx_path = f"{root}/assets/fx"


class Modes(enum.Enum):

    MAIN_MENU = 0
    GAME = 1
