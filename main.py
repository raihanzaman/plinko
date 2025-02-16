import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1200, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE1 = (16, 23, 38)
BLUE2 = (71, 85, 105)
GREEN1 = (33, 197, 0)
GREEN2 = (73, 222, 128)
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
GAP = 400
GRAVITY = 1

slot_texts = []
dev_panel = False
now = 0
MONEY = 100
BET = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko Game")

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
    for col in range(row + 1):
        x = WIDTH // 2 + (col - row / 2) * PEG_SPACING + SIDE
        y = (row * PEG_SPACING + PEG_SPACING // 2) - 60
        pegs.append((x, y))

balls = []
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLUE1)

    gap_rect = pygame.Rect(0, 0, GAP, HEIGHT)
    pygame.draw.rect(screen, (51, 65, 84), gap_rect)

    font = pygame.font.SysFont('helvetica', 18, bold=True)
    font1 = pygame.font.SysFont('impact', 54, bold=False, italic=True)

    drop_button = pygame.Rect(45, 600, 300, 50)
    bet_increase = pygame.Rect(45, 450, 300, 50)
    bet_decrease = pygame.Rect(45, 390, 300, 50)
    mouse_pos = pygame.mouse.get_pos()

    drop_button_color = GREEN2 if drop_button.collidepoint(mouse_pos) else GREEN1
    bet_increase_color = GREEN2 if bet_increase.collidepoint(mouse_pos) else GREEN1
    bet_decrease_color = GREEN2 if bet_decrease.collidepoint(mouse_pos) else GREEN1

    pygame.draw.rect(screen, drop_button_color, drop_button, border_radius=10)
    text = font.render("Drop Ball", True, BLACK)
    screen.blit(text, (drop_button.x + (drop_button.width - text.get_width()) // 2, drop_button.y + (drop_button.height - text.get_height()) // 2))

    pygame.draw.rect(screen, bet_increase_color, bet_increase, border_radius=10)
    text = font.render("INCREASE BET BY $1", True, BLACK)
    screen.blit(text, (bet_increase.x + (bet_increase.width - text.get_width()) // 2, bet_increase.y + (bet_increase.height - text.get_height()) // 2))

    pygame.draw.rect(screen, bet_decrease_color, bet_decrease, border_radius=10)
    text = font.render("DECREASE BET BY $1", True, BLACK)
    screen.blit(text, (bet_decrease.x + (bet_decrease.width - text.get_width()) // 2, bet_decrease.y + (bet_decrease.height - text.get_height()) // 2))

    bet_amount = pygame.Rect(45, 330, 300, 50)
    pygame.draw.rect(screen, BLUE1, bet_amount, border_radius=10)
    pygame.draw.rect(screen, BLUE2, bet_amount, width=2, border_radius=10)
    text = font.render(f"BET AMOUNT: ${BET}", True, WHITE)
    screen.blit(text, (bet_amount.x + (bet_amount.width - text.get_width()) // 2, bet_amount.y + (bet_amount.height - text.get_height()) // 2))
    money_amount = pygame.Rect(45, 100, 300, 100)
    pygame.draw.rect(screen, BLUE1, money_amount, border_radius=10)
    pygame.draw.rect(screen, BLUE2, money_amount, width=2, border_radius=10)
    text = font1.render(f"${MONEY:.2f}", True, WHITE)
    screen.blit(text, (money_amount.x + (money_amount.width - text.get_width()) // 2, money_amount.y + (money_amount.height - text.get_height()) // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if drop_button.collidepoint(event.pos) & (MONEY // 1 >= BET - 0.01):
                balls.append(Ball(WIDTH // 2 + SIDE + 5, HEIGHT // 50 + 10))
                MONEY -= BET
            elif bet_increase.collidepoint(event.pos) and MONEY // 1 > BET:
                BET += 1
            elif bet_decrease.collidepoint(event.pos) and BET > 1:
                BET -= 1
    
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
        slot_rect = pygame.Rect(SIDE + GAP - 120 + i * PEG_SPACING, HEIGHT - 50, SLOT_WIDTH, 35)
        display_rect = slot_rect
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
        pygame.draw.rect(screen, slot_color, display_rect, border_radius=10)
        font2 = pygame.font.SysFont(None, 20)
        text = font2.render(f"{values[i]}x", True, BLACK)
        screen.blit(text, (SIDE + GAP - 120 + i * PEG_SPACING + SLOT_WIDTH // 2 - text.get_width() // 2, HEIGHT - 40))

        for ball in balls:
            if slot_rect.collidepoint(ball.x, ball.y):
                slot_number = i + 1
                slot_texts.append(f"Slot: {slot_number}")
                balls.remove(ball)
                MONEY += BET * values[i]
                impact_color = (255, 255, 0)
                pygame.draw.rect(screen, impact_color, display_rect, border_radius=10)

        y_offset = 150
        recent_texts = slot_texts[-5:][::-1] 
        font2 = pygame.font.SysFont(None, 28)
        for text in recent_texts:
            slot_number = int(text.split(": ")[1])
            value = values[slot_number - 1]
            slot_color = color_map.get(value, WHITE)
            rendered_text = font2.render(f"{value}x", True, BLACK)
            text_rect = pygame.Rect(WIDTH - 100, y_offset, 50, 50)
            pygame.draw.rect(screen, slot_color, text_rect)
            screen.blit(rendered_text, (text_rect.x + (text_rect.width - rendered_text.get_width()) // 2, text_rect.y + (text_rect.height - rendered_text.get_height()) // 2))
            y_offset += 50

        slot_counts = [0] * NUM_SLOTS
        for text in slot_texts:
            slot_number = int(text.split(": ")[1])
            slot_counts[slot_number - 1] += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_g]:
            cooldown = 200
            if dev_panel  == False and now + cooldown < pygame.time.get_ticks():
                dev_panel = True
                now = pygame.time.get_ticks()
            elif dev_panel == True and now + cooldown < pygame.time.get_ticks():
                dev_panel = False
                cooldown = 0
                now = pygame.time.get_ticks()

        if dev_panel:

            dev = pygame.font.SysFont(None, 20)

            max_count = max(slot_counts) if max(slot_counts) > 0 else 1
            graph_height = 50
            graph_width = 100
            graph_x = WIDTH - 200
            graph_y = 20

            for i, count in enumerate(slot_counts):
                bar_height = int((count / max_count) * graph_height)
                bar_rect = pygame.Rect(graph_x + i * 10, graph_y + graph_height - bar_height, 10, bar_height)
                pygame.draw.rect(screen, GREEN1, bar_rect)

            x_label = dev.render("Slots", True, WHITE)
            y_label = dev.render("Hits", True, WHITE)
            screen.blit(x_label, (graph_x + graph_width // 2 - x_label.get_width() // 2, graph_y + graph_height + 10))
            screen.blit(y_label, (graph_x - 40, graph_y + graph_height // 2 - y_label.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)