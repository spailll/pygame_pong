# Author:   Ben Sailor
# Email:    bsailor@okstate.edu
# Date:     1/24/2024
# Desc:     A simple pong game with a start button 
#           and score counter. Developed using pygame.

import pygame
import random

# Change these variables to change various aspects of the game
WIDTH, HEIGHT = 1000, 1100                      # Window size
PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT = 1000, 1000  # Play area size
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60            # Paddle size
BALL_WIDTH, BALL_HEIGHT = 10, 10                # Ball size
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50           # Start button size

# Change these variables to change the speed of the paddle and ball
VEL = 10            # Paddle speed
VEL_INCREASE = 1    # Ball speed increase on paddle hit

FPS = 60            # Frames per second

# Defined some colors for easier use
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Initialize pygame and the window
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Function to draw the window
def draw_window(objects):
    # Set the background color to white
    WIN.fill(WHITE)
    # Draw the top section of the window and make it black
    pygame.draw.rect(WIN, BLACK, objects[0])
    # Draw the start button's shadow and make it gray
    pygame.draw.rect(WIN, GRAY, objects[1])
    # Draw the start button and make it white
    pygame.draw.rect(WIN, WHITE, objects[2])
    # Draw the start button text
    WIN.blit(objects[3], (objects[1].x + 20, objects[1].y + 20))
    # Draw the left paddle and make it black
    pygame.draw.rect(WIN, BLACK, objects[4])
    # Draw the right paddle and make it black
    pygame.draw.rect(WIN, BLACK, objects[5])
    # Draw the ball and make it black
    pygame.draw.rect(WIN, BLACK, objects[6])
    # Draw the left score text
    WIN.blit(objects[7], (100, 30))
    # Draw the right score text
    WIN.blit(objects[8], (WIDTH - 100 - objects[8].get_width(), 30))
    # Update the display
    pygame.display.update()

# Function to handle left paddle movement
def handle_movement_1(keys_pressed, paddle1):
    # Check if the W key is pressed and the left paddle is not at the top of the play area
    if keys_pressed[pygame.K_w] and paddle1.y > VEL + HEIGHT - PLAY_AREA_HEIGHT:
        paddle1.y -= VEL    # Move the left paddle up
    # Check if the S key is pressed and the left paddle is not at the bottom of the play area
    if keys_pressed[pygame.K_s] and paddle1.y < HEIGHT - PADDLE_HEIGHT - VEL:
        paddle1.y += VEL    # Move the left paddle down

# Function to handle right paddle movement
def handle_movement_2(keys_pressed, paddle2):
    # Check if the UP key is pressed and the right paddle is not at the top of the play area
    if keys_pressed[pygame.K_UP] and paddle2.y > VEL + HEIGHT - PLAY_AREA_HEIGHT:
        paddle2.y -= VEL    # Move the right paddle up
    # Check if the DOWN key is pressed and the right paddle is not at the bottom of the play area
    if keys_pressed[pygame.K_DOWN] and paddle2.y < HEIGHT - PADDLE_HEIGHT - VEL:
        paddle2.y += VEL    # Move the right paddle down

# Function to update the ball position
def update_ball(start, direction_1, direction_2, vel1, vel2, paddle1, paddle2, ball):
    i = 0
    if start:           # If the game has started
        # Check if the ball is colliding with the top or bottom of the play area
        if ball.y < HEIGHT - PLAY_AREA_HEIGHT + vel1 or ball.y > HEIGHT - BALL_HEIGHT - vel1:
            i += 1      # Add 1 to return encoding
            ball.y += vel1 * direction_1 * -1   # Reverse the y-direction of the ball temporarily
        else:           # If the ball is not colliding with the top or bottom of the play area 
            ball.y += vel1 * direction_1        # Move the ball in the current y-direction
        # Check if the ball is colliding with either paddle
        if ball.colliderect(paddle1) or ball.colliderect(paddle2) or paddle1.colliderect(ball) or paddle2.colliderect(ball): 
            i += 2      # Add 2 to return encoding
            vel2 += 1   # Increase the speed of the ball
            ball.x += vel2 * direction_2 * -1   # Reverse the x-direction of the ball temporarily
        # Check if the ball is colliding with the left side of the play area
        elif ball.x < vel2: 
            i += 4      # Add 4 to return encoding
        # Check if the ball is colliding with the right side of the play area
        elif ball.x > WIDTH - BALL_WIDTH - vel2:
            i += 8      # Add 8 to return encoding
        else:           # If the ball is not colliding with anything
            ball.x += vel2 * direction_2    # Move the ball in the current x-direction
        return i        # Return the encoding
        
# Main function
def main():
    # Initialize all the objects
    # top_section is the top section of the window where the score and start button are located
    top_section = pygame.Rect(0, 0, WIDTH, HEIGHT - PLAY_AREA_HEIGHT)
    # start_button is the start button
    start_button = pygame.Rect((WIDTH / 2) - (BUTTON_WIDTH / 2), ((HEIGHT - PLAY_AREA_HEIGHT) / 2) - (BUTTON_HEIGHT / 2), BUTTON_WIDTH, BUTTON_HEIGHT)
    # start_button_shadow is the shadow of the start button
    start_button_shadow = pygame.Rect((WIDTH / 2) - (BUTTON_WIDTH / 2) + 5, ((HEIGHT - PLAY_AREA_HEIGHT) / 2) - (BUTTON_HEIGHT / 2) + 5, BUTTON_WIDTH, BUTTON_HEIGHT)
    # start_button_text is the text on the start button
    start_button_text = pygame.font.Font(None, 36).render("START", True, BLACK)
    # paddle1 is the left paddle
    paddle1 = pygame.Rect(0, (HEIGHT - PLAY_AREA_HEIGHT) + PLAY_AREA_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    # paddle2 is the right paddle
    paddle2 = pygame.Rect(PLAY_AREA_WIDTH - PADDLE_WIDTH, (HEIGHT - PLAY_AREA_HEIGHT) + PLAY_AREA_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    # ball is the ball
    ball = pygame.Rect((WIDTH / 2) - (BALL_WIDTH / 2), (HEIGHT - PLAY_AREA_HEIGHT) + (PLAY_AREA_HEIGHT / 2) - (BALL_WIDTH / 2) , BALL_WIDTH, BALL_HEIGHT)

    # score1 and score2 are the scores of the left and right players respectively
    score1 = 0
    score2 = 0

    # P1_Score and P2_Score are the text objects for the scores
    P1_Score = pygame.font.Font(None, 84).render(str(score1), True, WHITE)
    P2_Score = pygame.font.Font(None, 84).render(str(score2), True, WHITE)

    # start is a boolean that determines if the game has started (i.e. ball is moving)
    start = False   
    # direction_1 and direction_2 are the directions of the ball in the x and y directions respectively
    direction_1 = (random.randint(1, 2) % 2) * 2 - 1
    direction_2 = (random.randint(1, 2) % 2) * 2 - 1
    # vel1 and vel2 are the speeds of the ball in the y and x directions respectively (giving it a semirandom angle of travel)
    vel1 = random.randint(1,3)
    vel2 = random.randint(1,3)
    if vel1 == vel2:    # If the speeds are the same
        vel2 += 1       # Increase the speed of the ball in the y direction, so it doesnt just hit the corners
    # run is a boolean that determines if the game is running (i.e. program is started/running)
    run = True          
    # clock is the pygame clock
    clock = pygame.time.Clock()

    # Main loop oof the game
    while run:
        # Tick the clock at rate of FPS
        clock.tick(FPS)
        # Get all the events that have happened since the last tick
        for event in pygame.event.get():
            # Check if the user has quit the game
            if event.type == pygame.QUIT:
                run = False     # Set run to false to exit the loop
            # Check if the user has clicked the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse
                mouse_pos = event.pos
                # Check if the mouse is within the start button
                if start_button.collidepoint(mouse_pos):
                    # Set start to true to start the game
                    start = True
            # Get all the keys that are currently pressed
            keys_pressed = pygame.key.get_pressed()
            # Check if the user has pressed the space bar
            if keys_pressed[pygame.K_SPACE]:
                # Set start to true to start the game
                start = True
        # Pass the keys pressed and the paddles to the movement functions
        handle_movement_1(keys_pressed, paddle1)
        handle_movement_2(keys_pressed, paddle2)
        # Update the ball position and get the return encoding
        ret = update_ball(start, direction_1, direction_2, vel1, vel2, paddle1, paddle2, ball)
        # Create a list of all the objects to be drawn
        objects = [top_section, start_button_shadow, start_button, start_button_text, paddle1, paddle2, ball, P1_Score, P2_Score]
        # Draw the window with the objects
        draw_window(objects)
        if ret == 1:                # If the ball is colliding with the top or bottom of the play area
            direction_1 *= -1       # Reverse the y-direction of the ball
        elif ret == 2:              # If the ball is colliding with either paddle
            direction_2 *= -1       # Reverse the x-direction of the ball
            vel1 += VEL_INCREASE    # Increase the speed of the ball in the y-direction
            vel2 += VEL_INCREASE    # Increase the speed of the ball in the x-direction
        elif ret == 3:              # If the ball is colliding with the top or bottom of the play area and either paddle
            direction_1 *= -1       # Reverse the y-direction of the ball
            direction_2 *= -1       # Reverse the x-direction of the ball
            vel1 += VEL_INCREASE    # Increase the speed of the ball in the y-direction
            vel2 += VEL_INCREASE    # Increase the speed of the ball in the x-direction
        elif ret == 4 or ret == 5:  # If the ball is colliding with the left side of the play area
            # Set start to false to stop the game
            start = False           
            # Reset the ball position to the middle of the play area
            ball.x = (WIDTH / 2) - (BALL_WIDTH / 2) 
            ball.y = (HEIGHT - PLAY_AREA_HEIGHT) + (PLAY_AREA_HEIGHT / 2) - (BALL_WIDTH / 2)
            # Randomize the ball directions for start of next round
            direction_1 = (random.randint(1, 2) % 2) * 2 - 1
            direction_2 = (random.randint(1, 2) % 2) * 2 - 1
            # Randomize the ball speeds (starting angle)
            vel1 = random.randint(1,3)
            vel2 = random.randint(1,3)
            if vel1 == vel2:        # If the speeds are the same
                vel2 += 1           # Increase the speed of the ball in the y direction, so it doesnt just hit the corners
            # Increase the score of the left player
            score1 += 1
            # Update the score text             
            P1_Score = pygame.font.Font(None, 84).render(str(score1), True, WHITE)
        elif ret == 8 or ret == 9:  # If the ball is colliding with the right side of the play area
            # Set start to false to stop the game
            start = False
            # Reset the ball position to the middle of the play area
            ball.x = (WIDTH / 2) - (BALL_WIDTH / 2)
            ball.y = (HEIGHT - PLAY_AREA_HEIGHT) + (PLAY_AREA_HEIGHT / 2) - (BALL_WIDTH / 2)
            # Randomize the ball direction for start of next round
            direction_1 = (random.randint(1, 2) % 2) * 2 - 1
            direction_2 = (random.randint(1, 2) % 2) * 2 - 1
            # Randomize the ball speeds (starting angle)
            vel1 = random.randint(1,3)
            vel2 = random.randint(1,3)
            if vel1 == vel2:        # If the speeds are the same
                vel2 += 1           # Increase the speed of the ball in the y direction, so it doesnt just hit the corners
            # Increase the score of the right player
            score2 += 1
            # Update the score text
            P2_Score = pygame.font.Font(None, 84).render(str(score2), True, WHITE)
    # after the loop is exited, quit the game and program
    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()