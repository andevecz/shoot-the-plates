# Audio menu test
from pyray import *

def draw_thick_horizontal_line(thickness : int, starting_posX : int, starting_posY : int, ending_posX : int, ending_posY : int, color : Color):
    for i in range(thickness):
        draw_line(starting_posX, starting_posY + i, ending_posX, ending_posY + i, color)

def draw_thick_table(thickness : int, posX : int, posY : int, sizeX : int, sizeY : int, color : Color):
    for i in range(thickness):
        draw_rectangle_lines(posX - i, posY - i, sizeX + i*2, sizeY + i*2, color)

def draw_volume_option():
    draw_thick_horizontal_line(6, width//2 - line_size//2, height//2, width//2 + line_size//2, height//2, BLACK)
    draw_texture(button, width//2 - line_size//2 + volume, height//2 - 30, WHITE)

init_window(1200, 800, "Hello")
set_target_fps(120)
line_size = 500
volume = 500

button = load_texture("sprites/options/square_sprite.png")
change_volume = False

while not window_should_close():
    width = get_screen_width()
    height = get_screen_height()
    mouse_position = get_mouse_position()

    button_position = [width//2 - line_size//2 + volume, height//2 - 30,60,60]

    if check_collision_point_rec(mouse_position, button_position):
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            change_volume = True
    if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT) and change_volume:
        volume = int(mouse_position.x - 385)
    if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
        change_volume = False

    if volume >= 500:
        volume = 500
    if volume <= 0:
        volume = 0

    begin_drawing()
    clear_background(WHITE)
    
    draw_volume_option()
    end_drawing()
close_window()