import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Operius-like Game")

# Load sprites
player_image = pygame.image.load("player.png")
bullet_image = pygame.image.load("bullet.png")
enemy_image = pygame.image.load("enemy.png")

# Resize images to desired dimensions if necessary
player_size = 50
player_image = pygame.transform.scale(player_image, (player_size, player_size))

bullet_width, bullet_height = 5, 10
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))

enemy_size = 50
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

# Player settings
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100
player_speed = 5

# Bullet settings
bullets = []
bullet_speed = -10

# Enemy settings
enemies = []
enemy_speed = 2
enemies_destroyed = 0

# Game loop settings
clock = pygame.time.Clock()
running = True
level = 1
score = 0
level_up_display = False
level_up_timer = 0
level_up_duration = 60  # frames to display "Level Up!"

# Font for displaying text
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

def spawn_enemy():
    x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
    enemies.append(pygame.Rect(x_pos, 0, enemy_size, enemy_size))

# Main game loop
while running:
    screen.fill((0, 0, 0))  # Clear screen with black color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire bullet
                bullet_rect = bullet_image.get_rect(center=(player_x + player_size // 2, player_y))
                bullets.append(bullet_rect)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
        player_x += player_speed

    # Move bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Spawn enemies periodically
    if random.randint(1, 30) == 1:
        spawn_enemy()

    # Move enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # Collision detection
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10  # Increase score for each destroyed enemy
                enemies_destroyed += 1
                break
        if enemy.colliderect(pygame.Rect(player_x, player_y, player_size, player_size)):
            running = False  # End game on collision with player

    # Level Up
    if enemies_destroyed >= 10:
        level += 1
        enemies_destroyed = 0
        enemy_speed += 1  # Increase difficulty
        level_up_display = True
        level_up_timer = pygame.time.get_ticks()  # Start timer for level up display

    # Draw player
    player_rect = player_image.get_rect(topleft=(player_x, player_y))
    screen.blit(player_image, player_rect)

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_image, bullet)

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw level
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (SCREEN_WIDTH - 120, 10))

    # Display "Level Up!" message briefly
    if level_up_display:
        level_up_message = large_font.render("Level Up!", True, (255, 255, 0))
        screen.blit(level_up_message, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        if pygame.time.get_ticks() - level_up_timer > level_up_duration * (1000 / 60):
            level_up_display = False

    # Update display and set frame rate
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
