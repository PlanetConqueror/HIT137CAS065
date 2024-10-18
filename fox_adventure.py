#https://github.com/PlanetConqueror/HIT137CAS065

import pygame
import random

pygame.init()

# Screen dimensions and constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Game variables
GRAVITY = 1
PLAYER_SPEED = 7
JUMP_STRENGTH = 30
PROJECTILE_SPEED = 10
ENEMY_SPEED = 2
BOSS_SPEED = 1
PLAYER_LIVES = 3
PLAYER_HEALTH = 100
LEVEL_COUNT = 3
SCORE_TO_NEXT_LEVEL = 500
BOSS_HEALTH = 30
BOSS_KNOCKBACK = 10

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fox Adventure")

# Clock to control game speed
clock = pygame.time.Clock()

# Fonts for displaying text (score, health, etc.)
font = pygame.font.SysFont(None, 36)

# Initialize the Pygame mixer for sound
pygame.mixer.init()

# Load sound files
shoot_sound = pygame.mixer.Sound('shoot.wav')
fail_sound = pygame.mixer.Sound('fail.wav')
collect_sound = pygame.mixer.Sound('collect.wav')
win_sound = pygame.mixer.Sound('win.wav')
background_music = 'game_sound.wav'

# Start background music
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Loops the background music indefinitely

# Camera class to follow the player smoothly
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, SCREEN_HEIGHT - 150
        self.speed_x = 0
        self.speed_y = 0
        self.jumping = False
        self.health = PLAYER_HEALTH
        self.lives = PLAYER_LIVES
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED
        else:
            self.speed_x = 0

        if not self.jumping:
            if keys[pygame.K_SPACE]:
                self.jumping = True
                self.speed_y = -JUMP_STRENGTH

        self.speed_y += GRAVITY
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.jumping = False

    # Play shoot sound and shoot a projectile
    def shoot(self):
        pygame.mixer.Sound.play(shoot_sound)  # Play shooting sound
        projectile = Projectile(self.rect.centerx, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = PROJECTILE_SPEED

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100)
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.speed_x = speed

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

# Boss enemy class
class BossEnemy(Enemy):
    def __init__(self):
        super().__init__(BOSS_SPEED)
        self.image = pygame.Surface((150, 150))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.health = BOSS_HEALTH

    def take_damage(self):
        self.health -= 1
        pygame.mixer.Sound.play(hit_sound)  # Play hit sound when boss is hit
        if self.health <= 0:
            pygame.mixer.Sound.play(win_sound)  # Play win sound when boss is defeated
            self.kill()
        else:
            self.rect.x = max(0, self.rect.x - BOSS_KNOCKBACK)

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        if type == "health":
            self.image.fill(GREEN)
        elif type == "life":
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type = type

    def apply_effect(self, player):
        pygame.mixer.Sound.play(collect_sound)  # Play collect sound when item is picked up
        if self.type == "health":
            player.health = min(player.health + 20, PLAYER_HEALTH)
        elif self.type == "life":
            player.lives += 1

# Game loop variables and sprite groups
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

camera = Camera(SCREEN_WIDTH * 2, SCREEN_HEIGHT)

current_level = 1
boss_defeated = False
game_over = False
enemy_spawn_rate = 0.02
boss_health_display = 0

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.shoot()

    if not game_over:
        all_sprites.update()
        camera.update(player)

        # Projectile-enemy collision
        for projectile in projectiles:
            enemy_hit = pygame.sprite.spritecollideany(projectile, enemies)
            if enemy_hit:
                projectile.kill()
                if isinstance(enemy_hit, BossEnemy):
                    enemy_hit.take_damage()
                    boss_health_display = enemy_hit.health
                    if enemy_hit.health <= 0:
                        player.score += 1000
                        boss_defeated = True
                        game_over = True
                else:
                    enemy_hit.kill()
                    player.score += 10

        # Player-enemy collision
        enemy_hit_player = pygame.sprite.spritecollideany(player, enemies)
        if enemy_hit_player:
            player.health -= 50
            enemy_hit_player.kill()

        # Health and lives check
        if player.health <= 0:
            pygame.mixer.Sound.play(fail_sound)  # Play fail sound when the player dies
            player.lives -= 1
            player.health = PLAYER_HEALTH
            if player.lives <= 0:
                game_over = True

        # Handle boss fight
        if current_level == LEVEL_COUNT and not boss_defeated:
            if not any(isinstance(e, BossEnemy) for e in enemies):
                boss = BossEnemy()
                all_sprites.add(boss)
                enemies.add(boss)
                boss_health_display = boss.health
                enemy_spawn_rate = 0.005

        # Spawn enemies and collectibles
        if random.random() < enemy_spawn_rate:
            enemy = Enemy(ENEMY_SPEED + current_level)
            all_sprites.add(enemy)
            enemies.add(enemy)

        if random.random() < 0.008:
            collectible = Collectible(random.randint(100, SCREEN_WIDTH * 2 - 100), random.randint(100, SCREEN_HEIGHT - 100), "health")
            all_sprites.add(collectible)
            collectibles.add(collectible)
        elif random.random() < 0.002:
            collectible = Collectible(random.randint(100, SCREEN_WIDTH * 2 - 100), random.randint(100, SCREEN_HEIGHT - 100), "life")
            all_sprites.add(collectible)
            collectibles.add(collectible)

        collectible_hit = pygame.sprite.spritecollideany(player, collectibles)
        if collectible_hit:
            collectible_hit.apply_effect(player)
            collectible_hit.kill()

        # Check for level progression
        if player.score >= SCORE_TO_NEXT_LEVEL * current_level and current_level < LEVEL_COUNT:
            current_level += 1
            enemy_spawn_rate += 0.01
            ENEMY_SPEED += 1

    # Drawing phase
    screen.fill(WHITE)

    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    # Display player's score, health, and lives
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    health_text = font.render(f"Health: {player.health}", True, BLACK)
    lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
    level_text = font.render(f"Level: {current_level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))
    screen.blit(lives_text, (10, 70))
    screen.blit(level_text, (10, 100))

    if boss_health_display > 0:
        boss_health_text = font.render(f"Boss Health: {boss_health_display}", True, BLACK)
        screen.blit(boss_health_text, (SCREEN_WIDTH - 200, 10))

    if game_over:
        if boss_defeated:
            game_over_text = font.render("You won! Press R to restart", True, GREEN)
        else:
            game_over_text = font.render("GAME OVER! Press R to restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            current_level = 1
            player.lives = PLAYER_LIVES
            player.health = PLAYER_HEALTH
            player.score = 0
            boss_defeated = False
            enemy_spawn_rate = 0.02
            ENEMY_SPEED = 2
            all_sprites.empty()
            all_sprites.add(player)

    pygame.display.flip()

pygame.quit()
