import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((350, 600))
clock = pygame.time.Clock()

# constants:
TILESIZE = 32

# fonts:
font = pygame.font.Font('assets/PixeloidMono.ttf', TILESIZE//2)

# sound effects:
pickup = pygame.mixer.Sound('assets/powerup.mp3')
pickup.set_volume(0.1)

explode = pygame.mixer.Sound('assets/explosion.mp3')
explode.set_volume(0.1)

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

# high score storage:
try:
    with open("hs.txt", "r") as file:
        high_score = int(file.read())
except (FileNotFoundError, ValueError):
    # default to 0 if the file doesn't exist, is empty, or is corrupted
    high_score = 0 



# variables:
speed = 3
score = 0
game_over = False
new_hs = False
game_over_timer = 0
EXPLOSION_DELAY = 20

# floor:
floor_image = pygame.image.load('assets/floor.png').convert_alpha()
floor_image = pygame.transform.scale(floor_image, (TILESIZE*15, TILESIZE*5))
floor_rect = floor_image.get_rect(bottomleft = (-20, screen.get_height()))

# player:
player_image = pygame.image.load('assets/basket.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (TILESIZE*1.5, TILESIZE))
player_rect = player_image.get_rect(center = (screen.get_width()/2,
                                              screen.get_height()-floor_image.get_height()-(player_image.get_height()/2)))

# apple:
apple_image = pygame.image.load('assets/apple.png').convert_alpha()
apple_image = pygame.transform.scale(apple_image, (TILESIZE, TILESIZE))

# bomb:
bomb_image = pygame.image.load('assets/regular_bomb.png').convert_alpha()
bomb_image = pygame.transform.scale(bomb_image, (TILESIZE, TILESIZE))

# explosion:
explosion_image = pygame.image.load('assets/exploded.png').convert_alpha()
explosion_image = pygame.transform.scale(explosion_image, (TILESIZE, TILESIZE))

# buttons:
retry_button = font.render(f"Try Again", True, "white")
quit_button = font.render(f"Quit Game", True, "white")
retry_button_rect = retry_button.get_rect(center = (-100, -100))
quit_button_rect = quit_button.get_rect(center = (-100, -100))


apples = [
  Apple(apple_image, (100,0), 3),
  Apple(apple_image, (300,0), 3),
]

bombs = [
  Bomb(bomb_image, (50,0), 3)
]

running = True
mouse_pos = (0,0)

def update():
  global speed
  global score
  global running
  global game_over
  global game_over_timer

  keys = pygame.key.get_pressed()

# player movement:
  if keys[pygame.K_LEFT]:
    player_rect.x -= 8
  if keys[pygame.K_RIGHT]:
    player_rect.x += 8
    
# alternate player movement:
  if keys[pygame.K_a]:
    player_rect.x -= 8
  if keys[pygame.K_d]:
    player_rect.x += 8



# keep player within bounds with smooth screen wrapping
  if player_rect.right < 0:
    player_rect.left = screen.get_width()
  if player_rect.left > screen.get_width():
    player_rect.right = 0


# apple movement:
  for apple in apples:
    apple.move()

    if apple.rect.colliderect(floor_rect):
      apples.remove(apple)
      apples.append(Apple(apple_image, (random.randint(50, 300), -50), speed))
      if score > 0:
        score -= 1
      speed -= 0.05
    elif apple.rect.colliderect(player_rect):      
      apples.remove(apple)      
      apples.append(Apple(apple_image, (random.randint(50, 300), -50), speed))
      speed += 0.1
      score += 2
      pickup.play()


# bomb movement:
  for bomb in bombs:
    bomb.move()

    if bomb.rect.colliderect(floor_rect):
      bombs.remove(bomb)
      bombs.append(Bomb(bomb_image, (random.randint(50,300), -50), speed))
    elif bomb.rect.colliderect(player_rect):
      bomb.image = explosion_image
      explode.play()
      game_over = True
      game_over_timer = EXPLOSION_DELAY




# game-over screen:
def game_end():
  global retry_button_rect
  global quit_button_rect
  
  overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
  overlay.fill((255, 0, 0, 150)) 
  screen.blit(overlay, (0, 0))

  game_over_text = font.render("GAME OVER", True, "white")
  final_score_text = font.render("Final Score:", True, "white")
  score_font = pygame.font.Font('assets/PixeloidMono.ttf', 32)
  final_score_num = score_font.render(f'{score}', True, "white")
  score_rect = final_score_num.get_rect(center=(175, 150))
  hs_text = font.render("New High Score!", True, "white")
  
  game_over_rect = game_over_text.get_rect(center = (screen.get_width() // 2, screen.get_height() - 550))
  final_score_rect = final_score_text.get_rect(midtop = (screen.get_width() // 2, game_over_rect.bottom + 20))
  high_score_rect = hs_text.get_rect(midtop = (screen.get_width() // 2, retry_button_rect.top - 40))

  retry_button_rect.midtop = (screen.get_width() // 2, final_score_rect.bottom + 200)
  quit_button_rect.midtop = (screen.get_width() // 2, retry_button_rect.bottom + 20)

  retry_bg_rect = retry_button_rect.inflate(20, 10)
  quit_bg_rect = quit_button_rect.inflate(20, 10)

  pygame.draw.rect(screen, (211, 211, 211), retry_bg_rect, border_radius = 6)
  pygame.draw.rect(screen, (211, 211, 211), quit_bg_rect, border_radius=6)

  pygame.draw.rect(screen, "white", retry_bg_rect, width=2, border_radius=6)
  pygame.draw.rect(screen, "white", quit_bg_rect, width=2, border_radius=6)

  screen.blit(game_over_text, game_over_rect)
  screen.blit(final_score_text, final_score_rect)
  screen.blit(final_score_num, score_rect)
  if new_hs:
    screen.blit(hs_text, high_score_rect)
  screen.blit(retry_button, retry_button_rect)
  screen.blit(quit_button, quit_button_rect)



# resets score and mechanics when retry is clicked:
def reset_game():
  global game_over, score, speed, apples, bombs, player_rect, new_hs

  game_over = False
  score = 0
  speed = 3
  new_hs = False

  player_rect.center = (screen.get_width()/2,
                         screen.get_height()-floor_image.get_height()-(player_image.get_height()/2))

  apples = [
    Apple(apple_image, (100,0), speed),
    Apple(apple_image, (300,0), speed),
  ]

  bombs = [
    Bomb(bomb_image, (50,0), speed)
  ]


def draw(): 
  screen.fill('#63CFF7')
  screen.blit(floor_image, floor_rect)
  screen.blit(player_image, player_rect)

  for apple in apples:
    screen.blit(apple.image, apple.rect)

  for bomb in bombs:
    screen.blit(bomb.image, bomb.rect)

  hs_text = font.render(f'High Score: {high_score}', True, "white")
  screen.blit(hs_text, (5,575))


  score_font = pygame.font.Font('assets/PixeloidMono.ttf', 32)
  score_text = score_font.render(f'{score}', True, "white")
  score_rect = score_text.get_rect(center=(175, 150))
  screen.blit(score_text, score_rect)

# game loop:
while running: 

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      hs_str = str(high_score)
      with open("hs.txt", "w") as file:
        file.write(hs_str)
      pygame.quit()  
      sys.exit()

    if event.type == pygame.MOUSEBUTTONUP:
      mouse_pos = event.pos
      if game_over:
        if retry_button_rect.collidepoint(mouse_pos):
          reset_game()
        elif quit_button_rect.collidepoint(mouse_pos):
          hs_str = str(high_score)
          with open("hs.txt", "w") as file:
            file.write(hs_str)
          pygame.quit()
          sys.exit()


  if game_over is False:
    update()
    draw()
  elif game_over is True:
    if score > high_score:
        new_hs = True
        high_score = score
    draw()
    if game_over_timer > 0:
        game_over_timer -= 1
    else:
        game_end()


  clock.tick(60)

  pygame.display.update()