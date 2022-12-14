import pygame
import sys
import random
import asyncio

from components.Player import Player
from components.Enemy import Enemy

# Initialize pygame
pygame.init()

# Create a window
size = width, height = 800, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SpikeDodge")
white = 255, 255, 255
black = 0, 0, 0

async def main():
  score = 0
  high_score = 0

# Load assets
  ball = Player()
  ball_rect = ball.rect

  spike = pygame.image.load("assets/spike.png").convert_alpha()

  water = pygame.image.load("assets/water.png").convert_alpha()

  font = pygame.font.Font("assets/JustMyType.ttf", 20)
  big_font = pygame.font.Font("assets/JustMyType.ttf", 100)

  play_button = pygame.image.load("assets/playbutton.png").convert_alpha()
  play_button_rect = play_button.get_rect()
  play_button_rect.x = 400 - 75
  play_button_rect.y = 400

  left = pygame.image.load("assets/left.png").convert_alpha()
  left_rect = left.get_rect()
  left_rect.x = 130
  left_rect.y = 370
  right = pygame.image.load("assets/right.png").convert_alpha()
  right_rect = right.get_rect()
  right_rect.x = 570
  right_rect.y = 370
  left_accel = pygame.image.load("assets/leftaccel.png").convert_alpha()
  left_accel_rect = left_accel.get_rect()
  left_accel_rect.x = 30
  left_accel_rect.y = 370
  right_accel = pygame.image.load("assets/rightaccel.png").convert_alpha()
  right_accel_rect = right_accel.get_rect()
  right_accel_rect.x = 670
  right_accel_rect.y = 370
  exit_button = pygame.image.load("assets/exitbutton.png").convert_alpha()
  exit_button_rect = exit_button.get_rect()
  exit_button_rect.x = 400 - 20
  exit_button_rect.y = 4

  enemies = []
  enemy_amount = 5
  multiplier = 5

  pygame.mixer.music.load("assets/musicloop.wav")
  if sys.platform == "emscripten":
    pygame.mixer.music.load("assets/musicloop.ogg")
  pygame.mixer.music.set_volume(0.2)
  pygame.mixer.music.play(loops=-1)

  death_sound = pygame.mixer.Sound("assets/death.wav")
  if sys.platform == "emscripten":
    death_sound = pygame.mixer.Sound("assets/death.ogg")

  clock = pygame.time.Clock()

  running = True
  menu = True
  gameplay = False
  touch = False

  while running:
    clock.tick(60)

    # Close the windows when the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.FINGERDOWN:
            touch = True

    if menu:
        screen.fill(white)
        screen.blit(big_font.render("SpikeDodge", True, black), (230, 150))
        high_score_text = font.render(f"High Score: {high_score}", True, black)
        screen.blit(high_score_text, (400 - (high_score_text.get_width() / 2), 300))
        if play_button_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(pygame.transform.scale(play_button, (225, 75)), (
                400 - 112.5,
                400 - 15
            ))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.FINGERDOWN:
                menu = False
                ball_rect.x = 400 - (ball_rect.width / 2)
                for i in range(enemy_amount):
                    enemies.append(Enemy(random.randint(0, 800 - 64), -64))
                gameplay = True
        else:
            screen.blit(play_button, play_button_rect)
        screen.blit(font.render("Play", True, black), (400 - 12, 414))

    if gameplay:
        acceleration = 4
        keys = pygame.key.get_pressed()
        if ball_rect.x <= 0:
            ball_rect.x = 1
        if ball_rect.x >= 800 - 64:
            ball_rect.x = 799 - 64
        if keys[pygame.K_LSHIFT]:
            acceleration = 12
            touch = False
        if keys[pygame.K_LEFT]:
            ball_rect.x = ball_rect.x - acceleration
            touch = False
        if keys[pygame.K_RIGHT]:
            ball_rect.x = ball_rect.x + acceleration
            touch = False
        if keys[pygame.K_ESCAPE]:
            enemies.clear()
            score = 0
            enemy_amount = 5
            gameplay = False
            menu = True
            touch = False
        if left_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.FINGERDOWN:
            ball_rect.x = ball_rect.x - acceleration
        if left_accel_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.FINGERDOWN:
            acceleration = 12
            ball_rect.x = ball_rect.x - acceleration
        if right_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.FINGERDOWN:
            ball_rect.x = ball_rect.x + acceleration
        if right_accel_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.FINGERDOWN:
            acceleration = 12
            ball_rect.x = ball_rect.x + acceleration
        if exit_button_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.FINGERDOWN:
            enemies.clear()
            score = 0
            enemy_amount = 5
            multiplier = 5
            gameplay = False
            menu = True

        screen.fill(white)

        for enemy in enemies:
            enemy.y = enemy.y + enemy.speed

            if ball_rect.x + 32 > enemy.x and ball_rect.x < enemy.x + 32:
                if ball_rect.y + 32 > enemy.y and ball_rect.y < enemy.y + 32:
                    death_sound.play()
                    enemies.clear()
                    if score > high_score:
                        high_score = score
                    score = 0
                    enemy_amount = 5
                    multiplier = 5
                    gameplay = False
                    menu = True

            if enemy.y > 480:
                enemy.x = random.randint(0, 800 - 32)
                enemy.y = -64
                score += 1
                if score % multiplier == 0:
                    multiplier = multiplier * 2
                    enemy_amount = enemy_amount + 1
                    enemies.append(Enemy(random.randint(0, 800 - 64), -64))

            screen.blit(spike, (enemy.x, enemy.y))

        screen.blit(ball.image, ball_rect)
        water.get_rect().x = water.get_rect().x + 10
        screen.blit(water, (water.get_rect().x, 480 - 85))

        score_text = font.render(f"Score: {score}", True, black)
        screen.blit(score_text, (4, 4))
        
        if sys.platform == "emscripten" and touch == True:
            screen.blit(left, left_rect)
            screen.blit(right, right_rect)
            screen.blit(left_accel, left_accel_rect)
            screen.blit(right_accel, right_accel_rect)
            screen.blit(exit_button, exit_button_rect)

    pygame.display.update()
    await asyncio.sleep(0)

asyncio.run(main())