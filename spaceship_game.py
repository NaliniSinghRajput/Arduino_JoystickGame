import pygame
import serial
import time
import random
import math

# ==================================================
# Arduino Serial Setup
# ==================================================
PORT = "COM3"      # Change this if your Arduino is on another COM port
BAUD = 9600

arduino = serial.Serial(PORT, BAUD, timeout=0.01)
time.sleep(2)

# ==================================================
# Pygame Setup
# ==================================================
pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arduino Joystick Spaceship Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ==================================================
# Colors
# ==================================================
BLACK = (5, 5, 20)
WHITE = (255, 255, 255)
BLUE = (60, 180, 255)
RED = (255, 70, 70)
YELLOW = (255, 220, 80)
GREEN = (80, 255, 120)
GRAY = (120, 120, 120)

# ==================================================
# Joystick Settings
# ==================================================
CENTER_X = 512
CENTER_Y = 512
DEADZONE = 80

x_value = CENTER_X
y_value = CENTER_Y
button = 0

# ==================================================
# Player Settings
# ==================================================
player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 8
player_size = 35

lives = 3
score = 0

# ==================================================
# Bullet Settings
# ==================================================
bullets = []
bullet_speed = 10
last_shot_time = 0
shot_delay = 250  # milliseconds

# ==================================================
# Enemy Settings
# ==================================================
enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = 700  # milliseconds

# ==================================================
# Star Background
# ==================================================
stars = []

for _ in range(80):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])


def read_joystick():
    """
    Reads joystick data from Arduino.
    Expected Arduino format:
    x,y,button
    Example:
    512,498,0
    """
    global x_value, y_value, button

    try:
        line = arduino.readline().decode(errors="ignore").strip()

        if line:
            parts = line.split(",")

            if len(parts) == 3:
                x_value = int(parts[0])
                y_value = int(parts[1])
                button = int(parts[2])

    except:
        pass


def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
        star[1] += star[2]

        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
            star[2] = random.randint(1, 3)


def draw_player(x, y):
    """
    Draws a simple spaceship using polygons.
    """
    ship_points = [
        (x, y - player_size),
        (x - player_size, y + player_size),
        (x, y + player_size // 2),
        (x + player_size, y + player_size)
    ]

    pygame.draw.polygon(screen, BLUE, ship_points)
    pygame.draw.polygon(screen, WHITE, ship_points, 2)

    # engine flame
    flame_points = [
        (x - 10, y + player_size),
        (x + 10, y + player_size),
        (x, y + player_size + 25)
    ]

    pygame.draw.polygon(screen, YELLOW, flame_points)


def move_player():
    global player_x, player_y

    dx = x_value - CENTER_X
    dy = y_value - CENTER_Y

    if abs(dx) < DEADZONE:
        dx = 0

    if abs(dy) < DEADZONE:
        dy = 0

    move_x = int((dx / 512) * player_speed)
    move_y = int((dy / 512) * player_speed)

    player_x += move_x
    player_y += move_y

    # Keep player inside screen
    player_x = max(player_size, min(WIDTH - player_size, player_x))
    player_y = max(player_size, min(HEIGHT - player_size - 20, player_y))


def shoot_bullet():
    global last_shot_time

    current_time = pygame.time.get_ticks()

    if button == 1 and current_time - last_shot_time > shot_delay:
        bullets.append([player_x, player_y - player_size])
        last_shot_time = current_time


def update_bullets():
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed

        if bullet[1] < 0:
            bullets.remove(bullet)


def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, (bullet[0] - 4, bullet[1], 8, 20))


def spawn_enemy():
    global enemy_spawn_timer

    current_time = pygame.time.get_ticks()

    if current_time - enemy_spawn_timer > enemy_spawn_delay:
        enemy_x = random.randint(40, WIDTH - 40)
        enemy_y = -40

        # Smaller enemy balls
        enemy_radius = random.randint(10, 18)

        enemy_speed = random.randint(3, 6)

        enemies.append([enemy_x, enemy_y, enemy_radius, enemy_speed])
        enemy_spawn_timer = current_time


def update_enemies():
    global lives

    for enemy in enemies[:]:
        enemy[1] += enemy[3]

        if enemy[1] > HEIGHT + enemy[2]:
            enemies.remove(enemy)
            lives -= 1


def draw_enemies():
    for enemy in enemies:
        x, y, radius, speed = enemy

        pygame.draw.circle(screen, RED, (x, y), radius)
        pygame.draw.circle(screen, WHITE, (x, y), radius, 2)

        # small asteroid details
        pygame.draw.circle(screen, GRAY, (x - 8, y - 5), 5)
        pygame.draw.circle(screen, GRAY, (x + 10, y + 8), 4)


def check_collisions():
    global score, lives

    # Bullet-enemy collision
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            enemy_x, enemy_y, enemy_radius, enemy_speed = enemy

            distance = math.sqrt((bullet[0] - enemy_x) ** 2 + (bullet[1] - enemy_y) ** 2)

            if distance < enemy_radius:
                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy in enemies:
                    enemies.remove(enemy)

                score += 10
                break

    # Player-enemy collision
    for enemy in enemies[:]:
        enemy_x, enemy_y, enemy_radius, enemy_speed = enemy

        distance = math.sqrt((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2)

        if distance < player_size + enemy_radius:
            enemies.remove(enemy)
            lives -= 1


def draw_score_lives():
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)

    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (20, 55))


def game_over_screen():
    screen.fill(BLACK)

    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    exit_text = font.render("Close the window to exit", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 170, HEIGHT // 2 - 80))
    screen.blit(score_text, (WIDTH // 2 - 90, HEIGHT // 2))
    screen.blit(exit_text, (WIDTH // 2 - 140, HEIGHT // 2 + 50))

    pygame.display.update()


# ==================================================
# Main Game Loop
# ==================================================
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if lives > 0:
        read_joystick()
        move_player()
        shoot_bullet()

        spawn_enemy()
        update_bullets()
        update_enemies()
        check_collisions()

        screen.fill(BLACK)

        draw_stars()
        draw_player(player_x, player_y)
        draw_bullets()
        draw_enemies()
        draw_score_lives()

        pygame.display.update()

    else:
        game_over_screen()

pygame.quit()
arduino.close()