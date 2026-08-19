import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((350, 600))
clock = pygame.time.Clock()

# constants:
TILESIZE = 32

# floor:
floor_image = pygame.image.load('assets/floor.png').convert_alpha()
floor_image = pygame.transform.scale(floor_image, (TILESIZE*15, TILESIZE*5))
floor_rect = floor_image.get_rect(bottomleft = (0, screen.get_height()))

# player:
player_image = pygame.image.load('assets/player_static.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (TILESIZE, TILESIZE*2))

running = True

def draw(): 
  screen.fill('lightblue')
  screen.blit(floor_image, floor_rect)
  screen.blit(player_image, (175, 300))

# game loop:
while running: 

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()  
      sys.exit()

  draw()

  clock.tick(60)

  pygame.display.update()