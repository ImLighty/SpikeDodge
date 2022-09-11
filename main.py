import pygame, sys
import random, winsound

# Initialize pygame
pygame.init()

class Enemy:
  x = 0
  y = 0,
  speed = 0
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.speed = random.randint(5, 10)

# Create a window
size = width, height = 800, 480
screen = pygame.display.set_mode(size, vsync=True)
pygame.display.set_caption("First Python Game")
white = 255, 255, 255
black = 0, 0, 0

score = 0

# Load assets
ball = pygame.image.load("assets/ball.png")
ball_rect = ball.get_rect()
ball_rect.x = 400 - (ball_rect.width / 2)
ball_rect.y = 300

spike = pygame.image.load("assets/spike.png")

water = pygame.image.load("assets/water.png")

font = pygame.font.Font("assets/JustMyType.ttf", 20)
big_font = pygame.font.Font("assets/JustMyType.ttf", 100)

play_button = pygame.image.load("assets/playbutton.png")
play_button_rect = play_button.get_rect()
play_button_rect.x = 400 - 75
play_button_rect.y = 400

enemies = []
enemy_amount = 5

pygame.mixer.music.load("assets/musicloop.wav")
if sys.platform == "emscripten":
  pygame.mixer.music.load("assets/musicloop.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1, start=0, fade_ms=1000)

death_sound = pygame.mixer.Sound("assets/death.wav")
if sys.platform == "emscripten":
  death_sound = pygame.mixer.Sound("assets/death.ogg")

clock = pygame.time.Clock()

running = True
menu = True
gameplay = False

while running:
  clock.tick(60)

  # Close the windows when the window is closed
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  if menu:
    screen.fill(white)
    screen.blit(big_font.render("First", True, black), (320, 50))
    screen.blit(big_font.render("Python", True, black), (290, 150))
    screen.blit(big_font.render("Game", True, black), (310, 260))
    if play_button_rect.collidepoint(pygame.mouse.get_pos()):
      screen.blit(pygame.transform.scale(play_button, (225, 75)), (
        400 - 112.5,
        400 - 15
      ))
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        menu = False
        for i in range(enemy_amount):
          enemies.append(Enemy(random.randint(0, 800 - 64), -64))
        gameplay = True
    else:
      screen.blit(play_button, play_button_rect)
    screen.blit(font.render("Play", True, black), (400 - 12, 414))

      
  if gameplay:
    acceleration = 4
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
      acceleration = 12
    if keys[pygame.K_LEFT]:
      ball_rect.x = ball_rect.x - acceleration
    if keys[pygame.K_RIGHT]:
      ball_rect.x = ball_rect.x + acceleration
    if keys[pygame.K_ESCAPE]:
      enemies.clear()
      score = 0
      enemy_amount = 5
      gameplay = False
      menu = True

    screen.fill(white)

    for enemy in enemies:
      enemy.y = enemy.y + enemy.speed

      if ball_rect.x + 32 > enemy.x and ball_rect.x < enemy.x + 32:
        if ball_rect.y + 32 > enemy.y and ball_rect.y < enemy.y + 32:
          death_sound.play()
          enemies.clear()
          score = 0
          enemy_amount = 5
          for i in range(enemy_amount):
            enemies.append(Enemy(random.randint(0, 800 - 64), -64))
      
      if enemy.y > 480:
        enemy.x = random.randint(0, 800 - 32)
        enemy.y = -64
        score += 1
        if(score / 5) == 1:
          enemy_amount = enemy_amount + 1
          enemies.append(Enemy(random.randint(0, 800 - 64), -64))

      screen.blit(spike, (enemy.x, enemy.y))
    
    screen.blit(ball, ball_rect)
    water.get_rect().x = water.get_rect().x + 10
    screen.blit(water, (water.get_rect().x, 480 - 85))

    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (4, 4))
    
  pygame.display.update()

pygame.quit()