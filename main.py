import pygame
import networkx as nx
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo Grafos")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARKRED = (139, 0, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
ORANGE = (255, 153, 51)
GREEN = (0, 255, 0)
DARKGREEN = (1, 50, 32)

# Create a grid graph
G = nx.grid_2d_graph(8, 5)


# Function to convert graph coordinates to screen coordinates
def graph_to_screen(node):
    x, y = node

    return x * 100 + 50, y * 100 + 50  # Assuming each grid cell is 100x100 pixels


def random_path(graph, source, target):
    visited = set()
    stack = [(source, [source])]
    while stack:
        node, path = stack.pop()
        if node == target:
            return path
        if node not in visited:
            visited.add(node)
            neighbors = list(graph.neighbors(node))
            if neighbors:
                random.shuffle(neighbors)  # Randomly shuffle neighbors
                for neighbor in neighbors:
                    stack.append((neighbor, path + [neighbor]))
    return None  # No path exists


class Player:
    def __init__(self, position):
        self.position = position
        self.health = 100
        self.attack_points = 5
        self.treasure = 50
        self.armed = False
        self.weapon = None

    def pick_weapon(self, weapon):
        self.armed = True
        self.attack_points += weapon.attack_bonus
        self.weapon = weapon

    def drop_weapon(self):
        self.attack_points -= self.weapon.attack_bonus
        self.armed = False
        self.weapon = None

    def draw(self):
        pygame.draw.circle(screen, BLUE, graph_to_screen(self.position), 10)

    def attack(self, monster, weapon):
        monster.health -= self.attack_points
        if self.armed:
            weapon.life -= 1
            if weapon.life == 0:
                self.drop_weapon()


class Monster:
    def __init__(self, position):
        self.position = position
        self.health = 25
        self.attack_points = random.randrange(5, 10, 1)

    def draw(self):
        pygame.draw.circle(screen, RED, graph_to_screen(self.position), 10)

    def attack(self, entity):
        # Entity is the player or another monster
        entity.health = entity.health - self.attack_points


class Boss:
    def __init__(self, position):
        self.position = position
        self.health = 25
        self.attack_points = random.randrange(10, 20, 1)
        self.font = pygame.font.Font(None, 24)  # Font for the attack bonus text

    def draw(self):
        pygame.draw.circle(screen, DARKRED, graph_to_screen(self.position), 10)
        attack_bonus_text = self.font.render(str(self.attack_points), True, BLACK)
        text_rect = attack_bonus_text.get_rect(center=graph_to_screen(self.position))
        text_rect.y -= 20  # Place the text above the circle

        # Blit the attack bonus text onto the screen
        screen.blit(attack_bonus_text, text_rect)

    def attack(self, entity):
        # Entity is the player or another monster
        entity.health = entity.health - self.attack_points


class Plant:
    def __init__(self, position):
        self.position = position
        self.cure = random.randrange(5, 20, 5)
        self.font = pygame.font.Font(None, 24)  # Font for the attack bonus text

    def draw(self):
        pygame.draw.circle(screen, DARKGREEN, graph_to_screen(self.position), 10)
        attack_bonus_text = self.font.render(str(self.cure), True, BLACK)
        text_rect = attack_bonus_text.get_rect(center=graph_to_screen(self.position))
        text_rect.y -= 20  # Place the text above the circle

        # Blit the attack bonus text onto the screen
        screen.blit(attack_bonus_text, text_rect)


class Danger:
    def __init__(self, position, damage):
        self.position = position
        self.damage = damage
        self.cure = random.randrange(5, 15, 5)

    def draw(self):
        pygame.draw.circle(screen, ORANGE, graph_to_screen(self.position), 10)


class Weapon:
    def __init__(self, position):
        self.position = position
        self.attack_bonus = 5
        self.life = 3
        self.font = pygame.font.Font(None, 24)  # Font for the attack bonus text

    def draw(self):
        pygame.draw.circle(screen, GRAY, graph_to_screen(self.position), 10)

        # Render the attack bonus text
        attack_bonus_text = self.font.render(str(self.attack_bonus), True, BLACK)
        text_rect = attack_bonus_text.get_rect(center=graph_to_screen(self.position))
        text_rect.y -= 20  # Place the text above the circle

        # Blit the attack bonus text onto the screen
        screen.blit(attack_bonus_text, text_rect)


class Treasure:
    def __init__(self, position):
        self.position = position

    def draw(self):
        pygame.draw.circle(screen, GOLD, graph_to_screen(self.position), 10)


class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(position[0], position[1], 150, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Bar():
    def __init__(self, x, y, attribute, max_attribute, color):
        self.x = x
        self.y = y
        self.attribute = attribute
        self.max_attribute = max_attribute
        self.color = color
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        ratio = self.attribute/self.max_attribute
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 120, 20))
        pygame.draw.rect(screen, self.color, (self.x, self.y, 120 * ratio, 20))

class GameInterface:
    def __init__(self):
        self.buttons = [
            Button("Move", (50, 500)),
            Button("Fight", (200, 500)),
            Button("Pick Up", (350, 500)),
            Button("End Turn", (500, 500))
        ]
        self.time = 0
        self.time_left = 201

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
        health_bar.draw(screen)
        treasure_bar.draw(screen)
        attack_bar.draw(screen)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Tempo: {self.time}", True, BLACK)
        screen.blit(text_surface, (50, 50))
        text_surface2 = font.render(f"Tempo restante: {self.time_left}", True, GRAY)
        screen.blit(text_surface2, (50, 100))

    def handle_click(self, position):
        for button in self.buttons:
            if button.rect.collidepoint(position):
                return button.text
        return None

    def increment_time(self):
        self.time += 1
        self.time_left -= 1


class GameManager:
    def __init__(self, graph, player, monsters, weapons, treasure, path):
        self.graph = graph
        self.player = player
        self.monsters = monsters
        self.weapons = weapons
        self.treasure = treasure
        self.path = path
        self.path_index = 0
        self.is_forward = True

    def handle_player_movement(self):
        if self.path is None:
            return  # No path

        if self.is_forward:
            # Move player forward on the path
            if self.path_index < len(self.path):
                next_position = self.path[self.path_index]
                self.player.position = next_position
                self.path_index += 1
            else:
                # Reached the end of the path, start walking back
                self.is_forward = False
                self.path_index -= 2  # Move back two steps to start walking back
        else:
            # Move player back on the path
            if self.path_index >= 0:
                next_position = self.path[self.path_index]
                self.player.position = next_position
                self.path_index -= 1
            else:
                # Reached the start of the path, start walking forward again
                self.is_forward = True
                self.path_index = 1

    def handle_player_action(self, action):
        # Implement logic for player actions (e.g., picking up a weapon, fighting a monster)
        pass

    def update_game_state(self, clicked_button):
        # Implement game logic for updating the game state (e.g., monster movement, checking for collisions)
        if clicked_button.lower() == "move":
            self.handle_player_movement()

            # Monster movement
            for monster in self.monsters:
                neighbors = list(self.graph.neighbors(monster.position))
                if neighbors:
                    new_position = random.choice(list(neighbors + [monster.position]))
                    monster.position = new_position

# Player's status

# Create instances of player, monsters, weapons, and treasure
player = Player((0, 0))
treasure = Treasure((7, 4))

health_bar = Bar(50, 550, player.health, 100, GREEN)
treasure_bar = Bar(200, 550, player.treasure, 100, GOLD)
attack_bar = Bar(350, 550, player.attack_points, 50, DARKRED)

# TODO: Place monsters, weapons and dangers randomly on the graph,
#  together they should be 20%~30% of the number of edges
m = len(G.edges)

# Calculate the number of entities (monsters, weapons, dangers) based on the percentage range

# Function to generate random entities and objects into the island
num_entities = random.randint(round(m * 0.20), round(m * 0.30))

# monsters = [Monster((1, 1)), Monster((3, 3))]
# weapons = [Weapon((2, 2)), Weapon((4, 4))]
# dangers = [Danger((6, 0), damage=1), Danger((6, 1), damage=1), Danger((6, 2), damage=1)]
# plants = [Plant((1, 4)), Plant((3, 2))]
# boss = Boss((5, 2))

# Entities
monsters = []
weapons = []
dangers = []
plants = []
bosses = []


# Function to check if a position is valid (not on (0, 0) or (7, 4))
def is_valid_position(position):
    return position != (0, 0) and position != (7, 4)


# Function to check if a position is empty (no other entity already placed there)
def is_empty_position(position, all_entities):
    return position not in [entity.position for entity in all_entities]


for i in range(num_entities):
    while True:
        # Generate a random position
        position = (random.randint(0, 7), random.randint(0, 4))

        # Check if the position is valid and empty
        if is_valid_position(position) and is_empty_position(position, monsters + weapons + dangers + plants + bosses):
            # Randomly choose the type of entity to place
            entity_type = random.choice(['monster', 'weapon', 'danger', 'plant', 'boss'])
            if entity_type == 'monster':
                monsters.append(Monster(position))
            elif entity_type == 'weapon':
                weapons.append(Weapon(position))
            elif entity_type == 'danger':
                dangers.append(Danger(position, damage=1))
            elif entity_type == 'plant':
                plants.append(Plant(position))
            elif entity_type == 'boss':
                bosses.append(Boss(position))
            break  # Exit the loop if entity is successfully placed

# Find a path from the initial node to the treasure node
path = random_path(G, player.position, treasure.position)

# Create a reversed path from the treasure node back to the initial node
return_path = path[::-1]

# Create game interface
game_interface = GameInterface()

game_manager = GameManager(G, player, monsters, weapons, treasure, path)

# Mark the edges along the path as green
for i in range(len(path) - 1):
    G[path[i]][path[i + 1]]['color'] = GREEN

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_button = game_interface.handle_click(pygame.mouse.get_pos())
            if clicked_button is not None:
                game_manager.update_game_state(clicked_button)

            # Increment time
            game_interface.increment_time()

    # Clear the screen
    screen.fill(WHITE)

    # Draw nodes and edges of the graph
    for node in G.nodes:
        pygame.draw.circle(screen, BLACK, graph_to_screen(node), 5)

    for edge in G.edges:
        color = G[edge[0]][edge[1]].get('color', BLUE)
        pygame.draw.line(screen, color, graph_to_screen(edge[0]), graph_to_screen(edge[1]), 2)

    # Draw entities
    # boss.draw()
    for monster in monsters:
        if monster.health > 0:
            monster.draw()
    for weapon in weapons:
        weapon.draw()
    for danger in dangers:
        danger.draw()
    for plant in plants:
        plant.draw()
    player.draw()
    treasure.draw()

    # Draw game interface
    game_interface.draw(screen)

    # Update the display
    pygame.display.flip()

    # TODO: Implement game's logic and progression
    # # Combat logic (for demonstration purposes)
    # if "Fight" in [button.text for button in game_interface.buttons]:
    #     player_health = player.health
    #     monster_health = monsters[0].health
    #
    #     # Simulate combat
    #     player_attack = random.randint(1, player.attack_points)
    #     monster_attack = random.randint(1, monsters[0].attack_points)
    #
    #     player_health -= monster_attack
    #     monster_health -= player_attack
    #
    #     print(f"Player health: {player_health}, Monster health: {monster_health}")

# Quit Pygame
pygame.quit()
