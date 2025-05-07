from pyray import *
import ctypes

def get_resolution() -> int:
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

def center_text_x(text : str, font_size : int, screen_width : int) -> int:
    text_size = measure_text(text, font_size)
    return (screen_width - text_size)//2
    
# HEADER
SCREEN_WIDTH, SCREEN_HEIGHT = get_resolution()
APPLICATION_NAME = "Shoot The Plates"
TEXT_SIZE_CONSTANT = int(SCREEN_HEIGHT/67.5)

# TITLE_SCREEN
TITLE = "Shoot The Plates!"
TITLE_SIZE = TEXT_SIZE_CONSTANT * 4

MENU = ("Play", 
        "Quit",)
MENU_SIZE = TEXT_SIZE_CONSTANT * 3

# IMPORTANT VARIABLES

menu_items_coordinates = []
iterator = 0

init_window(0, 0, APPLICATION_NAME)
title_x = center_text_x(TITLE, TITLE_SIZE, SCREEN_WIDTH)
toggle_fullscreen()

while not window_should_close():
    begin_drawing()
    clear_background(WHITE)

    draw_text(TITLE, title_x, SCREEN_HEIGHT//5, TITLE_SIZE, BLACK)
    for text in MENU:
        startingX = center_text_x(text, MENU_SIZE, SCREEN_WIDTH)
        startingY = (SCREEN_HEIGHT//5)*2 + iterator
        endingX = measure_text(text, MENU_SIZE)
        endingY = MENU_SIZE
        menu_items_coordinates.append((startingX, startingY, endingX, endingY,))
        draw_text(text, startingX, startingY, MENU_SIZE, BLACK)
        iterator+=TEXT_SIZE_CONSTANT*5
    del startingX, startingY, endingX, endingY
    iterator = 0

    mouse_position = get_mouse_position()

    if check_collision_point_rec(mouse_position, menu_items_coordinates[0]):
        draw_text(MENU[0], menu_items_coordinates[0][0], menu_items_coordinates[0][1], MENU_SIZE, GRAY)
        set_mouse_cursor(MouseCursor.MOUSE_CURSOR_POINTING_HAND)

    if check_collision_point_rec(mouse_position, menu_items_coordinates[1]):
        draw_text(MENU[1], menu_items_coordinates[1][0], menu_items_coordinates[1][1], MENU_SIZE, GRAY)
        set_mouse_cursor(MouseCursor.MOUSE_CURSOR_POINTING_HAND)
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            break
    else:
        set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
    end_drawing()  
close_window()