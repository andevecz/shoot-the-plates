from pyray import *
import random

def center_text_x(text : str, font_size : int, screen_width : int) -> int:
    text_size = measure_text(text, font_size)
    return (screen_width - text_size)//2

def fullscreen_mode():
    if is_key_pressed(KeyboardKey.KEY_F11):
        if is_window_fullscreen():
            set_window_size(MIN_WIDTH, MIN_HEIGHT)
        else:
            set_window_size(INIT_SCREEN_WIDTH, INIT_SCREEN_HEIGHT)
        toggle_fullscreen()

# SCREEN OPTIONS
TITLE_SCREEN = 0
GAME_SCREEN = 1
PAUSE_SCREEN = 2
WIN_SCREEN = 3
LOST_SCREEN = 4

screen = TITLE_SCREEN

GRAVITY = 0.08
MAX_BALLS = 3

# TITLE
APPLICATION_NAME = "Shoot The Plates"

# TITLE_SCREEN
TITLE = "Shoot The Plates!"
MENU = ("Play", 
        "Quit",)
FULLSCREEN = "Press [F11] to toggle fullscreen."

# PAUSED_SCREEN
PAUSE = "Game Paused"
MENU_PAUSE = ("Resume",
              "Exit",)

# WIN_SCREEN
WIN_TITLE = "Congratulations, you have won!"

# LOST_SCREEN
LOST_TITLE = "YOU LOST!"
QUIT_TEXT = "Press [Esc] to go back to the menu."

# IMPORTANT VARIABLES

menu_items_coordinates = []
iterator = 0

add_ball = True
ball_list = []
score = 0

round = 1
ball_counter = 1

life = 10

set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)

init_window(0, 0, APPLICATION_NAME)
set_exit_key(KeyboardKey.KEY_NULL)
INIT_SCREEN_WIDTH = get_screen_width()
INIT_SCREEN_HEIGHT = get_screen_height()
MIN_WIDTH = int(INIT_SCREEN_WIDTH/1.2)
MIN_HEIGHT = int(INIT_SCREEN_HEIGHT/1.2)
set_window_min_size(MIN_WIDTH, MIN_HEIGHT)


set_window_position((INIT_SCREEN_WIDTH - MIN_WIDTH)//2, (INIT_SCREEN_HEIGHT - MIN_HEIGHT)//2)
set_target_fps(120)
toggle_fullscreen()

while not window_should_close():
    if not is_window_fullscreen():
        set_window_max_size(MIN_WIDTH, MIN_HEIGHT)

    screen_width = get_screen_width()
    screen_height = get_screen_height()
    mouse_position = get_mouse_position()

    text_size_multiplier = int(screen_height/67.5)

    title_size = text_size_multiplier * 4

    menu_size = text_size_multiplier * 3
    warning_size = text_size_multiplier * 2

    if screen == TITLE_SCREEN:
        title_x = center_text_x(TITLE, title_size, screen_width)
        begin_drawing()
        clear_background(RAYWHITE)

        draw_text(TITLE, title_x, screen_height//5, title_size, BLACK)
        
        for index, text in enumerate(MENU):
            startingX = center_text_x(text, menu_size, screen_width)
            startingY = (screen_height//5)*2 + iterator
            endingX = measure_text(text, menu_size)
            endingY = menu_size

            menu_items_coordinates.append([startingX, startingY, endingX, endingY])
            draw_text(text, menu_items_coordinates[index][0], menu_items_coordinates[index][1], menu_size, BLACK)
            iterator+=text_size_multiplier*5
        del startingX, startingY, endingX, endingY
        iterator = 0
        
        fullscreen_x = center_text_x(FULLSCREEN, warning_size, screen_width)
        draw_text(FULLSCREEN, fullscreen_x, (screen_height//5)*4, warning_size, BLACK)
                
        mouse_in_play = check_collision_point_rec(mouse_position, menu_items_coordinates[0])
        mouse_in_quit = check_collision_point_rec(mouse_position, menu_items_coordinates[1])

        if mouse_in_play or mouse_in_quit:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_POINTING_HAND)
            if mouse_in_play:
                draw_text(MENU[0], menu_items_coordinates[0][0], menu_items_coordinates[0][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
                    screen = GAME_SCREEN
            if mouse_in_quit:
                draw_text(MENU[1], menu_items_coordinates[1][0], menu_items_coordinates[1][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    break
        else:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
        end_drawing()
        menu_items_coordinates.clear()
        fullscreen_mode()
    
    if screen == GAME_SCREEN:
        score_string = f"Score: {score}"
        life_string = f"Life: {life}"
        score_x = center_text_x(score_string, warning_size, screen_width)

        begin_drawing()
        clear_background(RAYWHITE)
        
        draw_text(score_string, score_x, screen_height//10, warning_size, BLACK)
        draw_text(life_string, screen_width//10, screen_height//10, warning_size, BLACK)
        circle_speed_min = 8 if is_window_fullscreen() else 6
        circle_speed_max = 12 if is_window_fullscreen() else 10
        
        if add_ball:
            circle_random_X_position = random.randint(screen_width//8, screen_width*7//8)
            circle_random_radius = random.randint(20, 30)
            circle_random_color = random.choice((BLUE,RED,GREEN,YELLOW))
            circle_random_speed = random.randint(circle_speed_min, circle_speed_max)
            circle_initial_speed = circle_random_speed
            ball_list.append([circle_random_X_position, screen_height, circle_random_radius, circle_random_color, circle_random_speed, circle_initial_speed])
            
            if ball_counter % round:
                ball_counter += 1
            else:
                ball_counter = 1
                add_ball = False
        
        for index, ball in enumerate(ball_list):
            draw_circle(ball[0], ball[1], ball[2], ball[3])
            ball[1] = int(ball[1] - ball[4])
            ball[4] -= GRAVITY

            if ball[1] == screen_height:
                life -= 1
            # if ball[1] >= screen_height:
                ball[4] = ball[5]
            
            if check_collision_point_circle(mouse_position,(ball[0],ball[1]),ball[2]) and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                score+=1
                del ball_list[index]
        
        if not ball_list:
            if round != MAX_BALLS:
                round += 1
            add_ball = True

        end_drawing()

        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            screen = PAUSE_SCREEN

        if life <= 0:
            screen = LOST_SCREEN
        
        if score == 100:
            screen = WIN_SCREEN

    if screen == PAUSE_SCREEN:
        begin_drawing()
        clear_background(RAYWHITE)
        pause_x = center_text_x(PAUSE, title_size, screen_width)
        draw_text(PAUSE, pause_x, screen_height//5, title_size, BLACK)

        for index, text in enumerate(MENU_PAUSE):
            startingX = center_text_x(text, menu_size, screen_width)
            startingY = (screen_height//5)*2 + iterator
            endingX = measure_text(text, menu_size)
            endingY = menu_size

            menu_items_coordinates.append([startingX, startingY, endingX, endingY])
            draw_text(text, menu_items_coordinates[index][0], menu_items_coordinates[index][1], menu_size, BLACK)
            iterator+=text_size_multiplier*5
        del startingX, startingY, endingX, endingY
        iterator = 0

        mouse_in_resume = check_collision_point_rec(mouse_position, menu_items_coordinates[0])
        mouse_in_exit = check_collision_point_rec(mouse_position, menu_items_coordinates[1])

        if mouse_in_resume or mouse_in_exit:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_POINTING_HAND)
            if mouse_in_resume:
                draw_text(MENU_PAUSE[0], menu_items_coordinates[0][0], menu_items_coordinates[0][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
                    screen = GAME_SCREEN
            if mouse_in_exit:
                draw_text(MENU_PAUSE[1], menu_items_coordinates[1][0], menu_items_coordinates[1][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    add_ball = True
                    ball_list = []
                    score = 0
                    round = 1
                    ball_counter = 1
                    life = 10
                    screen = TITLE_SCREEN
        else:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)

        end_drawing()
    

    if screen == WIN_SCREEN:
        begin_drawing()
        clear_background(RAYWHITE)
        win_x = center_text_x(WIN_TITLE, title_size, screen_width)
        draw_text(WIN_TITLE, win_x, (screen_height//2 - title_size), title_size, GREEN)

        quit_x = center_text_x(QUIT_TEXT, warning_size, screen_width)
        draw_text(QUIT_TEXT, quit_x, (screen_height//5)*4, warning_size, BLACK)

        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            add_ball = True
            ball_list = []
            score = 0
            round = 1
            ball_counter = 1
            life = 10
            screen = TITLE_SCREEN

        end_drawing()

    if screen == LOST_SCREEN:
        final_score = f"Final score: {score}"
        begin_drawing()
        clear_background(RAYWHITE)
        lost_x = center_text_x(LOST_TITLE, title_size, screen_width)
        final_score_x = center_text_x(final_score, warning_size, screen_width)
        draw_text(LOST_TITLE, lost_x, (screen_height//2 - title_size), title_size, RED)
        draw_text(final_score, final_score_x, screen_height//2, warning_size, BLACK)

        quit_x = center_text_x(QUIT_TEXT, warning_size, screen_width)
        draw_text(QUIT_TEXT, quit_x, (screen_height//5)*4, warning_size, BLACK)

        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            add_ball = True
            ball_list = []
            score = 0
            round = 1
            ball_counter = 1
            life = 10
            screen = TITLE_SCREEN

        end_drawing()
close_window()