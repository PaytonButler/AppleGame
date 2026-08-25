import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((350, 600))
clock = pygame.time.Clock()

class Apple:
  def __init__(self, image, position, speed):
    self.image = image
    self.rect = self.image.get_rect(topleft = position)
    self.speed = speed

  def move(self):
    self.rect.y += self.speed


class Bomb:
  def __init__(self, image, position, speed):
    self.image = image
    self.rect = self.image.get_rect(topleft = position)
    self.speed = speed

  def move(self):
    self.rect.y += self.speed

# variables:
speed = 3
score = 0
game_over = False


# constants:
TILESIZE = 32

# floor:
floor_image = pygame.image.load('assets/floor.png').convert_alpha()
floor_image = pygame.transform.scale(floor_image, (TILESIZE*15, TILESIZE*5))
floor_rect = floor_image.get_rect(bottomleft = (0, screen.get_height()))

# player:
player_image = pygame.image.load('assets/player_static.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (TILESIZE, TILESIZE*2))
player_rect = player_image.get_rect(center = (screen.get_width()/2,
                                              screen.get_height()-floor_image.get_height()-(player_image.get_height()/2)))

# apple:
apple_image = pygame.image.load('assets/apple.png').convert_alpha()
apple_image = pygame.transform.scale(apple_image, (TILESIZE, TILESIZE))

# bomb:
bomb_image = pygame.image.load('assets/bomb.png').convert_alpha()
bomb_image = pygame.transform.scale(bomb_image, (TILESIZE, TILESIZE))

apples = [
  Apple(apple_image, (100,0), 3),
  Apple(apple_image, (300,0), 3),
]

bombs = [
  Bomb(bomb_image, (50,0), 3)
]


# fonts:
font = pygame.font.Font('assets/PixeloidMono.ttf', TILESIZE//2)

# sound effects:
pickup = pygame.mixer.Sound('assets/powerup.mp3')
pickup.set_volume(0.1)


running = True

def update():
  global speed
  global score
  global running
  global game_over

  keys = pygame.key.get_pressed()

  if keys[pygame.K_LEFT]:
    player_rect.x -= 8
  if keys[pygame.K_RIGHT]:
    player_rect.x += 8


# keep player within bounds:
  if player_rect.left < 0:
    player_rect.left = 0
  if player_rect.right > screen.get_width():
    player_rect.right = screen.get_width()

  # apple movement:
  for apple in apples:
    apple.move()

    if apple.rect.colliderect(floor_rect):
      apples.remove(apple)
      apples.append(Apple(apple_image, (random.randint(50, 300), -50), speed))
    elif apple.rect.colliderect(player_rect):      
      apples.remove(apple)      
      apples.append(Apple(apple_image, (random.randint(50, 300), -50), speed))
      speed += 0.1
      score += 1
      pickup.play()


  # bomb movement:
  for bomb in bombs:
    bomb.move()

    if bomb.rect.colliderect(floor_rect):
      bombs.remove(bomb)
      bombs.append(Bomb(bomb_image, (random.randint(50,300), -50), speed))
    elif bomb.rect.colliderect(player_rect):
      game_over = True


def game_end():
  # Create a semi-transparent surface matching the screen size
  overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
  
  # Fill with red and 150 alpha (0 = invisible, 255 = solid)
  overlay.fill((255, 0, 0, 150)) 
  
  # Draw the overlay over the existing, frozen game visuals
  screen.blit(overlay, (0, 0))
  
  # Render both texts
  game_over_text = font.render("GAME OVER", True, "white")
  final_score = font.render(f'Score: {score}', True, "white")
  
  # Position Game Over exactly in the center of the screen
  game_over_rect = game_over_text.get_rect(center = screen.get_rect().center)
  
  # Snap the top of the Score text 20 pixels below the bottom of Game Over
  final_rect = final_score.get_rect(midtop = (screen.get_width() // 2, game_over_rect.bottom + 20))
  
  # Draw both to the screen
  screen.blit(game_over_text, game_over_rect)
  screen.blit(final_score, final_rect)




def draw(): 
  screen.fill('lightblue')
  screen.blit(floor_image, floor_rect)
  screen.blit(player_image, player_rect)

  for apple in apples:
    screen.blit(apple.image, apple.rect)

  for bomb in bombs:
    screen.blit(bomb_image, bomb.rect)

  score_text = font.render(f'Score: {score}', True, "white")
  screen.blit(score_text, (5,5))



# game loop:
while running: 

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()  
      sys.exit()

  if game_over is False:
    update()
    draw()
  elif game_over is True:
    draw()
    game_end()


  clock.tick(60)

  pygame.display.update()