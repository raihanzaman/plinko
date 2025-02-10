import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

BLUE1 = (16, 23, 38)
GREEN1 = (33, 197, 93)
COLOR1 = (255, 0, 63)
COLOR2 = (255, 47, 47)
COLOR3 = (255, 96, 31)
COLOR4 = (255, 120, 25)
COLOR5 = (255, 168, 9)
COLOR6 = (254, 192, 0)

PEG_RADIUS = 5
BALL_RADIUS = 8

ROWS = 14
COLS = ROWS - 1
PEG_SPACING = 50

SIDE = 200
NUM_SLOTS = ROWS - 1
SLOT_WIDTH = PEG_SPACING - 15
GAP = (WIDTH - NUM_SLOTS * SLOT_WIDTH) // 2
slot_texts = []
toggle_graph = False

GRAVITY = 1
now = 0
MONEY = 10000
BET = 10

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

pegs = []
for row in range(2, ROWS): 
    for col in range(row+1):
        x = WIDTH // 2 + (col - row / 2) * PEG_SPACING + SIDE
        y = (row * PEG_SPACING + PEG_SPACING // 2) - 60
        pegs.append((x, y))

balls = []

clock = pygame.time.Clock()
running = True

drop_button = pygame.Rect(100, HEIGHT - 100, 300, 50)
bet_increase = pygame.Rect(100, 200, 300, 50)

while running:
    screen.fill(BLUE1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if drop_button.collidepoint(event.pos) & (MONEY >= 5):
                balls.append(Ball(WIDTH // 2 + SIDE + 5, HEIGHT // 50 + 10))
                MONEY -= BET
            elif bet_increase.collidepoint(event.pos):
                BET += 2


    pygame.draw.rect(screen, GREEN1, drop_button, border_radius=10)
    font = pygame.font.SysFont('helvetica', 18, bold=True)
    text = font.render("Drop Ball", True, BLACK)
    screen.blit(text, (drop_button.x + (drop_button.width - text.get_width()) // 2, drop_button.y + (drop_button.height - text.get_height()) // 2))

    pygame.draw.rect(screen, GREEN1, bet_increase, border_radius=10)
    font = pygame.font.SysFont('helvetica', 18, bold=True)
    text = font.render("INCREASE BET BY 2", True, BLACK)
    screen.blit(text, (bet_increase.x + (bet_increase.width - text.get_width()) // 2, bet_increase.y + (bet_increase.height - text.get_height()) // 2))

    for ball in balls:
        ball.update()
        for peg in pegs:
            dx = peg[0] - ball.x
            dy = peg[1] - ball.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < PEG_RADIUS + BALL_RADIUS:
                angle = math.atan2(dy, dx)
                ball.vx = 0.5 * (ball.vx - 2 * math.cos(angle))
                ball.vy = -0.8 * abs(ball.vy - 2 * math.sin(angle))
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), BALL_RADIUS)

    for peg in pegs:
        pygame.draw.circle(screen, WHITE, peg, PEG_RADIUS)

    for i in range(NUM_SLOTS):
        slot_rect = pygame.Rect(SIDE + GAP - 90 + i * PEG_SPACING, HEIGHT - 50, SLOT_WIDTH, 35)
        values = [35, 9, 4, 2, 0.5, 0.2, 0.2, 0.2, 0.5, 2, 4, 9, 35]
        color_map = {
            35: COLOR1,
            9: COLOR2,
            4: COLOR3,
            2: COLOR4,
            0.5: COLOR5,
            0.2: COLOR6
        }
        slot_color = color_map.get(values[i], WHITE)
        pygame.draw.rect(screen, slot_color, slot_rect, border_radius=10)
        font = pygame.font.SysFont(None, 20)
        text = font.render(f"{values[i]}x", True, BLACK)
        screen.blit(text, (SIDE + GAP - 90 + i * PEG_SPACING + SLOT_WIDTH // 2 - text.get_width() // 2, HEIGHT - 40))

        for ball in balls:
            if slot_rect.collidepoint(ball.x, ball.y):
                slot_number = i + 1
                slot_texts.append(f"Slot: {slot_number}")
                balls.remove(ball)
                MONEY += 5 * values[i]

        y_offset = 10
        recent_texts = slot_texts[-10:][::-1] 
        for text in recent_texts:
            slot_number = int(text.split(": ")[1])
            value = values[slot_number - 1]
            rendered_text = font.render(f"{value}x", True, WHITE)
            screen.blit(rendered_text, (10, y_offset))
            y_offset += 20

        font = pygame.font.SysFont('helvetica', 18, bold=True)
        money_text = font.render(f"Money: ${MONEY:.2f}", True, WHITE)
        screen.blit(money_text, (20, 30))

        slot_counts = [0] * NUM_SLOTS
        for text in slot_texts:
            slot_number = int(text.split(": ")[1])
            slot_counts[slot_number - 1] += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_g]:
            cooldown = 200
            if toggle_graph  == False and now + cooldown < pygame.time.get_ticks():
                toggle_graph = True
                now = pygame.time.get_ticks()
            elif toggle_graph == True and now + cooldown < pygame.time.get_ticks():
                toggle_graph = False
                cooldown = 0
                now = pygame.time.get_ticks()

        if toggle_graph:
            max_count = max(slot_counts) if max(slot_counts) > 0 else 1
            graph_height = 50
            graph_width = 50
            graph_x = WIDTH - 200
            graph_y = 20

            for i, count in enumerate(slot_counts):
                bar_height = int((count / max_count) * graph_height)
                bar_rect = pygame.Rect(graph_x + i * 10, graph_y + graph_height - bar_height, 10, bar_height)
                pygame.draw.rect(screen, GREEN, bar_rect)

            x_label = font.render("Slots", True, WHITE)
            y_label = font.render("Hits", True, WHITE)
            screen.blit(x_label, (graph_x + graph_width // 2 - x_label.get_width() // 2, graph_y + graph_height + 10))
            screen.blit(y_label, (graph_x - 40, graph_y + graph_height // 2 - y_label.get_height() // 2))

    quit_button = pygame.Rect(WIDTH - 150, HEIGHT // 3 - 80, 100, 50)

    pygame.draw.rect(screen, WHITE, quit_button)
    text = font.render("Quit", True, BLACK)
    screen.blit(text, (quit_button.x + (quit_button.width - text.get_width()) // 2, quit_button.y + (quit_button.height - text.get_height()) // 2))

    if event.type == pygame.MOUSEBUTTONDOWN:
        if quit_button.collidepoint(event.pos):
            running = False

    tick_text = font.render(f"Tick: {pygame.time.get_ticks()}, Now: {now}", True, WHITE)
    screen.blit(tick_text, (WIDTH - 150, HEIGHT - 60))

    pygame.display.flip()
    clock.tick(60)