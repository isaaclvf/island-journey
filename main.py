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
n = len(G.nodes)

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
    pygame.draw.rect(screen, (109, 54, 22), (670, 470, 110, 70), 3)
    # dialog
    pygame.draw.rect(screen, (0, 0, 0), (260, 510, 380, 30))
    # time window
    pygame.draw.rect(screen, (109, 54, 22), (630, 20, 150, 40))


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
        if self.armed:
            self.drop_weapon()

        weapon.being_used = True
        self.armed = True
        self.attack_points += weapon.attack_bonus
        self.weapon = weapon

        if self.with_treasure:
            # TODO: Verify if this is correct
            self.treasure -= self.treasure * (weapon.attack_bonus / 100)

    def drop_weapon(self):
        self.attack_points -= self.weapon.attack_bonus
        self.armed = False
        self.weapon.being_used = False

        if self.weapon.life > 0:
            self.weapon.position = self.position
            self.weapon = None
            return True  # Weapon can still be used
        else:
            del self.weapon
            return False

    def draw(self):
        pygame.draw.circle(screen, (106, 55, 113), graph_to_screen(self.position), 10)

    def handle_weapon_damage(self):
        if self.armed:
            weapon.life -= 1
            if weapon.life <= 0:
                print("Sua arma foi destruída")
                self.drop_weapon()

    def cure(self, plant):
        self.health += plant.cure
        if self.health > self.max_health:
            self.health = self.max_health

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
        self.attack_bonus = random.randint(5, 20)
        self.life = 3
        self.being_used = False
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
    MAX_TREASURE = 10_000

    def __init__(self, position):
        self.position = position
        self.value = self.MAX_TREASURE

    def draw(self):
        pygame.draw.circle(screen, GOLD, graph_to_screen(self.position), 10)


class Button:
    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.font = pygame.font.Font('assets/VT323-Regular.ttf', 24)
        self.rect = pygame.Rect(position[0], position[1], 85, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, (109, 54, 22), self.rect)
        pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 3, 30))
        pygame.draw.rect(screen, (58, 30, 13), (self.position[0] + 82, self.position[1], 3, 30))
        pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 85, 3))
        pygame.draw.rect(screen, (58, 30, 13), (self.position[0], self.position[1] + 27, 85, 3))

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
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 110, 30))
        pygame.draw.rect(screen, self.color, (self.x, self.y, 110 * ratio, 30))
        rect = pygame.draw.rect(screen, (109, 54, 22), (self.x, self.y, 110, 30), 2)
        size = pygame.transform.scale(self.icon, (30, 30))
        number = font.render(str(self.attribute), True, WHITE)
        screen.blit(size, (self.x + 80, self.y))
        screen.blit(number, (self.x + 5, self.y - 2))


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

        # Variables for handling battles
        self.is_battling = False
        self.is_player_turn = True
        self.turn_counter = 0
        self.max_turns = 3
        self.is_battle_over = False
        self.is_monster_dead = False
        self.current_enemy = None

        # Variables for tracking the player's movement over the path
        self.path = path
        self.path_index = 0
        self.is_forward = True

    def handle_player_movement(self):
        if self.path is None:
            return  # No path

        if self.is_forward:
            # Move player forward on the path
            self.path_index += 1
            if self.path_index < len(self.path):
                next_position = self.path[self.path_index]
                self.player.position = next_position
            else:
                self.path_index -= 2  # Move back two steps to start walking back
                # Reached the end of the path, start walking back
                self.is_forward = False
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

    def handle_monsters_movement(self):
        for monster in self.monsters:
            neighbors = list(self.graph.neighbors(monster.position))
            if neighbors:
                new_position = random.choice(list(neighbors + [monster.position]))
                monster.position = new_position

    def handle_bosses_movement(self):
        for boss in self.bosses:
            neighbors = list(self.graph.neighbors(boss.position))
            if neighbors:
                new_position = random.choice(list(neighbors + [boss.position]))
                boss.position = new_position

    def reset_collision_flags(self):
        # self.is_collision_with_monster = False
        # self.is_collision_with_boss = False

        self.is_collision_with_weapon = False
        self.is_collision_with_treasure = False
        self.is_collision_with_plant = False
        self.is_collision_with_danger = False

    def handle_collisions(self):
        self.reset_collision_flags()

        # Collision detection
        for entity in self.monsters + self.weapons + self.bosses + self.dangers + self.plants + [self.treasure]:
            if entity.position == self.player.position:
                if isinstance(entity, Monster):
                    print(f"Encontrou um monstro, com ataque: {entity.attack_points} e vida: {entity.health}")
                    print("Começando batalha, é o seu turno")

                    self.is_battling = True
                    self.is_collision_with_monster = True
                    self.current_enemy = entity
                    self.turn_counter = 0

                if isinstance(entity, Boss):
                    print(f"Encontrou um chefão, com ataque: {entity.attack_points} e vida: {entity.health}")
                    print("Começando batalha, é o seu turno")

                    self.is_battling = True
                    self.is_collision_with_boss = True
                    self.current_enemy = entity
                    self.turn_counter = 0

                if isinstance(entity, Weapon):
                    print(f"Encontrou uma arma com {entity.attack_bonus} pontos de ataque")
                    self.is_collision_with_weapon = True

                if isinstance(entity, Treasure):
                    self.is_collision_with_treasure = True

                    print(f"Chegou ao tesouro! O valor total é de {entity.value} moedas de ouro.")
                    self.player.with_treasure = True
                    self.player.max_treasure = self.player.health
                    if self.player.weapon is not None:
                        self.player.max_treasure -= self.player.weapon.attack_bonus

                    self.player.treasure = entity.value * (self.player.max_treasure / 100)

                    print(
                        f"Você pode carregar {self.player.max_treasure}% desse tesouro: {self.player.treasure} moedas")

                if isinstance(entity, Danger):
                    self.is_collision_with_danger = True
                    # TODO: Implement danger logic
                    print("Encontrou um perigo... O que o perigo faz mesmo?")

                if isinstance(entity, Plant):
                    self.is_collision_with_plant = True
                    print(f"Encontrou uma planta medicinal com {entity.cure} pontos de cura")

    def switch_battle_turns(self):
        self.is_player_turn = not self.is_player_turn
        if self.is_player_turn:
            self.turn_counter += 1

    def update_game_state(self, clicked_button):
        if self.is_battling:
            if self.is_player_turn:
                if clicked_button is not None and clicked_button.lower() == "fight":
                    infringed_attack = random.randint(1, self.player.attack_points)
                    print(f"Seu ataque foi de {infringed_attack} pontos")
                    self.current_enemy.health -= infringed_attack

                    if self.current_enemy.health <= 0:
                        self.is_monster_dead = True
                        print("Você derrotou o inimigo!")
                    else:
                        print(f"Agora o inimigo está com {self.current_enemy.health} pontos de vida")

                    self.switch_battle_turns()
                    self.increment_time()

                elif clicked_button is not None and clicked_button.lower() == "run":
                    self.player.health -= self.current_enemy.attack_points
                    # self.player.handle_weapon_damage()  # Running damages the weapon anyway
                    self.is_battle_over = True
                    self.is_battling = False

                    print(f"Você fugiu e perdeu {self.current_enemy.attack_points} pontos de vida")

                    # TODO: Verify if this is correct
                    if self.player.with_treasure:
                        print("Você perdeu uma parte do tesouro na fuga")
                        self.player.treasure -= self.player.treasure * (self.current_enemy.attack_points / 100)

                    self.current_enemy = None
                    self.is_player_turn = True
                    self.handle_player_movement()
                    self.increment_time()
                    self.handle_collisions()
            else:
                # Enemy's turn
                print("Turno do inimigo")
                infringed_attack = random.randint(1, self.current_enemy.attack_points)
                print(f"O ataque dele foi de {infringed_attack}")
                self.player.health -= infringed_attack

                # TODO: Verify if this is correct
                if self.player.with_treasure:
                    self.player.treasure -= self.player.treasure * (infringed_attack / 100)

                print("Seu turno")

                self.switch_battle_turns()
                self.increment_time()

            # Check if battle is over
            if self.player.health <= 0 or self.is_monster_dead:
                print("A batalha acabou")

                self.is_battle_over = True
                self.is_battling = False
                self.current_enemy = None  # TODO: Might be del self.current_enemy (?) here
                self.turn_counter = 0
                self.is_monster_dead = False

                self.player.handle_weapon_damage()

                # TODO: Check game over here (player might me dead)
            elif self.turn_counter >= self.max_turns:
                self.is_battle_over = True
                self.is_battling = False
                self.turn_counter = 0

                self.player.handle_weapon_damage()

                # Enemy runs away
                print("O inimigo fugiu")
                if self.current_enemy is not None:
                    neighbors = list(self.graph.neighbors(self.current_enemy.position))
                    new_position = random.choice(list(neighbors))
                    self.current_enemy.position = new_position
                    self.current_enemy = None

        if clicked_button is not None and clicked_button.lower() == "move":
            self.handle_player_movement()
            self.handle_monsters_movement()
            self.handle_bosses_movement()
            self.handle_collisions()
            self.increment_time()

        if clicked_button is not None and clicked_button.lower() == "pick up":
            for entity in self.weapons + self.plants + [self.treasure]:
                if entity.position == self.player.position:
                    if isinstance(entity, Weapon):
                        print("Você escolheu pegar essa arma")
                        if self.player.armed:
                            print("A arma foi trocada")
                        self.player.pick_weapon(entity)
                        self.is_collision_with_weapon = False

                    if isinstance(entity, Plant):
                        print("Você escolheu pegar essa cura")
                        self.player.cure(entity)
                        self.is_collision_with_plant = False

                    if isinstance(entity, Treasure):
                        # TODO: Should the player click on pick up to get the treasure?
                        print("Agora você com certeza está carregando o tesouro")
            self.increment_time()

        if clicked_button is not None and clicked_button.lower() == "drop":
            can_still_use = self.player.drop_weapon()
            if can_still_use:
                self.is_collision_with_weapon = True

    def game_over(self):
        player_won = False
        player_lost = False
        if self.player.health == 0 or self.time_left == 0:
            player_lost = True
            print("Player lost!")
            return -1
        if self.player.position == (0, 0) and self.time != 0:
            player_won = True
            print("Player won!")
            lost = DialogBox("Won", "haha")
            lost.draw()
            return 1

        return 0

    def increment_time(self):
        self.time += 1
        self.time_left -= 1


class GameInterface:
    MOVE = 0
    FIGHT = 1
    PICK_UP = 2
    DROP = 3
    END_TURN = 4
    RUN = 5

    def __init__(self, game_manager: GameManager):
        self.buttons = [
            Button("MOVE", (260, 470)),
            Button("Fight", (200, 545)),
            Button("Pick Up", (400, 500)),
            Button("Drop", (400, 545)),
            Button("End Turn", (400, 545)),
            Button("RUN", (460, 470))
        ]

        self.game_manager = game_manager

    def draw(self, screen):
        if self.game_manager.is_battling:
            self.buttons[self.FIGHT].draw(screen)
            self.buttons[self.RUN].draw(screen)
        elif self.game_manager.is_collision_with_weapon \
                or self.game_manager.is_collision_with_treasure \
                or self.game_manager.is_collision_with_plant:
            self.buttons[self.PICK_UP].draw(screen)
            self.buttons[self.MOVE].draw(screen)
        else:
            self.buttons[self.MOVE].draw(screen)

        if self.game_manager.player.armed:
            self.buttons[self.DROP].draw(screen)

        time_surface = font.render(f"Tempo: {self.game_manager.time}", True, WHITE)
        screen.blit(time_surface, (640, 22))
        # time_left_surface = font.render(f"Tempo restante: {self.game_manager.time_left}", True, GRAY)
        # screen.blit(time_left_surface, (50, 100))

    def handle_click(self, position):
        for button in self.buttons:
            if button.rect.collidepoint(position):
                return button.text
        return None


# Create instances of player, monsters, weapons, and treasure
player = Player((0, 0))
treasure = Treasure((7, 4))

# Player's status
heart = pygame.image.load('assets/icons/heart.png')
sword = pygame.image.load('assets/icons/sword.png')
chest = pygame.image.load('assets/icons/chest.png')
health_bar = Bar(120, 470, player.health, 100, (104, 89, 30), heart)
treasure_bar = Bar(120, 510, player.treasure, Treasure.MAX_TREASURE, (211, 142, 49), chest)
# TODO: Also show information about the weapon: attack bonus and life
attack_bar = Bar(120, 550, player.attack_points, 50, (153, 41, 21), sword)

# Place monsters, weapons and dangers randomly on the graph
# Together they should be 20%~30% of the number of edges
# TODO: 20%~30% of the number of *nodes*, actually

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
for _ in range(num_entities):
    while True:
        # Generate a random position
        position = (random.randint(0, 7), random.randint(0, 4))

        # Check if the position is valid and empty
        if is_valid_position(position) and is_empty_position(position, monsters + weapons + dangers + plants + bosses):
            # Randomly choose the type of entity to place
            entity_type = random.choice(['monster', 'weapon', 'danger', 'plant'])
            if entity_type == 'monster':
                monsters.append(Monster(position))
            elif entity_type == 'weapon':
                weapons.append(Weapon(position))
            elif entity_type == 'danger':
                dangers.append(Danger(position, damage=1))
            elif entity_type == 'plant':
                plants.append(Plant(position))
            break  # Exit the loop if entity is successfully placed

# Place three bosses on the island
for _ in range(3):
    while True:
        position = (random.randint(0, 7), random.randint(0, 4))
        if is_valid_position(position) and is_empty_position(position, monsters + weapons + dangers + plants + bosses):
            bosses.append(Boss(position))
            break

# Find a path from the initial node to the treasure node
path = random_path(G, player.position, treasure.position)

# Create game manager and game interface
game_manager = GameManager(G, path, player, treasure, monsters, weapons, plants, bosses, dangers)
game_interface = GameInterface(game_manager)

# Mark the edges along the path as green
for i in range(len(path) - 1):
    G[path[i]][path[i + 1]]['color'] = GREEN

# Main loop
running = True
while running:
    clicked_button = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_button = game_interface.handle_click(pygame.mouse.get_pos())

    game_manager.update_game_state(clicked_button)
    game_manager.game_over()
    health_bar.attribute = player.health
    treasure_bar.attribute = player.treasure
    attack_bar.attribute = player.attack_points

    # Clear the screen
    screen.fill(WHITE)
    background_map(background)
    draw_menu_interface()

    # Draw nodes and edges of the graph
    for node in G.nodes:
        pygame.draw.circle(screen, BLACK, graph_to_screen(node), 5)

    for edge in G.edges:
        color = G[edge[0]][edge[1]].get('color', BLUE)
        pygame.draw.line(screen, color, graph_to_screen(edge[0]), graph_to_screen(edge[1]), 2)

    # Draw entities
    for boss in bosses:
        boss.draw()
    for monster in monsters:
        if monster.health > 0:
            monster.draw()
    for weapon in weapons:
        if not weapon.being_used:
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
