import pygame
import random

# setting up some initial parameters
WIDTH, HEIGHT = 600, 600
PLAYER_SIZE = 40
BULLET_SIZE = 10
ENEMY_SIZE = 40

pygame.font.init()
score_font = pygame.font.SysFont("consolas", 20)
score = 0

# color definition
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# initialize pygame
pygame.init()

# setting up display
win = pygame.display.set_mode((WIDTH, HEIGHT))

# setting up clock
clock = pygame.time.Clock()

# player initialization
player_pos = [WIDTH//2, HEIGHT - PLAYER_SIZE - 10]
player_speed = 10

# bullet and enemy initialization
bullets = []
enemies = []

# Create a bullet
def create_bullet():
    bullet_pos = [player_pos[0] + PLAYER_SIZE//2 - BULLET_SIZE//2, player_pos[1]]
    bullets.append(bullet_pos)

# Create an enemy
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_SIZE)
    y = random.randint(-HEIGHT, -ENEMY_SIZE)
    enemies.append([x, y])

# Draw objects on the screen
def draw_objects():
    win.fill((0, 0, 0))
    pygame.draw.rect(win, GREEN, pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))
    
    for bullet in bullets:
        pygame.draw.rect(win, WHITE, pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))
    
    for enemy in enemies:
        pygame.draw.rect(win, RED, pygame.Rect(enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE))
    
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

# Update bullets' and enemies' positions
def update_positions():
    global score

    # Update bullets
    for bullet in bullets[:]:
        bullet[1] -= 10
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies[:]:
        enemy[1] += 5
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

        # Check for collision between bullet and enemy
        for bullet in bullets[:]:
            if enemy[0] < bullet[0] < enemy[0] + ENEMY_SIZE and \
               enemy[1] < bullet[1] < enemy[1] + ENEMY_SIZE:
                bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 2


# Check for collision between player and enemy
def check_collision():
    for enemy in enemies:
        if player_pos[0] < enemy[0] < player_pos[0] + PLAYER_SIZE and \
           player_pos[1] < enemy[1] < player_pos[1] + PLAYER_SIZE:
            return True
    return False

# Game over screen
def game_over_screen():
    global score
    win.fill((0, 0, 0))
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
    global score
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
        
        draw_objects()
        update_positions()
        
        if check_collision():
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
