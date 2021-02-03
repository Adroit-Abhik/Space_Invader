import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

# load assets
# Enemy
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


# General ship class for player and enemy
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# Player ship class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


# Enemy ship class
class Enemy(Ship):
    COLOR_MAP = {
        "red" : (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    lives = 5
    level = 0

    # Player
    player = Player(300, 630)
    player_vel = 5
    lost = False
    lost_count = 0

    # Enemy
    enemies = []
    wave_length = 5
    enemy_vel = 1

    # drawing and updating game attributes
    def redraw_window():
        WIN.blit(BG, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # drawing player ship
        player.draw(WIN)

        # drawing enemy ships
        for enemy in enemies:
            enemy.draw(WIN)

        # Rendering lost label
        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))


        pygame.display.update()

    # main game loop to track
    while run:
        clock.tick(FPS)
        redraw_window()

        # Player Lost logic
        if lives <= 0 or player.health <= 0:
            lives = 0
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

        # creating enemy ships if player beats the current wave or beginning of the game
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Player ship movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel

        # Enemy Movement, shooting, and destruction
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


main()
