# Author:   Ben Sailor
# Email:    bsailor@okstate.edu
# Date:     1/24/2024
# Desc:     A simple pong game with a start button 
#           and score counter. Developed using pygame.

import pygame
import random

WIDTH, HEIGHT = 1000, 1100
PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT = 1000, 1000
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_WIDTH, BALL_HEIGHT = 10, 10
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50

VEL = 10
VEL_INCREASE = 1

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

def draw_window(objects):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, objects[0])
    pygame.draw.rect(WIN, GRAY, objects[2])
    pygame.draw.rect(WIN, WHITE, objects[1])
    WIN.blit(objects[3], (objects[1].x + 20, objects[1].y + 20))
    pygame.draw.rect(WIN, BLACK, objects[4])
    pygame.draw.rect(WIN, BLACK, objects[5])
    pygame.draw.rect(WIN, BLACK, objects[6])
    WIN.blit(objects[7], (100, 30))
    WIN.blit(objects[8], (WIDTH - 100 - objects[8].get_width(), 30))
    pygame.display.update()

def handle_movement_1(keys_pressed, paddle1):
    if keys_pressed[pygame.K_w] and paddle1.y > VEL + HEIGHT - PLAY_AREA_HEIGHT:
        paddle1.y -= VEL
    if keys_pressed[pygame.K_s] and paddle1.y < HEIGHT - PADDLE_HEIGHT - VEL:
        paddle1.y += VEL

def handle_movement_2(keys_pressed, paddle2):
    if keys_pressed[pygame.K_UP] and paddle2.y > VEL + HEIGHT - PLAY_AREA_HEIGHT:
        paddle2.y -= VEL
    if keys_pressed[pygame.K_DOWN] and paddle2.y < HEIGHT - PADDLE_HEIGHT - VEL:
        paddle2.y += VEL

def update_ball(start, direction_1, direction_2, vel1, vel2, paddle1, paddle2, ball):
    i = 0
    if start:
        if ball.y < HEIGHT - PLAY_AREA_HEIGHT + vel1 or ball.y > HEIGHT - BALL_HEIGHT - vel1:
            i += 1
            ball.y += vel1 * direction_1 * -1
        else: 
            ball.y += vel1 * direction_1
        if ball.colliderect(paddle1) or ball.colliderect(paddle2) or paddle1.colliderect(ball) or paddle2.colliderect(ball): 
            i += 2
            vel2 += 1
            ball.x += vel2 * direction_2 * -1
        elif ball.x < vel2:
            i += 4
        elif ball.x > WIDTH - BALL_WIDTH - vel2:
            i += 8
        else:
            ball.x += vel2 * direction_2
        return i
        
def main():
    top_section = pygame.Rect(0, 0, WIDTH, HEIGHT - PLAY_AREA_HEIGHT)
    start_button = pygame.Rect((WIDTH / 2) - (BUTTON_WIDTH / 2), ((HEIGHT - PLAY_AREA_HEIGHT) / 2) - (BUTTON_HEIGHT / 2), BUTTON_WIDTH, BUTTON_HEIGHT)
    start_button_shadow = pygame.Rect((WIDTH / 2) - (BUTTON_WIDTH / 2) + 5, ((HEIGHT - PLAY_AREA_HEIGHT) / 2) - (BUTTON_HEIGHT / 2) + 5, BUTTON_WIDTH, BUTTON_HEIGHT)
    start_button_text = pygame.font.Font(None, 36).render("START", True, BLACK)
    paddle1 = pygame.Rect(0, (HEIGHT - PLAY_AREA_HEIGHT) + PLAY_AREA_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(PLAY_AREA_WIDTH - PADDLE_WIDTH, (HEIGHT - PLAY_AREA_HEIGHT) + PLAY_AREA_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect((WIDTH / 2) - (BALL_WIDTH / 2), (HEIGHT - PLAY_AREA_HEIGHT) + (PLAY_AREA_HEIGHT / 2) - (BALL_WIDTH / 2) , BALL_WIDTH, BALL_HEIGHT)

    score1 = 0
    score2 = 0

    P1_Score = pygame.font.Font(None, 84).render(str(score1), True, WHITE)
    P2_Score = pygame.font.Font(None, 84).render(str(score2), True, WHITE)

    start = False
    direction_1 = (random.randint(1, 2) % 2) * 2 - 1
    direction_2 = (random.randint(1, 2) % 2) * 2 - 1
    vel1 = random.randint(1,3)
    vel2 = random.randint(1,3)
    if vel1 == vel2:
        vel2 += 1
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    start = True
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                start = True
        handle_movement_1(keys_pressed, paddle1)
        handle_movement_2(keys_pressed, paddle2)
        ret = update_ball(start, direction_1, direction_2, vel1, vel2, paddle1, paddle2, ball)
        objects = [top_section, start_button, start_button_shadow, start_button_text, paddle1, paddle2, ball, P1_Score, P2_Score]

        draw_window(objects)
        if ret == 1:
            direction_1 *= -1
        elif ret == 2:
            direction_2 *= -1
            vel1 += VEL_INCREASE
            vel2 += VEL_INCREASE
        elif ret == 3:
            direction_1 *= -1
            direction_2 *= -1
        elif ret == 4 or ret == 5:
            start = False
            ball.x = (WIDTH / 2) - (BALL_WIDTH / 2)
            ball.y = (HEIGHT - PLAY_AREA_HEIGHT) + (PLAY_AREA_HEIGHT / 2) - (BALL_WIDTH / 2)
            direction_1 = (random.randint(1, 2) % 2) * 2 - 1
            direction_2 = (random.randint(1, 2) % 2) * 2 - 1
            vel1 = random.randint(1,3)
            vel2 = random.randint(1,3)
            if vel1 == vel2:
                vel2 += 1
            score1 += 1
            P1_Score = pygame.font.Font(None, 84).render(str(score1), True, WHITE)
        elif ret == 8 or ret == 9:
            start = False
            ball.x = (WIDTH / 2) - (BALL_WIDTH / 2)
            ball.y = (HEIGHT - PLAY_AREA_HEIGHT) + (PLAY_AREA_HEIGHT / 2) - (BALL_WIDTH / 2)
            direction_1 = (random.randint(1, 2) % 2) * 2 - 1
            direction_2 = (random.randint(1, 2) % 2) * 2 - 1
            vel1 = random.randint(1,3)
            vel2 = random.randint(1,3)
            if vel1 == vel2:
                vel2 += 1
            score2 += 1
            P2_Score = pygame.font.Font(None, 84).render(str(score2), True, WHITE)

    pygame.quit()

if __name__ == "__main__":
    main()