import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Player settings
PLAYER_SIZE = 50
PLAYER_COLOR = (0, 255, 0)
player_pos = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]
player_speed = 10

# Enemy settings
ENEMY_SIZE = 50
ENEMY_COLOR = (255, 0, 0)
enemies = []
enemy_speed = 5

# Bullet settings
BULLET_SIZE = 20
BULLET_COLOR = (255, 255, 255)
bullets = []
bullet_speed = 10

# Special power variables
rapid_fire_active = False
shield_active = False
rapid_fire_timer = 0
shield_timer = 0

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize clock
clock = pygame.time.Clock()

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game with Special Powers")

# Score
score = 0
score_font = pygame.font.SysFont("consolas", 30)

# Load background image and background music
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pygame.mixer.music.load("516010__enviromaniac2__super-mario-bros-theme-techno-loop.mp3")
pygame.mixer.music.play(-1)  # Play the background music in a loop

# Load the game over sound
game_over_sound = pygame.mixer.Sound("game-over-160612.mp3")

def create_enemy():
    x_pos = random.randint(0, WIDTH - ENEMY_SIZE)
    y_pos = 0
    enemies.append([x_pos, y_pos])

def create_bullet():
    bullets.append([player_pos[0] + PLAYER_SIZE // 2, player_pos[1]])

def update_positions():
    global score

    # Update bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

        # Check for collision between bullet and enemy
        for bullet in bullets[:]:
            if enemy[0] < bullet[0] < enemy[0] + ENEMY_SIZE and \
               enemy[1] < bullet[1] < enemy[1] + ENEMY_SIZE:
                bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 1

def check_collision():
    for enemy in enemies:
        if (enemy[0] < player_pos[0] < enemy[0] + ENEMY_SIZE or
            enemy[0] < player_pos[0] + PLAYER_SIZE < enemy[0] + ENEMY_SIZE) and \
           (enemy[1] < player_pos[1] < enemy[1] + ENEMY_SIZE or
            enemy[1] < player_pos[1] + PLAYER_SIZE < enemy[1] + ENEMY_SIZE):
            return True
    return False

def draw_objects():
    # Draw the background image
    win.blit(background_image, (0, 0))

    pygame.draw.rect(win, PLAYER_COLOR, pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

    for bullet in bullets:
        pygame.draw.rect(win, BULLET_COLOR, pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))

    for enemy in enemies:
        pygame.draw.rect(win, ENEMY_COLOR, pygame.Rect(enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE))

    # Show active powers
    if rapid_fire_active:
        rapid_fire_text = score_font.render("Rapid Fire Active", True, WHITE)
        win.blit(rapid_fire_text, (WIDTH - 200, 10))

    if shield_active:
        shield_text = score_font.render("Shield Active", True, WHITE)
        win.blit(shield_text, (WIDTH - 200, 30))

    score_text = score_font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

def game_over_screen():
    global score
    # Play the game over sound
    game_over_sound.play()
    
    win.fill(BLACK)
    game_over_font = pygame.font.SysFont("consolas", 50)
    game_over_text = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()  # replay the game
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()  # quit the game
                    return

def run():
    global score, rapid_fire_active, shield_active, rapid_fire_timer, shield_timer
    score = 0
    running = True
    enemy_spawn_counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_d] and player_pos[0] < WIDTH - PLAYER_SIZE:
                player_pos[0] += player_speed
            if keys[pygame.K_SPACE]:
                create_bullet()

            # Activate Rapid Fire with 'R'
            if keys[pygame.K_r] and not rapid_fire_active:
                rapid_fire_active = True
                rapid_fire_timer = pygame.time.get_ticks() + 5000  # 5 seconds duration

            # Activate Shield with 'S'
            if keys[pygame.K_s] and not shield_active:
                shield_active = True
                shield_timer = pygame.time.get_ticks() + 5000  # 5 seconds duration

        # Handle Rapid Fire
        if rapid_fire_active:
            if pygame.time.get_ticks() > rapid_fire_timer:
                rapid_fire_active = False
            else:
                if pygame.time.get_ticks() % 100 < 50:  # Fire bullets rapidly
                    create_bullet()

        # Update and draw objects
        draw_objects()
        update_positions()

        # Handle Shield expiration
        if shield_active and pygame.time.get_ticks() > shield_timer:
            shield_active = False

        # Check collision (only if shield is not active)
        if not shield_active and check_collision():
            game_over_screen()
            break

        # Spawn enemies periodically
        enemy_spawn_counter += 1
        if enemy_spawn_counter % 30 == 0:  # adjust this to change the spawn rate
            create_enemy()

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    run()
