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

def draw_heart(heart_list: list, screen_width : int, screen_height : int):
    i = 0
    scale = 1.2
    for heart in heart_list:
        draw_texture_ex(heart, (screen_width//10 + i, screen_height//10),0,scale, WHITE)
        i+=int(45*scale)

def draw_thick_table(thickness : int, posX : int, posY : int, sizeX : int, sizeY : int, color : Color):
    for i in range(thickness):
        draw_rectangle_lines(posX - i, posY - i, sizeX + i*2, sizeY + i*2, color)

def draw_thick_vertical_line(thickness : int, starting_posX : int, starting_posY : int, ending_posX : int, ending_posY : int, color : Color):
    for i in range(thickness):
        draw_line(starting_posX + i, starting_posY, ending_posX + i, ending_posY, color)

def draw_thick_horizontal_line(thickness : int, starting_posX : int, starting_posY : int, ending_posX : int, ending_posY : int, color : Color):
    for i in range(thickness):
        draw_line(starting_posX, starting_posY + i, ending_posX, ending_posY + i, color)

# SCREEN OPTIONS
TITLE_SCREEN = 0
GAME_SCREEN = 1
PAUSE_SCREEN = 2
WIN_SCREEN = 3
LOST_SCREEN = 4
OPTIONS_SCREEN = 5

screen = TITLE_SCREEN

GRAVITY = 0.08

# TITLE
APPLICATION_NAME = "Shoot The Plates"

# TITLE_SCREEN
TITLE = "Shoot The Plates!"
MENU = ("Play",
        "Options", 
        "Quit",)
FULLSCREEN = "Press [F11] to toggle fullscreen."

# OPTIONS_SCREEN
enable_plate_rotation = False
enable_golden_plate = True
enable_insane_mode = False

change_master_button = False
change_music_button = False
change_effects_button = False

MENU_OPTIONS = ("Game options",
        "Audio",
        "",
        "Return",)

GAME_OPTIONS = ("Enable plate rotation",
                "Enable golden plate",
                "Insane mode",)

AUDIO_OPTIONS = ("Master volume",
                 "Music volume",
                 "Effects volume",)

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
game_options_coordinates = []

mouse_in_plate_rotation = False
mouse_in_golden_plate = False
mouse_in_insane_mode = False

mouse_in_master_volume = False
mouse_in_music_volume = False
mouse_in_effects_volume = False

iterator = 0

add_ball = True
ball_list = []
ball_deletion_list = []
score = 0

round = 1
ball_counter = 1

deltha_time = 0

draw_game_options = False
draw_audio_options = False

line_size = 500
volume = line_size

volume_master = volume
volume_music = volume
volume_effects = volume

# SPRITE VARIABLES
sprite_iterator = 200
sprite_position_size = []

set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)

init_window(0, 0, APPLICATION_NAME)
init_audio_device()

sprites = load_texture("sprites/plates/sprites.png")
heart = load_texture("sprites/heart/heart.png")
golden_heart = load_texture("sprites/heart/golden_heart.png")
truth_symbol = load_texture("sprites/options/true.png")
life_list = [heart for _ in range(5)]
audio_button = load_texture("sprites/options/square_sprite.png")

breaking_sound_1 = load_sound("sound/breaking_glass/1.wav")
breaking_sound_2 = load_sound("sound/breaking_glass/2.wav")
pop_sound = load_sound("sound/heart_pop/pop.wav")

music_1 = load_music_stream("music/killing_time.mp3")
set_music_volume(music_1, 1.0)
play_music_stream(music_1)

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

    window_time = get_time()
    window_fps = get_fps()
    current_frame = window_time * window_fps
    update_music_stream(music_1)

    if enable_insane_mode:
        max_balls = 10
    else:
        max_balls = 3

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
        mouse_in_quit = check_collision_point_rec(mouse_position, menu_items_coordinates[2])
        mouse_in_options = check_collision_point_rec(mouse_position, menu_items_coordinates[1])

        if mouse_in_play or mouse_in_quit or mouse_in_options:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_POINTING_HAND)
            if mouse_in_play:
                draw_text(MENU[0], menu_items_coordinates[0][0], menu_items_coordinates[0][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
                    screen = GAME_SCREEN
            if mouse_in_options:
                draw_text(MENU[1], menu_items_coordinates[1][0], menu_items_coordinates[1][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
                    screen = OPTIONS_SCREEN
            if mouse_in_quit:
                draw_text(MENU[2], menu_items_coordinates[2][0], menu_items_coordinates[2][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    break
        else:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
        end_drawing()
        menu_items_coordinates.clear()
        fullscreen_mode()
    
    if screen == OPTIONS_SCREEN:
        begin_drawing()
        clear_background(RAYWHITE)

        draw_thick_table(4,screen_width//5, screen_height//10, 3*screen_width//5, 4*screen_height//5, BLACK)
        draw_thick_vertical_line(4, 2*screen_width//5, screen_height//10, 2*screen_width//5, 9*screen_height//10, BLACK)

        for line_iterator in range(3):
            draw_thick_horizontal_line(4, screen_width//5,3*screen_height//10 + line_iterator*screen_height//5, 2*screen_width//5, 3*screen_height//10 + line_iterator*screen_height//5, BLACK)

        for index, text in enumerate(MENU_OPTIONS):
            startingX = center_text_x(text, menu_size, 2*screen_width//5) + screen_width//10
            startingY = (screen_height//5) - (menu_size//2) + iterator
            endingX = measure_text(text, menu_size)
            endingY = menu_size

            menu_items_coordinates.append([startingX, startingY, endingX, endingY])
            draw_text(text, menu_items_coordinates[index][0], menu_items_coordinates[index][1], menu_size, BLACK)
            iterator+=screen_height//5
        del startingX, startingY, endingX, endingY
        iterator = 0

        mouse_in_game_options = check_collision_point_rec(mouse_position, menu_items_coordinates[0])
        mouse_in_audio_options = check_collision_point_rec(mouse_position, menu_items_coordinates[1])
        mouse_in_resume = check_collision_point_rec(mouse_position, menu_items_coordinates[3])

        mouse_options_pointing_hand = (mouse_in_game_options or mouse_in_audio_options or mouse_in_resume or mouse_in_plate_rotation or mouse_in_golden_plate or mouse_in_insane_mode or mouse_in_master_volume or mouse_in_music_volume or mouse_in_effects_volume)


        if mouse_options_pointing_hand:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_POINTING_HAND)
            if mouse_in_game_options:
                draw_text(MENU_OPTIONS[0], menu_items_coordinates[0][0], menu_items_coordinates[0][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
                    draw_audio_options = False
                    draw_game_options = True
            if mouse_in_audio_options:
                draw_text(MENU_OPTIONS[1], menu_items_coordinates[1][0], menu_items_coordinates[1][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
                    draw_game_options = False
                    draw_audio_options = True
            if mouse_in_resume:
                draw_text(MENU_OPTIONS[3], menu_items_coordinates[3][0], menu_items_coordinates[3][1], menu_size, GRAY)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
                    draw_game_options = False
                    draw_audio_options = False
                    screen = TITLE_SCREEN
        else:
            set_mouse_cursor(MouseCursor.MOUSE_CURSOR_DEFAULT)
        
        if draw_game_options:
            option_iterator = 0
            for option in GAME_OPTIONS:
                optionX = 21*screen_width//50
                optionY = screen_height//5 + option_iterator
                draw_text(option, optionX, optionY, menu_size, BLACK)

                option_tableX = 7*screen_width//10
                option_tableY = screen_height//5 + option_iterator
                draw_thick_table(4, option_tableX, option_tableY, menu_size, menu_size, BLACK)
                game_options_coordinates.append([option_tableX, option_tableY, menu_size, menu_size])

                option_iterator+=screen_height//10

            if enable_plate_rotation:
                draw_texture_ex(truth_symbol, (7*screen_width//10, screen_height//5),0, 0.8,WHITE)
            if enable_golden_plate:
                draw_texture_ex(truth_symbol, (7*screen_width//10, 3*screen_height//10),0, 0.8,WHITE)
            if enable_insane_mode:
                draw_texture_ex(truth_symbol, (7*screen_width//10, 4*screen_height//10),0, 0.8,WHITE)

            mouse_in_plate_rotation = check_collision_point_rec(mouse_position, game_options_coordinates[0])
            mouse_in_golden_plate = check_collision_point_rec(mouse_position, game_options_coordinates[1])
            mouse_in_insane_mode = check_collision_point_rec(mouse_position, game_options_coordinates[2])

            if mouse_in_plate_rotation and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                enable_plate_rotation = False if enable_plate_rotation else True
            if mouse_in_golden_plate and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                enable_golden_plate = False if enable_golden_plate else True
            if mouse_in_insane_mode and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                enable_insane_mode = False if enable_insane_mode else True
        else:
            mouse_in_plate_rotation = False
            mouse_in_golden_plate = False
            mouse_in_insane_mode = False
            

        if draw_audio_options:
            option_iterator = 0
            lineX = 3*screen_width//5 - line_size//2
            audio_button_list = [[volume_master], [volume_music], [volume_effects]]
            set_master_volume(volume_master/500)

            set_sound_volume(breaking_sound_1, volume_effects/500)
            set_sound_volume(breaking_sound_2, volume_effects/500)
            set_sound_volume(pop_sound, volume_effects/500)

            set_music_volume(music_1,volume_music/500)

            for index, option in enumerate(AUDIO_OPTIONS):
                optionX = center_text_x(option, menu_size, 2*screen_width//5) + 2*screen_width//5
                optionY = screen_height//5 + option_iterator
                draw_text(option, optionX, optionY, menu_size, BLACK)
                
                option_iterator+=screen_height//10
                optionY = screen_height//5 + option_iterator
                print(audio_button_list)
                audio_button_list[index].append(optionY)

                draw_thick_horizontal_line(6, lineX, optionY, lineX + line_size, optionY, BLACK)
                draw_texture(audio_button, lineX + audio_button_list[index][0], optionY - 30, WHITE)

                option_iterator+=screen_height//10
            
            master_button = [lineX + audio_button_list[0][0], audio_button_list[0][1] - 30,60,60]
            music_button = [lineX + audio_button_list[1][0], audio_button_list[1][1] - 30,60,60]
            effects_button = [lineX + audio_button_list[2][0], audio_button_list[2][1] - 30,60,60]

            mouse_in_master_volume = check_collision_point_rec(mouse_position, master_button)
            mouse_in_music_volume = check_collision_point_rec(mouse_position, music_button)
            mouse_in_effects_volume = check_collision_point_rec(mouse_position, effects_button)

            # MASTER VOLUME
            if mouse_in_master_volume and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                change_master_button = True
            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT) and change_master_button:
                volume_master = int(mouse_position.x - lineX - 30)
                if volume_master >= line_size:
                    volume_master = line_size
                if volume_master <= 0:
                    volume_master = 0
            if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT) and change_master_button:
                change_master_button = False

            # MUSIC VOLUME
            if mouse_in_music_volume and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                change_music_button = True
            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT) and change_music_button:
                volume_music = int(mouse_position.x - lineX - 30)
                if volume_music >= line_size:
                    volume_music = line_size
                if volume_music <= 0:
                    volume_music = 0
            if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT) and change_music_button:
                change_music_button = False

            # EFFECTS VOLUME
            if mouse_in_effects_volume and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                change_effects_button = True
            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT) and change_effects_button:
                volume_effects = int(mouse_position.x - lineX - 30)
                if volume_effects >= line_size:
                    volume_effects = line_size
                if volume_effects <= 0:
                    volume_effects = 0
            if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT) and change_effects_button:
                change_effects_button = False
        else:
            mouse_in_master_volume = False
            mouse_in_music_volume = False
            mouse_in_effects_volume = False

        end_drawing()
        menu_items_coordinates.clear()
        game_options_coordinates.clear()
        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            screen = TITLE_SCREEN

    if screen == GAME_SCREEN:
        score_string = f"Score: {score}"
        score_x = center_text_x(score_string, warning_size, screen_width)

        begin_drawing()
        clear_background(RAYWHITE)
        
        draw_text(score_string, score_x, screen_height//10, warning_size, BLACK)
        for _ in life_list:
            draw_heart(life_list, screen_width, screen_height)
        circle_speed_min = 8 if is_window_fullscreen() else 6
        circle_speed_max = 12 if is_window_fullscreen() else 10
        golden_plate_speed = 14 if is_window_fullscreen() else 12
        
        if add_ball:
            if enable_golden_plate:
                golden_plate = True if random.randint(0,5) == 5 else False
            else:
                golden_plate = False

            circle_random_X_position = random.randint(screen_width//8, screen_width*7//8)
            circle_random_diameter = 50 if golden_plate else random.randint(80, 160)
            circle_random_speed = golden_plate_speed if golden_plate else random.randint(circle_speed_min, circle_speed_max)
            circle_initial_speed = circle_random_speed
            circle_sprite = [0, 0, 200, 200]
            frame_death_moment = 0
            circle_color = [253, 249, 0, 255] if golden_plate else [255,255,255,255]
            circle_rotation = 0
            circle_random_rotation = random.randint(4,6) if enable_plate_rotation else 0


            ball_list.append([circle_random_X_position, 
                              screen_height, 
                              circle_random_diameter, 
                              circle_random_speed, 
                              circle_initial_speed, 
                              circle_sprite, 
                              frame_death_moment, 
                              circle_color,
                              circle_random_rotation,
                              circle_rotation,
                              golden_plate])
            
            if ball_counter % round:
                ball_counter += 1
            else:
                ball_counter = 1
                add_ball = False
        
        for index, ball in enumerate(ball_list):
            draw_texture_pro(sprites, ball[5], [ball[0], ball[1],ball[2],ball[2]],[ball[2]//2,ball[2]//2],ball[9],ball[7])
            ball[9]+=ball[8]
            ball[1] = int(ball[1] - ball[3])
            ball[3] -= GRAVITY

            if ball[10] == True and ball[1] >= screen_height:
                play_sound(pop_sound)
                life_list.pop()
                if len(life_list) > 1:
                    play_sound(pop_sound)
                    life_list.pop()
                del ball_list[index]

            if ball[1] == screen_height:
                play_sound(pop_sound)
                life_list.pop()
                ball[3] = ball[4]
            
            if check_collision_point_circle(mouse_position,(ball[0],ball[1]),ball[2]//2) and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                if ball[10]:
                    score+=5
                    play_sound(breaking_sound_2)
                    life_list.append(golden_heart)
                else:
                    score+=1
                    play_sound(breaking_sound_1)
                ball[6] = current_frame - 1
                ball_deletion_list.append(ball_list[index])
                del ball_list[index]
        
        for index, ball in enumerate(ball_deletion_list):
            draw_texture_pro(sprites, ball[5], [ball[0], ball[1], ball[2], ball[2]], [ball[2]//2,ball[2]//2],0,ball[7])
            deltha_time = int(current_frame - ball[6])
            if (not deltha_time % 5) and ball[5][0] < 400:
                ball[5][0]+=sprite_iterator
            if ball[5][0] == 400:
                deltha_time = 0
                ball[7][3] -= 10
                if ball[7][3] <= 0:
                    del ball_deletion_list[index]
        
        if not ball_list:
            if round != max_balls:
                round += 1
            add_ball = True

        end_drawing()

        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            screen = PAUSE_SCREEN

        if not life_list:
            screen = LOST_SCREEN
        
        if score >= 100:
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
                    ball_deletion_list = []
                    score = 0
                    round = 1
                    ball_counter = 1
                    life_list = [heart for _ in range(5)]
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
            ball_deletion_list = []
            score = 0
            round = 1
            ball_counter = 1
            life_list = [heart for _ in range(5)]
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
            ball_deletion_list = []
            score = 0
            round = 1
            ball_counter = 1
            life_list = [heart for _ in range(5)]
            screen = TITLE_SCREEN
        end_drawing()
unload_sound(breaking_sound_1)
unload_sound(breaking_sound_2)
unload_sound(pop_sound)
unload_music_stream(music_1)
close_audio_device()
close_window()