import pygame
import networkx as nx
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo Grafos")

font = pygame.font.Font('assets/VT323-Regular.ttf', 32)
character = pygame.image.load('assets/personagem.png')

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
m = len(G.edges)

background = pygame.image.load("assets/old_map.png")


def background_map(image):
    size = pygame.transform.scale(background, (800, 450))
    screen.blit(size, (0, 0))


# Function to convert graph coordinates to screen coordinates
def graph_to_screen(node):
    x, y = node

    return x * 81 + 115, y * 57.5 + 110  #

def draw_menu_interface():
    def character_place():
        size = pygame.transform.scale(character, (90, 110))
        screen.blit(size, (20, 470))

    def bg0_place(w, h, x, y):
        background = pygame.image.load('assets/backgrounds/menu_background.jpg')
        size = pygame.transform.scale(background, (w, h))
        screen.blit(size, (x, y))
    def bg1_place():
        character_background = pygame.image.load('assets/backgrounds/character_background.png')
        size = pygame.transform.scale(character_background, (90, 110))
        screen.blit(size, (20, 470))
        
    def bg2_place():
        object_background = pygame.image.load('assets/backgrounds/character_background.png')
        size2 = pygame.transform.scale(object_background, (110, 70))
        screen.blit(size2, (670, 470))

    # menu
    pygame.draw.rect(screen, (240, 223, 153), (0, 450, 800, 150))
    bg0_place(800, 150, 0, 450)
    # character
    pygame.draw.rect(screen, (109, 54, 22), (20, 470, 90, 110))
    bg1_place()
    character_place()
    pygame.draw.rect(screen, (109, 54, 22), (20, 470, 90, 110), 3)
    # object
    pygame.draw.rect(screen, (0, 0, 0), (670, 470, 110, 70))
    bg2_place()
    pygame.draw.rect(screen, (0, 0, 0), (670, 550, 110, 30))
    pygame.draw.rect(screen, (109, 54, 22), (670, 470, 110, 70), 3)
    # dialog
    pygame.draw.rect(screen, (0, 0, 0), (260, 510, 380, 30))
    # time window
    pygame.draw.rect(screen, (109, 54, 22), ( 630, 20, 150, 40))

object_rect = pygame.draw.rect(screen, (0, 0, 0), (670, 550, 110, 30))
def draw_monster(hp, ap):
    object = pygame.image.load('assets/monsters/monstro.png')
    size = pygame.transform.scale(object, (110, 70))
    message = str(hp) + "h/" + str(ap) + "a"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=object_rect.center)
    screen.blit(size, (670, 470))
    screen.blit(text, text_rect)

def draw_plant(hp):
    object = pygame.image.load('assets/objects/planta.png')
    size = pygame.transform.scale(object, (110, 70))
    message = "+" + str(hp) + "hp"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center = object_rect.center)
    screen.blit(size, (670, 470))
    screen.blit(text, text_rect)

def draw_treasure():
    object = pygame.image.load('assets/objects/tesouro.png')
    size = pygame.transform.scale(object, (110, 70))
    screen.blit(size, (670, 470))

def draw_weapon(bonus):
    object = pygame.image.load('assets/objects/arma.png')
    size = pygame.transform.scale(object, (110, 70))
    message = "+" + str(bonus) + "ap"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center = object_rect.center)
    screen.blit(size, (670, 470))
    screen.blit(text, text_rect)

def draw_danger(hp):
    object = pygame.image.load('assets/objects/perigo.png')
    size = pygame.transform.scale(object, (110, 70))
    message = "-" + str(hp) + "hp"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center = object_rect.center)
    screen.blit(size, (670, 470))
    screen.blit(text, text_rect)

def draw_boss(hp, ap):
    object = pygame.image.load('assets/monsters/jacare.png')
    size = pygame.transform.scale(object, (110, 70))
    message = str(hp) + "h/" + str(ap) + "a"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=object_rect.center)
    screen.blit(size, (670, 470))
    screen.blit(text, text_rect)


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
        self.max_health = 100
        self.attack_points = 5
        self.max_attack_points = 20
        self.treasure = 0
        self.max_treasure = 100
        self.with_treasure = False
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
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (106, 55, 113), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/jogador.png')
        img = pygame.transform.scale(load_img, (25, 25))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)
    def attack(self, monster, weapon):
        monster.health -= self.attack_points
        if self.armed:
            weapon.life -= 1
            if weapon.life == 0:
                self.drop_weapon()

    def recalculate_max_treasure(self):
        last_limit = self.health
        if self.armed == True:
            self.max_treasure -= self.weapon.attack_bonus

class Monster:
    def __init__(self, position):
        self.position = position
        self.health = 25
        self.attack_points = random.randrange(5, 10, 1)

    def draw(self):
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (58, 30, 13), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/monstro.png')
        img = pygame.transform.scale(load_img, (25, 25))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)

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
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (109, 54, 22), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/chefao.png')
        img = pygame.transform.scale(load_img, (25, 25))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)

    def attack(self, entity):
        # Entity is the player or another monster
        entity.health = entity.health - self.attack_points


class Plant:
    def __init__(self, position):
        self.position = position
        self.cure = random.randrange(5, 20, 5)
        self.font = pygame.font.Font(None, 24)  # Font for the attack bonus text

    def draw(self):
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (109, 54, 22), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/planta.png')
        img = pygame.transform.scale(load_img, (20, 20))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)


class Danger:
    def __init__(self, position):
        self.position = position
        self.damage = random.randrange(5, 20, 5)

    def draw(self):
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (109, 54, 22), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/perigo.png')
        img = pygame.transform.scale(load_img, (20, 20))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)


class Weapon:
    def __init__(self, position):
        self.position = position
        self.attack_bonus = 5
        self.life = 3
        self.font = pygame.font.Font(None, 24)  # Font for the attack bonus text

    def draw(self):
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (109, 54, 22), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/arma.png')
        img = pygame.transform.scale(load_img, (20, 20))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)


class Treasure:
    def __init__(self, position):
        self.position = position

    def draw(self):
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (109, 54, 22), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/tesouro.png')
        img = pygame.transform.scale(load_img, (20, 20))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)


class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = pygame.font.Font('assets/VT323-Regular.ttf', 24)
        self.rect = pygame.Rect(position[0], position[1], 85, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, (109, 54, 22), self.rect)
        pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 3, 30))
        pygame.draw.rect(screen, (58, 30, 13), (self.position[0]+82, self.position[1], 3, 30))
        pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 85, 3))
        pygame.draw.rect(screen, (58, 30, 13), (self.position[0], self.position[1]+27, 85, 3))

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class Bar:
    def __init__(self, x, y, attribute, max_attribute, color, icon):
        self.x = x
        self.y = y
        self.attribute = attribute
        self.max_attribute = max_attribute
        self.color = color
        self.icon = icon
        self.font = pygame.font.Font('assets/VT323-Regular.ttf', 10)

    def draw(self, screen):
        ratio = self.attribute / self.max_attribute
        pygame.draw.rect(screen, (58, 30, 13), (self.x, self.y, 110, 30))
        pygame.draw.rect(screen, self.color, (self.x, self.y, 110 * ratio, 30))
        rect = pygame.draw.rect(screen, (109, 54, 22), (self.x, self.y, 110, 30), 2)
        size = pygame.transform.scale(self.icon, (30, 30))
        number = font.render(str(self.attribute), True, WHITE)
        screen.blit(size, (self.x + 80, self.y))
        screen.blit(number, (self.x + 5, self.y-2))




class DialogBox:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def draw(self):
        text = font.render(self.title, True, BLACK)
        screen.blit(text, (200, 200))

class GameManager:
    def __init__(self,
                 graph,
                 path,
                 player: Player,
                 treasure: Treasure,
                 monsters: [Monster],
                 weapons: [Weapon],
                 plants: [Plant],
                 bosses: [Boss],
                 dangers: [Danger]):

        self.graph = graph
        self.time = 0
        self.time_left = 3 * len(graph.edges)

        # Entities
        self.player = player
        self.monsters = monsters
        self.weapons = weapons
        self.treasure = treasure
        self.plants = plants
        self.bosses = bosses
        self.dangers = dangers

        # These flags will be used to decide which buttons to render
        self.is_collision_with_monster = False
        self.is_collision_with_weapon = False
        self.is_collision_with_treasure = False
        self.is_collision_with_boss = False
        self.is_collision_with_plant = False
        self.is_collision_with_danger = False

        # Variables for tracking the player's movement over the path
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
        if clicked_button.lower() == "move":
            self.handle_player_movement()

            self.is_collision_with_monster = False
            self.is_collision_with_weapon = False
            self.is_collision_with_treasure = False
            self.is_collision_with_boss = False
            self.is_collision_with_plant = False
            self.is_collision_with_danger = False
            self.actual_entity = None
            # Monster movement
            for monster in self.monsters:
                neighbors = list(self.graph.neighbors(monster.position))
                if neighbors:
                    new_position = random.choice(list(neighbors + [monster.position]))
                    monster.position = new_position

            # Collision detection
            for entity in self.monsters + self.weapons + self.bosses + self.dangers + self.plants + [self.treasure]:
                if entity.position == self.player.position:
                    if isinstance(entity, Monster):
                        print("Encontrou um monstro")
                        self.is_collision_with_monster = True
                        # TODO: Add proper battle logic here
                    if isinstance(entity, Weapon):
                        print("Encontrou uma arma")
                        self.is_collision_with_weapon = True
                        pass
                    if isinstance(entity, Treasure):
                        self.is_collision_with_treasure = True
                        # implementar o pick up para poder recolher o tesouro
                        self.player.treasure = self.player.max_treasure
                        treasure_bar.attribute = self.player.max_treasure
                        print("Chegou ao tesouro!")
                    if isinstance(entity, Boss):
                        self.is_collision_with_boss = True
                        print("Encontrou um chefão")
                    if isinstance(entity, Danger):
                        self.is_collision_with_danger = True
                        self.player.health -= entity.damage
                        health_bar.attribute -= entity.damage
                        print("Encontrou um perigo, -" + str(entity.damage) + "hp")

                    if isinstance(entity, Plant):
                        self.is_collision_with_plant = True
                        frase = "+" + str(entity.cure) + "hp"
                        if (self.player.health + entity.cure > 100):
                            health_bar.attribute = 100
                            self.player.health = 100
                        else:
                            health_bar.attribute += entity.cure
                            self.player.health += entity.cure
                        print("Encontrou uma planta medicinal, +" + str(entity.cure) + "hp")
                    self.actual_entity = entity

    def game_over(self):
        player_won = False
        player_lost = False
        if self.player.health == 0 or self.time_left == 0:
            player_lost = True
            print("Player lost!")
            return -1
        if self.player.position == (0,0) and self.time != 0:
            player_won = True
            print("Player won!")
            lost = DialogBox("Won", "haha")
            lost.draw()
            return 1

        return 0
            





class GameInterface:
    MOVE = 0
    FIGHT = 1
    PICK_UP = 2
    END_TURN = 3

    def __init__(self, game_manager: GameManager):
        self.buttons = [
            Button("MOVE", (260, 470)),
            Button("FIGHT", (355, 470)),
            Button("PICK UP", (450, 470)),
            Button("DROP", (400, 545)),
            Button("End Turn", (400, 545))
        ]
        self.game_manager = game_manager

    def draw(self, screen):
        if self.game_manager.is_collision_with_monster:
            self.buttons[self.FIGHT].draw(screen)
            draw_monster(self.game_manager.actual_entity.health, self.game_manager.actual_entity.attack_points)
        if self.game_manager.is_collision_with_weapon:
            self.buttons[self.PICK_UP].draw(screen)
            draw_weapon(self.game_manager.actual_entity.attack_bonus)
        if self.game_manager.is_collision_with_treasure:
            self.buttons[self.PICK_UP].draw(screen)
            draw_treasure()
        if self.game_manager.is_collision_with_plant:
            draw_plant(self.game_manager.actual_entity.cure)
        if self.game_manager.is_collision_with_danger:
            draw_danger(self.game_manager.actual_entity.damage)
        if self.game_manager.is_collision_with_boss:
            draw_boss(self.game_manager.actual_entity.health, self.game_manager.actual_entity.attack_points)
        self.buttons[self.MOVE].draw(screen)

        time_surface = font.render(f"Tempo: {self.game_manager.time}", True, WHITE)
        screen.blit(time_surface, (640, 22))
        # time_left_surface = font.render(f"Tempo restante: {self.game_manager.time_left}", True, GRAY)
        # screen.blit(time_left_surface, (50, 100))

    def handle_click(self, position):
        for button in self.buttons:
            if button.rect.collidepoint(position):
                return button.text
        return None

    def increment_time(self):
        self.game_manager.time += 1
        self.game_manager.time_left -= 1


# Create instances of player, monsters, weapons, and treasure
player = Player((0, 0))
treasure = Treasure((7, 4))

# Player's status
heart = pygame.image.load('assets/icons/heart.png')
sword = pygame.image.load('assets/icons/sword.png')
chest = pygame.image.load('assets/icons/chest.png')
health_bar = Bar(120, 470, player.health, 100, (104, 89, 30), heart)
treasure_bar = Bar(120, 510, player.treasure, 100, (211, 142, 49), chest)
attack_bar = Bar(120, 550, player.attack_points, 50, (153, 41, 21), sword)

# Place monsters, weapons and dangers randomly on the graph
# Together they should be 20%~30% of the number of edges

# Calculate the number of entities (monsters, weapons, dangers) based on the percentage range
num_entities = random.randint(round(m * 0.20), round(m * 0.30))

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


# Generate random entities and objects into the island
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
                dangers.append(Danger(position))
            elif entity_type == 'plant':
                plants.append(Plant(position))
            elif entity_type == 'boss':
                bosses.append(Boss(position))
            break  # Exit the loop if entity is successfully placed

# Find a path from the initial node to the treasure node
path = random_path(G, player.position, treasure.position)

# Create game manager and game interface
game_manager = GameManager(G, path, player, treasure, monsters, weapons, plants, bosses, dangers)
game_interface = GameInterface(game_manager)

# Mark the edges along the path as black
for i in range(len(path) - 1):
    G[path[i]][path[i + 1]]['color'] = (171, 171, 171)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_button = game_interface.handle_click(pygame.mouse.get_pos())
            if clicked_button is not None:
                game_interface.increment_time()

                game_manager.update_game_state(clicked_button)

                game_manager.game_over()

    # Clear the screen
    screen.fill(WHITE)
    background_map(background)
    draw_menu_interface()

    # Draw nodes and edges of the graph
    for node in G.nodes:
        pygame.draw.circle(screen, BLACK, graph_to_screen(node), 5)

    for edge in G.edges:
        color = G[edge[0]][edge[1]].get('color', BLACK)
        pygame.draw.line(screen, color, graph_to_screen(edge[0]), graph_to_screen(edge[1]), 2)

    # Draw entities
    for boss in bosses:
        if boss.health > 0:
            boss.draw()
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

    health_bar.draw(screen)
    treasure_bar.draw(screen)
    attack_bar.draw(screen)

    # Draw game interface
    game_interface.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
