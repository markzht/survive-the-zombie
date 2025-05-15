import pygame
import random
import math
import os

# FINAL PROJECT: SURVIVE THE ZOMBIES
# 1. Initialize game
#       - initialize pygame, clock, and screen
# 2. Set up constants and variables
# 3. Write classes (Player, Base, Bullet, Zombie, Item)
#       - Player
#           * must move and shoot
#       - Base
#       - Bullet
#           * must move
#       - Zombie
#           * must move
#       - Item
#           * must move
# 4. Write game loop
#       - handle shooting
#       - handle movement
#       - handle collisions (player with item, bullet with zombie, zombie with player, zombie with base)
#       - wave logic [I will help you with this one.]
#       - draw text
# 5. Polish game

# initialize pygame
pygame.init()

# =============
# CONSTANTS
# =============
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

START = "start"
PLAYING = "playing"
CONTROLS = "controls"
PAUSED = "paused"
GAMEOVER = "gameover"
game_state = START

WHITE = (255, 255, 255)

BASE_HP = 100
PLAYER_HP = 20
player_speed = 10
bullet_power = 5
BULLET_SPEED = 15
ITEM_SPEED = 2

# load and scale images
PLAYER_IMAGE = pygame.image.load("assets/images/player.png")
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (70, 70))

ZOMBIE_IMAGE_1 = pygame.image.load("assets/images/zombies/zombie_1.png")
ZOMBIE_IMAGE_1 = pygame.transform.scale(ZOMBIE_IMAGE_1, (70, 90))
ZOMBIE_IMAGE_2 = pygame.image.load("assets/images/zombies/zombie_2.png")
ZOMBIE_IMAGE_2 = pygame.transform.scale(ZOMBIE_IMAGE_2, (70, 90))
ZOMBIE_IMAGE_3 = pygame.image.load("assets/images/zombies/zombie_3.png")
ZOMBIE_IMAGE_3 = pygame.transform.scale(ZOMBIE_IMAGE_3, (70, 90))
ZOMBIE_IMAGE_4 = pygame.image.load("assets/images/zombies/zombie_4.png")
ZOMBIE_IMAGE_4 = pygame.transform.scale(ZOMBIE_IMAGE_4, (70, 90))
ZOMBIE_IMAGE_5 = pygame.image.load("assets/images/zombies/zombie_5.png")
ZOMBIE_IMAGE_5 = pygame.transform.scale(ZOMBIE_IMAGE_5, (70, 90))
ZOMBIE_IMAGE_6 = pygame.image.load("assets/images/zombies/zombie_6.png")
ZOMBIE_IMAGE_6 = pygame.transform.scale(ZOMBIE_IMAGE_6, (70, 90))
ZOMBIE_IMAGE_7 = pygame.image.load("assets/images/zombies/zombie_7.png")
ZOMBIE_IMAGE_7 = pygame.transform.scale(ZOMBIE_IMAGE_7, (70, 90))

BASE_IMAGE = pygame.image.load("assets/images/base.png")
BASE_IMAGE = pygame.transform.scale(BASE_IMAGE, (SCREEN_WIDTH + 35, 90))

BACKGROUND_IMAGE = pygame.image.load("assets/images/background.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

SPEED_ITEM_IMAGE = pygame.image.load("assets/images/items/speed_item.png")
SPEED_ITEM_IMAGE = pygame.transform.scale(SPEED_ITEM_IMAGE, (30, 30))
HEAL_ITEM_IMAGE = pygame.image.load("assets/images/items/heal_item.png")
HEAL_ITEM_IMAGE = pygame.transform.scale(HEAL_ITEM_IMAGE, (30, 30))
BULLET_ITEM_IMAGE = pygame.image.load("assets/images/items/bullet_item.png")
BULLET_ITEM_IMAGE = pygame.transform.scale(BULLET_ITEM_IMAGE, (35, 20))
BRICK_ITEM_IMAGE = pygame.image.load("assets/images/items/brick_item.png")
BRICK_ITEM_IMAGE = pygame.transform.scale(BRICK_ITEM_IMAGE, (40, 30))

# load sounds
ZOMBIE_SCREAM_SOUND = pygame.mixer.Sound("assets/sounds/zombie_scream.mp3")
PLAYER_DAMAGE_SOUND = pygame.mixer.Sound("assets/sounds/player_damage.mp3")
BASE_DAMAGE_SOUND = pygame.mixer.Sound("assets/sounds/base_damage.mp3")
PICKUP_ITEM_SOUND = pygame.mixer.Sound("assets/sounds/pickup_item.mp3")

# load and play background music
pygame.mixer.music.load("assets/sounds/background.mp3")  
pygame.mixer.music.play(-1)

# dictionary of zombie types
ZOMBIE_TYPES = {
    "normal": {"hp": 20, "atk": 3, "speed": 0.7, "image": ZOMBIE_IMAGE_1},
    "slow": {"hp": 30, "atk": 5, "speed": 0.2, "image": ZOMBIE_IMAGE_2},
    "strong": {"hp": 55, "atk": 10, "speed": 0.4, "image": ZOMBIE_IMAGE_3},
    "drop_speed": {"hp": 20, "atk": 3, "speed": 0.5, "image": ZOMBIE_IMAGE_4},
    "drop_heal": {"hp": 20, "atk": 3, "speed": 0.5, "image": ZOMBIE_IMAGE_5},
    "drop_bullet": {"hp": 20, "atk": 3, "speed": 0.5, "image": ZOMBIE_IMAGE_6},
    "drop_brick": {"hp": 20, "atk": 3, "speed": 0.5, "image": ZOMBIE_IMAGE_7},
}

# dictionary of item types
ITEM_TYPES = {
    "speed": {"image": SPEED_ITEM_IMAGE},
    "heal": {"image": HEAL_ITEM_IMAGE},
    "bullet": {"image": BULLET_ITEM_IMAGE},
    "brick": {"image": BRICK_ITEM_IMAGE},
}

# initialize clock and screen
clock = pygame.time.Clock()     
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont(None, 36)
pygame.display.set_caption("Survive the Zombies")

# =============
# FUNCTIONS
# =============
HIGHSCORE_FILE = "highscore.txt"
# Load current high score. Nikki will help you with this one.
def load_highscore():
    # Check if the file exists. If it doesn't return 0
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    
    # Open file and read the first line. Return the first score
    with open(HIGHSCORE_FILE, "r") as file:
        line = file.readline()
        stripped_line = line.strip()

        if stripped_line.isdigit():
            return int(stripped_line)
        else:
            return 0
        
# Log current high score. Nikki will help you with this one.
def log_highscore():
    current_highscore = load_highscore()

    # If new high score is greater than current high score,
    if player.points > current_highscore:
        # Write new score into file
        with open(HIGHSCORE_FILE, "w") as file:
            file.write(f"{player.points}\n")

# draw text
def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def reset_game():
    global player, base, wave, player_speed, bullet_power

    wave = 0
    player_speed = 10
    bullet_power = 5 

    all_sprites.empty()
    bullets.empty()
    items.empty()
    zombies.empty()

    player = Player()
    base = Base()
    
    all_sprites.add(player)
    all_sprites.add(base)

# =============
# CLASSES
# =============
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # initialize sprite class

        # set up player's image and rect
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 115))
        self.facing_right = True
        
        # set up player's stats
        self.hp = PLAYER_HP
        self.points = 0

    def move(self, keys):
        # if player presses left arrow and is in screen, move to left
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= player_speed
            # make player look to the left
            if self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_right = False
        # if player presses right arrow and is in screen, move to right
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += player_speed
            # make player look to the right
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_right = True

    def shoot(self):
        # create bullet at center and top of player when player shoots
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Base(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # set up base image and rect
        self.image = BASE_IMAGE
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        
        # set up base stats
        self.base_hp = BASE_HP

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # set up bullet image and rect
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.rect.y -= BULLET_SPEED
        # delete bullet if it hits top of screen
        if self.rect.bottom < 0:
            self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, z_type, x):
        super().__init__()

        rand_y = random.randint(-200, 50) # pick random y for zombie

        # set up zombie's image and rect
        self.image = ZOMBIE_TYPES[z_type]["image"]
        self.rect = self.image.get_rect(topleft=(x, rand_y))
        self.y = float(self.rect.y)  # store y-position as a float

        # set up zombie's stats
        self.type = z_type
        self.hp = ZOMBIE_TYPES[z_type]["hp"]
        self.atk = ZOMBIE_TYPES[z_type]["atk"]
        self.speed = ZOMBIE_TYPES[z_type]["speed"]

    def update(self):
        self.y += self.speed # add speed to y
        self.rect.y = int(self.y) # update actual rect position
        # if zombie reaches bottom of screen,
        if self.rect.top > SCREEN_HEIGHT:
            base.base_hp -= self.atk
            self.kill()

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()

        self.type = type

        # set up item's image and rect
        self.image = ITEM_TYPES[self.type]["image"]
        self.rect = self.image.get_rect(center=(x, y))

    # Move item toward player (kinda like a magnet).
    def move(self):
        if self.rect.top < SCREEN_HEIGHT - 80:
            # Calculate direction to player.
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:  # Prevent division by zero.
                self.rect.x += (dx / distance) * ITEM_SPEED
                self.rect.y += (dy / distance) * ITEM_SPEED
        
        
# sprite groups
bullets = pygame.sprite.Group()
items = pygame.sprite.Group()
zombies = pygame.sprite.Group()
player = Player()
base = Base()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(base)

wave = 0
running = True

# =============
# GAME LOOP
# =============
while running:
    screen.blit(BACKGROUND_IMAGE, (0, 0)) # clear previous frame by drawing background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = PLAYING
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                # shoot if player presses spacebar
                if event.key == pygame.K_SPACE:
                    player.shoot()
                # pause game if player presses p
                elif event.key == pygame.K_p:
                    game_state = PAUSED
                elif event.key == pygame.K_c:
                    game_state = CONTROLS
        elif game_state == PAUSED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                game_state = PLAYING
        elif game_state == CONTROLS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                game_state = PLAYING
        elif game_state == GAMEOVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()
                game_state = PLAYING

    # ======== START SCREEN ========
    if game_state == START:
        draw_text("SURVIVAL THE ZOMBIES", SCREEN_WIDTH // 2 - 135, SCREEN_HEIGHT // 2 - 50)
        draw_text("Press ENTER to start", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10)

    # ======== PAUSE SCREEN ========
    elif game_state == PAUSED:
        draw_text("PAUSED", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 40)
        draw_text("Press P to resume", SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20)
    # ======== CONTROLS SCREEN ========
    elif game_state == CONTROLS:
        draw_text("CONTROLS", SCREEN_WIDTH // 2 - 70, 80)
        draw_text("RIGHT / LEFT ARROW - move", SCREEN_WIDTH // 2 - 180, 150)
        draw_text("SPACE - shoot", SCREEN_WIDTH // 2 - 180, 190)
        draw_text("LEFT SHIFT - collect items", SCREEN_WIDTH // 2 - 180, 230)
        draw_text("P - pause", SCREEN_WIDTH // 2 - 180, 270)
        draw_text("Press C to go back", SCREEN_WIDTH // 2 - 180, 370)
    # ======== GAME PLAY SCREEN ========
    elif game_state == PLAYING:
        # move items if player presses left shift
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            for item in items:
                item.move()

        player.move(keys) # move player
        all_sprites.update() # call update method of all sprites

        # player collision with item
        items_collected = pygame.sprite.spritecollide(player, items, True)
        for item in items_collected:
            PICKUP_ITEM_SOUND.play()
            if item.type == "speed":
                if player_speed < 15:
                    player_speed += 1
            if item.type == "heal":
                if player.hp <= PLAYER_HP - 5:
                    player.hp += 5
                else:
                    player.hp += PLAYER_HP - player.hp
            if item.type == "bullet":
                if bullet_power < 50:
                    bullet_power += 1 
            if item.type == "brick":
                if base.base_hp <= BASE_HP - 5:
                    base.base_hp += 5
                else:
                    base.base_hp += BASE_HP - base.base_hp

        # bullet collision with zombies
        for bullet in bullets:
            hit_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
            for zombie in hit_zombies:
                zombie.hp -= bullet_power
                bullet.kill()
                # if zombie has no more hp
                if zombie.hp <= 0:
                    ZOMBIE_SCREAM_SOUND.play()
                    # if zombie is a drop zombie, create the item
                    if zombie.type == "drop_speed":
                        item = Item(zombie.rect.centerx, zombie.rect.centery, "speed")
                        items.add(item)
                        all_sprites.add(item)
                    if zombie.type == "drop_heal":
                        item = Item(zombie.rect.centerx, zombie.rect.centery, "heal")
                        items.add(item)
                        all_sprites.add(item)
                    if zombie.type == "drop_bullet":
                        item = Item(zombie.rect.centerx, zombie.rect.centery, "bullet")
                        items.add(item)
                        all_sprites.add(item)
                    if zombie.type == "drop_brick":
                        item = Item(zombie.rect.centerx, zombie.rect.centery, "brick")
                        items.add(item)
                        all_sprites.add(item)
                    zombie.kill() # delete zombie
                    player.points += 1

        # zombie collision with player
        zombies_attacking_player = pygame.sprite.spritecollide(player, zombies, True)
        for zombie in zombies_attacking_player:
            PLAYER_DAMAGE_SOUND.play()
            player.hp -= zombie.atk
            # end game if player has no more hp
            if player.hp <= 0:
                game_state = GAMEOVER
                log_highscore()

        # zombie collision with base
        zombies_at_base = pygame.sprite.spritecollide(base, zombies, dokill=True)
        for zombie in zombies_at_base:
            BASE_DAMAGE_SOUND.play()
            base.base_hp -= zombie.atk
            # end game if base has no more hp
            if base.base_hp <= 0:
                game_state = GAMEOVER
                log_highscore()

        # Wave Logic
        # Once no more zombies in the wave are alive, start the next wave.
        if len(zombies) == 0:
            wave += 1
            # Number of zombies in the wave equals the wave number.
            for i in range(wave):
                x_position = random.randint(0, SCREEN_WIDTH - 40)  # Pick a random x-position for zombie.
                # For level 5 or less, only generate strong zombies.
                if wave < 5:
                    zombie_type = "strong"
                # For level 10 or less, generate zombies in following list with different probabilities.
                elif wave < 10:
                    zombie_type = random.choices(
                        ["strong", "normal", "drop_speed", "drop_heal", "drop_brick"], 
                        weights=[3, 3, 2, 2, 2],
                        k=1
                    )[0]
                elif wave < 15:
                    zombie_type = random.choices(
                        ["strong", "normal", "drop_speed", "drop_heal", "drop_brick", "drop_bullet"], 
                        weights=[3, 3, 2, 2, 2, 4],
                        k=1
                    )[0]
                # For levels over 15, generate all zombies where non-drop zombies are 5x more likely to be generated than drop zombies.
                else:
                    zombie_type = random.choices(
                        list(ZOMBIE_TYPES.keys()), 
                        weights=[5 if not z.startswith("drop_") else 1 for z in ZOMBIE_TYPES.keys()],
                        k=1
                    )[0]
                zombie = Zombie(zombie_type, x_position)
                all_sprites.add(zombie)
                zombies.add(zombie)

        all_sprites.draw(screen)  # draw all sprites after clearing the previous frame

        # draw text on screen
        draw_text(f'Base HP: {base.base_hp}', 10, 10)
        draw_text(f'Points: {player.points}', 10, 35)
        draw_text(f'Wave: {wave}', 10, 60)
        draw_text(f'HP: {player.hp}', 10, 100)
        draw_text(f'Speed: {player_speed}', 10, 125)
        draw_text(f'Power: {bullet_power}', 10, 150)

    # ======== GAME OVER SCREEN ========
    elif game_state == GAMEOVER:
        draw_text("GAME OVER", SCREEN_WIDTH // 2 - 80, 120)
        draw_text(f"Final Score: {player.points}", SCREEN_WIDTH // 2 - 80, 200)
        draw_text("Your High Score", SCREEN_WIDTH // 2 - 90, 250)

        score = load_highscore()
        draw_text(f"{score}", SCREEN_WIDTH // 2, 330)

        draw_text("Press ENTER to start", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 140)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

