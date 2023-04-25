import pygame
import random
import math

pygame.init()

# Set up the Pygame window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hans Bowling")

# Set up the game variables
ball_pos = [400, 580]
ball_vel = [0, 0]
ball_speed = 10
stickman_pos = [random.randint(50, 750), 20]
wind_strength = random.randint(1, 50)
wind_strength = (wind_strength/2)
wind_direction = 1 if random.randint(0, 1) == 0 else -1
score = 0

# Load the images
ball_img = pygame.image.load("ball.png")
ball_img = pygame.transform.scale(ball_img, (30, 50))
stickman_img = pygame.image.load("stickman.png")
stickman_img = pygame.transform.scale(stickman_img, (80, 120))

# Set the initial position of the ball
ball_pos = [screen.get_width() // 2, screen.get_height() - 50]
aim_angle = 90

# Set up the font for displaying the wind strength and score
font = pygame.font.Font(None, 36)

# Set up the clock to control the game's frame rate
clock = pygame.time.Clock()

# Define a function to calculate the distance between two points
def distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Define a function to calculate the angle between two points
def angle(p, q):
    return math.atan2(q[1] - p[1], q[0] - p[0])

# Define a function to calculate the wind effect on the ball
def apply_wind():
    global ball_vel, wind_strength, wind_direction
    wind_force = wind_strength / 10.0 * wind_direction
    ball_vel[0] += wind_force

# Define the main game loop
running = True
draw_line = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_line = False
                # Shoot the ball
                aim_direction = math.radians(aim_angle)
                ball_vel[0] = ball_speed * math.cos(aim_direction)
                ball_vel[1] = -ball_speed * math.sin(aim_direction)
                # Apply the wind effect on the ball
                apply_wind()
                # Update wind strength and direction randomly
                wind_strength = random.randint(1, 50)
                wind_strength = (wind_strength/2)
                wind_direction = 1 if random.randint(0, 1) == 0 else -1
            elif event.key == pygame.K_LEFT:
                ball_pos[0] -= 10
            elif event.key == pygame.K_RIGHT:
                ball_pos[0] += 10
            elif event.key == pygame.K_UP:
                aim_angle += 5
            elif event.key == pygame.K_DOWN:
                aim_angle -= 5

    # Update the ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check if the ball is above the stickman
    if ball_pos[1] < stickman_pos[1]:
        # Restart the game with 0 points
        ball_pos = [screen.get_width() // 2, screen.get_height() - 50]
        ball_vel = [0, 0]
        score = 0
        draw_line = True
    else:
        # Check for collisions with the stickman
        if distance(ball_pos, stickman_pos) < 80:
            score += 10
            stickman_pos = [random.randint(50, 750), 20]
            ball_pos = [screen.get_width() // 2, screen.get_height() - 50]
            ball_vel = [0, 0]
            draw_line = True

    # Draw the game objects
    screen.fill((255, 255, 255))
    screen.blit(ball_img, ball_pos)
    screen.blit(stickman_img, stickman_pos)
    wind_text = font.render(f"Wind: {wind_strength} ({'Right' if wind_direction == 1 else 'Left'})", True, (0, 0, 0))
    screen.blit(wind_text, (10, 10))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (700, 10))

    # Calculate the direction of the ball based on the angle
    aim_direction = math.radians(aim_angle)

    # Draw a line to indicate the direction of the ball
    dx = ball_speed * math.cos(aim_direction)
    dy = -ball_speed * math.sin(aim_direction)

    if draw_line:
        line_end_pos = [ball_pos[0] + dx * 10 + 15, ball_pos[1] + dy * 10 + 15]
        pygame.draw.line(screen, (0, 0, 255), (ball_pos[0]+15, ball_pos[1]+25), line_end_pos, 2)

    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()