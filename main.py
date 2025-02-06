import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Peg and ball properties
PEG_RADIUS = 5
BALL_RADIUS = 8

# Plinko board dimensions
ROWS = 14
COLS = ROWS - 1
PEG_SPACING = 40

# Bottom slots
NUM_SLOTS = ROWS + 1
SLOT_WIDTH = (WIDTH - 200) // NUM_SLOTS
slot_texts = []

# Gravity
GRAVITY = 1

# Money
MONEY = 100

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = 0

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

# Generate pegs in a triangle shape, excluding the top peg
pegs = []
for row in range(2, ROWS):  # Start from row 2 to exclude the top peg
    for col in range(row+1):
        x = WIDTH // 2 + (col - row / 2) * PEG_SPACING
        y = (row * PEG_SPACING + PEG_SPACING // 2 )
        pegs.append((x, y))

# Balls list
balls = []

# Game loop
clock = pygame.time.Clock()
running = True

# Define the drop button
drop_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 50, 100, 50)

while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the button is clicked
            if drop_button.collidepoint(event.pos):
                # Add a new ball at the center
                balls.append(Ball(WIDTH // 2, HEIGHT // 50 + 50))
    
    # Draw the drop button
    pygame.draw.rect(screen, BLACK, drop_button)
    font = pygame.font.SysFont(None, 36)
    text = font.render("Drop", True, WHITE)
    screen.blit(text, (drop_button.x + (drop_button.width - text.get_width()) // 2, drop_button.y + (drop_button.height - text.get_height()) // 2))

    # Update and draw balls
    for ball in balls:
        ball.update()

        # Collision with pegs
        for peg in pegs:
            dx = peg[0] - ball.x
            dy = peg[1] - ball.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < PEG_RADIUS + BALL_RADIUS:
                angle = math.atan2(dy, dx)
                ball.vx = 0.5 * (ball.vx - 2 * math.cos(angle))
                ball.vy = -0.8 * abs(ball.vy - 2 * math.sin(angle))

        # Draw the ball
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), BALL_RADIUS)

    # Draw pegs
    for peg in pegs:
        pygame.draw.circle(screen, BLUE, peg, PEG_RADIUS)

    # Draw bottom slots and check for ball collisions
    for i in range(NUM_SLOTS):
        slot_rect = pygame.Rect(100 + i * SLOT_WIDTH, HEIGHT - 40, SLOT_WIDTH, 30)
        pygame.draw.rect(screen, BLACK, slot_rect, 2)
        
        # Number the slots and display values
        values = [10, 2, 1.5, 1.25, 1, 0.5, 0.2, 0.2, 0.2, 0.5, 1, 1.25, 1.5, 2, 10]
        font = pygame.font.SysFont(None, 20)
        text = font.render(f"{values[i]}x", True, BLACK)
        screen.blit(text, (100 + i * SLOT_WIDTH + SLOT_WIDTH // 2 - text.get_width() // 2, HEIGHT - 30))
        
        # Check for ball collision with slots
        for ball in balls:
            if slot_rect.collidepoint(ball.x, ball.y):
                slot_number = i + 1
                print(f"Ball hit slot number: {slot_number}")
                # Display the slot number on the screen
                slot_texts.append(f"Slot: {slot_number}")
                balls.remove(ball)  # Remove the ball if it falls into the slot    
    
        # Display the 10 most recent slot numbers on the screen
        y_offset = 10
        recent_texts = slot_texts[-10:][::-1]  # Get the 10 most recent drops and reverse the order
        for text in recent_texts:
            slot_number = int(text.split(": ")[1])
            value = values[slot_number - 1]
            rendered_text = font.render(f"{value}x", True, BLACK)
            screen.blit(rendered_text, (10, y_offset))
            y_offset += 20

        # Calculate the total money won
        total_money = MONEY - len(slot_texts)
        for text in slot_texts:
            slot_number = int(text.split(": ")[1])
            value = values[slot_number - 1]
            total_money += value

        # Display the total money on the screen
        money_text = font.render(f"Money: ${total_money:.2f}", True, BLACK)
        screen.blit(money_text, (10, HEIGHT - 60))
        
        # Graph of slots hit
        slot_counts = [0] * NUM_SLOTS
        for text in slot_texts:
            slot_number = int(text.split(": ")[1])
            slot_counts[slot_number - 1] += 1

        # Graph of slots hit in the top right corner
        max_count = max(slot_counts) if max(slot_counts) > 0 else 1
        graph_height = 50
        graph_width = 50
        graph_x = 600
        graph_y = 20

        # Draw the bars
        for i, count in enumerate(slot_counts):
            bar_height = int((count / max_count) * graph_height)
            bar_rect = pygame.Rect(graph_x + i * 10, graph_y + graph_height - bar_height, 10, bar_height)
            pygame.draw.rect(screen, BLUE, bar_rect)

        # Draw the x-axis and y-axis labels
        font = pygame.font.SysFont(None, 24)
        x_label = font.render("Slots", True, BLACK)
        y_label = font.render("Hits", True, BLACK)
        screen.blit(x_label, (graph_x + graph_width // 2 - x_label.get_width() // 2, graph_y + graph_height + 10))
        screen.blit(y_label, (graph_x - 40, graph_y + graph_height // 2 - y_label.get_height() // 2))

    # Define the quit button
    quit_button = pygame.Rect(WIDTH - 150, HEIGHT // 3 - 80, 100, 50)

    # Draw the quit button
    pygame.draw.rect(screen, BLACK, quit_button)
    text = font.render("Quit", True, WHITE)
    screen.blit(text, (quit_button.x + (quit_button.width - text.get_width()) // 2, quit_button.y + (quit_button.height - text.get_height()) // 2))

    # Check if the quit button is clicked
    if event.type == pygame.MOUSEBUTTONDOWN:
        if quit_button.collidepoint(event.pos):
            running = False

    # Update display
    pygame.display.flip()
    clock.tick(60)