#Author: Angelic McPherson
#Date: 10/5/2021
#Purpose: To create a program similar to pong

from cs1lib import *
import random

"""
Set all relevant variables and constants
"""
# define window constants
HEIGHT_WINDOW = WIDTH_WINDOW = 400

# define paddle constants
HEIGHT_PADDLE = 80
WIDTH_PADDLE = 20
PADDLE_BOUND_LEFT = 0
PADDLE_BOUND_RIGHT = 320
MOVEMENT_AMOUNT = 5

# define ball constants
INITIAL_VELOCITY = 3
SIZE = 10

# define paddle coordinate variables
paddle_x_left = PADDLE_BOUND_LEFT
paddle_y_left = PADDLE_BOUND_LEFT
paddle_x_right = WIDTH_WINDOW - WIDTH_PADDLE
paddle_y_right = PADDLE_BOUND_RIGHT

# define ball variables
ball_x = HEIGHT_WINDOW//2
ball_y = HEIGHT_WINDOW//2
x_velocity = INITIAL_VELOCITY
y_velocity = INITIAL_VELOCITY

# define key constants
KEY_A = "a"
KEY_Z = "z"
KEY_K = "k"
KEY_M = "m"
KEY_Q = "q"
KEY_SPACE = " "

# define keys pressed variables
apressed = False
zpressed = False
kpressed = False
mpressed = False
spacepressed = False
qpressed = False
playing = False


"""
Add ball and paddles to the screen
"""
#Purpose: To create the ball
#Parameter:r, g, and b values for color
def ball(r, g, b):
    set_stroke_width(1)
    draw_circle(ball_x, ball_y, SIZE)
    set_fill_color(r, g, b)
    set_stroke_color(r, g, b)


#Purpose: To create the paddles
#Parameter: x, y for paddle location; r, g, and b values for color
def paddle(x, y, r, g, b):
    set_stroke_width(1)
    set_fill_color(r, g, b)
    set_stroke_color(r, g, b)
    draw_rectangle(x, y, WIDTH_PADDLE, HEIGHT_PADDLE)


"""
Define functions to move paddles and ball and handle collisions
"""
#Purpose: To move the paddles
#Parameters: none
def move_paddle():
    global paddle_y_left, paddle_y_right
    if apressed:
        if paddle_y_left > PADDLE_BOUND_LEFT:
            paddle_y_left = paddle_y_left - MOVEMENT_AMOUNT
    if zpressed:
        if paddle_y_left < PADDLE_BOUND_RIGHT:
            paddle_y_left = paddle_y_left + MOVEMENT_AMOUNT
    if kpressed:
        if paddle_y_right > PADDLE_BOUND_LEFT:
            paddle_y_right = paddle_y_right - MOVEMENT_AMOUNT
    if mpressed:
        if paddle_y_right < PADDLE_BOUND_RIGHT:
            paddle_y_right = paddle_y_right + MOVEMENT_AMOUNT


#Purpose: To move the ball
#Parameter: none
def move_ball():
    global ball_x, ball_y
    ball_x += x_velocity
    ball_y += y_velocity


#Purpose: To define boundaries of paddles and handle all ball collisions with walls and paddles
#Parameters: none
def handle_all_collisions():
    global paddle_x_left, paddle_y_left, paddle_x_right, paddle_y_right, ball_top, ball_bottom, ball_right, ball_left

    # create the paddle bounds for functions
    p_y_l = paddle_y_left + HEIGHT_PADDLE
    p_x_l = paddle_x_left + WIDTH_PADDLE
    p_x_r = WIDTH_WINDOW - WIDTH_PADDLE
    p_y_r = paddle_y_right + HEIGHT_PADDLE

    # create ball bounds for functions 
    ball_right = ball_x + SIZE
    ball_left = ball_x - SIZE
    ball_top = ball_y - SIZE
    ball_bottom = ball_y + SIZE

    # call collision functions
    paddle_collision(ball_left, ball_right, p_x_r, p_y_r, p_x_l, p_y_l)
    wall_collision(ball_top, ball_bottom, ball_right, ball_left)


#Purpose: To determine if the ball has made contact with the paddles or not
#Parameter: The ball boundaries and paddle boundaries
def paddle_collision(b_l, b_r, p_x_r, p_y_r, p_x_l, p_y_l):
    global ball_x, x_velocity, y_velocity

    # set behavior of the ball when it collides with paddles
    # left paddle
    if (b_r >= p_x_r) and (paddle_y_right <= ball_y <= p_y_r):
        ball_x = p_x_r - SIZE
        x_velocity *= -1

    # right paddle
    if (b_l <= p_x_l) and (paddle_y_left <= ball_y <= p_y_l):
        ball_x = p_x_l + SIZE
        x_velocity *= -1


#Purpose: To determine whether or not the ball has made contact with the boundaries or paddles.
#Parameter: The ball boundaries
def wall_collision(b_t, b_b, b_r, b_l):
    global x_velocity, y_velocity

    # set behavior of the ball when it collides with top and bottom of screen
    if b_t <= HEIGHT_WINDOW-HEIGHT_WINDOW:
        y_velocity *= -1

    if b_b >= HEIGHT_WINDOW:
        y_velocity *= -1

    # set behavior of the ball when it collides with left and right of the screen
    if b_r >= WIDTH_WINDOW:
        y_velocity = x_velocity = 0
        game_over()

    if b_l <= WIDTH_WINDOW - WIDTH_WINDOW:
        y_velocity = x_velocity = 0
        game_over()

"""
Handle game functionality with keyboard
"""
#Purpose: To see when a key is released
#Parameters: the key that is released
def keyboardrelease(value):
    global apressed, zpressed, kpressed, mpressed, qpressed
    if value == KEY_A:
        apressed = False
    if value == KEY_Z:
        zpressed = False
    if value == KEY_K:
        kpressed = False
    if value == KEY_M:
        mpressed = False
    if value == KEY_Q:
        qpressed = True


#Purpose: To see when a key is pressed
#Parameters: the key that is pressed
def keyboardpress(value):
    global apressed, zpressed, kpressed, mpressed, spacepressed, qpressed, playing
    if value == KEY_A:
        apressed = True
    if value == KEY_Z:
        zpressed = True
    if value == KEY_K:
        kpressed = True
    if value == KEY_M:
        mpressed = True
    if value == KEY_SPACE:
        spacepressed = True
        new_game()
        playing = True
    if value == KEY_Q:
        qpressed = True

"""
Define functions to set new game, handle main menu and game over
"""
#Purpose: To generate random colors
#Parameter: none
def get_random_color():
    # get random rgb values
    r = random.random()
    g = random.random()
    b = random.random()
    
    # normalize so sum is 1
    total = r + g + b
    r /= total
    g /= total
    b /= total
    
    return r, g, b


#Purpose: To show the game over screen
#Parameter: none
def game_over():
    # "Game Over" sign
    # draw box
    set_stroke_width(5)
    set_fill_color(0,0,0)
    r,g,b = get_random_color()
    set_stroke_color(r,g,b)
    draw_rectangle(100,150,200,100)

    # draw text
    set_stroke_width(15)
    r,g,b = get_random_color()
    set_stroke_color(r,g,b)
    set_font_bold()
    draw_text("GAME OVER", 160, 205)

    # show quit or play again nstructions 
    show_instructions()


#Purpose: To start the new game
#Parameter: none
def new_game():
    global ball_x, ball_y, x_velocity, y_velocity, paddle_y_left, paddle_y_right, spacepressed, playing

    # reset the variables used in the game to put ball and paddles back to the original position
    paddle_y_left = HEIGHT_WINDOW - HEIGHT_WINDOW
    paddle_y_right = HEIGHT_WINDOW - HEIGHT_PADDLE
    ball_x = WIDTH_WINDOW//2
    ball_y = HEIGHT_WINDOW//2
    x_velocity = INITIAL_VELOCITY
    y_velocity = INITIAL_VELOCITY
    playing = False

    # clear the screen
    clear()

    # draw the paddles and ball again
    R, G, B = get_random_color()
    paddle(paddle_x_left, paddle_y_left,  R, G, B)
    paddle(paddle_x_right, paddle_y_right, R, G, B)
    ball(R, G, B)


#Purpose: To show instructions if on the home screen or restarting the game
#Parameter: none
def show_instructions():
        # ask to press spacebar or quit
        set_stroke_color(1,1,1)
        set_stroke_width(10)
        set_font_bold()
        draw_text("PRESS SPACEBAR TO PLAY", 110, 275)
        draw_text("PRESS Q TO QUIT", 139, 300)


#Purpose: To quit the game if the q key is pressed
#Parameter: none
def quit_game():
    if qpressed:
        cs1_quit()

#Purpose: To start the game and run all the created functions together
#Parameter: none
def main_game():
    # clear the screen and display instrcutions
    set_clear_color(0,0,0)
    clear()
    if not playing:
        show_instructions()

    # draw the paddles and ball
    paddle(paddle_x_left, paddle_y_left, 1, 1, 1)
    paddle(paddle_x_right, paddle_y_right, 1, 1, 1)
    ball(1, 1, 1)
    
    # check for game quit
    quit_game()
    
    # if game is being played handle collisions, ball and paddle movements
    if playing:
        move_ball()
        move_paddle()
        handle_all_collisions()

start_graphics(main_game, key_press=keyboardpress, key_release=keyboardrelease, height=HEIGHT_WINDOW, width=WIDTH_WINDOW)


