import pygame
import networkx as nx
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Graph Visualization")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)

# Create a grid graph
G = nx.grid_2d_graph(8, 5)

# Function to convert graph coordinates to screen coordinates
def graph_to_screen(node):
    x, y = node
    return x * 100 + 50, y * 100 + 50  # Assuming each grid cell is 100x100 pixels

class Player:
    def __init__(self, position):
        self.position = position
        self.health = 100
        self.attack = 5

    def pick_weapon(self, weapon):
        self.attack += weapon.attack_bonus

    def draw(self):
        pygame.draw.circle(screen, BLUE, graph_to_screen(self.position), 10)

class Monster:
    def __init__(self, position):
        self.position = position
        self.health = 25
        self.attack = 2

    def draw(self):
        pygame.draw.circle(screen, RED, graph_to_screen(self.position), 10)

class Weapon:
    def __init__(self, position):
        self.position = position
        self.attack_bonus = 5

    def draw(self):
        pygame.draw.circle(screen, GRAY, graph_to_screen(self.position), 10)

class Treasure:
    def __init__(self, position):
        self.position = position

    def draw(self):
        pygame.draw.circle(screen, GOLD, graph_to_screen(self.position), 10)

class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(position[0], position[1], 200, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class GameInterface:
    def __init__(self):
        self.buttons = [
            Button("Move", (600, 50)),
            Button("Fight", (600, 150)),
            Button("Pick Up", (600, 250)),
            Button("End Turn", (600, 350))
        ]
        self.time = 0

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Time: {self.time}", True, BLACK)
        screen.blit(text_surface, (50, 50))

    def handle_click(self, position):
        for button in self.buttons:
            if button.rect.collidepoint(position):
                print(f"Button {button.text} clicked")

    def increment_time(self):
        self.time += 1

# Create instances of player, monsters, weapons, and treasure
player = Player((0, 0))
monsters = [Monster((1, 1)), Monster((3, 3))]
weapons = [Weapon((2, 2)), Weapon((4, 4))]
treasure = Treasure((7, 4))

# Create game interface
game_interface = GameInterface()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game_interface.handle_click(pygame.mouse.get_pos())

            # Increment time
            game_interface.increment_time()

    # Clear the screen
    screen.fill(WHITE)

    # Draw nodes and edges of the graph
    for node in G.nodes:
        pygame.draw.circle(screen, BLACK, graph_to_screen(node), 5)

    for edge in G.edges:
        pygame.draw.line(screen, BLUE, graph_to_screen(edge[0]), graph_to_screen(edge[1]), 2)

    # Draw entities
    player.draw()
    treasure.draw()
    for monster in monsters:
        monster.draw()
    for weapon in weapons:
        weapon.draw()

    # Draw game interface
    game_interface.draw(screen)

    # Update the display
    pygame.display.flip()
    

# Quit Pygame
pygame.quit()
