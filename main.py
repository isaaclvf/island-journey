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

tela_inicio = pygame.image.load("assets/screens/telaInicio.png")
tela_morte = pygame.image.load("assets/screens/telaMorte.png")
tela_vitoria = pygame.image.load("assets/screens/telaVitoria.png")

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
object_rect = pygame.draw.rect(screen, (0, 0, 0), (670, 550, 110, 30))

def update_i():
    i = random.randrange(1, 3, 1)
    return i

i = update_i()

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
    # Character
    pygame.draw.rect(screen, (109, 54, 22), (20, 470, 90, 110))
    bg1_place()
    character_place()
    pygame.draw.rect(screen, (109, 54, 22), (20, 470, 90, 110), 3)
    # Object
    pygame.draw.rect(screen, (0, 0, 0), (670, 470, 110, 70))
    bg2_place()
    pygame.draw.rect(screen, (0, 0, 0), (670, 550, 110, 30))
    pygame.draw.rect(screen, (109, 54, 22), (670, 470, 110, 70), 3)
    # Time window
    pygame.draw.rect(screen, (109, 54, 22), (630, 20, 150, 40))


# Auxiliar graphic's functions
def draw_monster(hp, ap):
    object = pygame.image.load('assets/monsters/monstro.png')
    size = pygame.transform.scale(object, (110, 70))
    message1 = "Você achou um monstro com"
    rect1 = pygame.draw.rect(screen, (0, 0, 0), (260, 515, 380, 30))
    text1 = font.render(message1, True, (255, 255, 255))
    text1_rect = text1.get_rect(center=rect1.center)
    message1 = "Você achou um monstro com"
    rect1 = pygame.draw.rect(screen, (0, 0, 0), (260, 515, 380, 30))
    text1 = font.render(message1, True, (255, 255, 255))
    text1_rect = text1.get_rect(center=rect1.center)
    screen.blit(size, (670, 470))
    screen.blit(text1, text1_rect)


def draw_plant(hp):
    object = pygame.image.load('assets/objects/planta.png')
    size = pygame.transform.scale(object, (110, 70))
    message = "+" + str(hp) + "hp"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=object_rect.center)
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
    text_rect = text.get_rect(center=object_rect.center)
    screen.blit(size, (670, 470))
    screen.blit(text, text_rect)


def draw_danger(hp):
    object = pygame.image.load('assets/objects/perigo.png')
    size = pygame.transform.scale(object, (110, 70))
    message = "-" + str(hp) + "hp"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=object_rect.center)
    screen.blit(size, (670, 470))
    screen.blit(text, text_rect)


def draw_boss(hp, ap, i):
    if i == 1:
        object = pygame.image.load('assets/monsters/jacare.png')
        size = pygame.transform.scale(object, (110, 70))
        screen.blit(size, (670, 470))
    elif i == 2:
        object = pygame.image.load('assets/monsters/onca.png')
        size = pygame.transform.scale(object, (110, 70))
        screen.blit(size, (670, 470))
    else:
        object = pygame.image.load('assets/monsters/formigas.png')
        size = pygame.transform.scale(object, (110, 70))
        screen.blit(size, (670, 470))

# Gamer's path generator
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
        circle_border = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (106, 55, 113), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/jogador.png')
        img = pygame.transform.scale(load_img, (25, 25))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)

    def handle_weapon_damage(self):
        if self.armed:
            weapon.life -= 1
            if weapon.life <= 0:
                print("Sua arma foi destruída")
                self.drop_weapon()

    def attack(self, monster, weapon):
        monster.health -= self.attack_points
        if self.armed:
            weapon.life -= 1
            if weapon.life == 0:
                self.drop_weapon()

    def cure(self, plant):
        self.health += plant.cure
        if self.health > self.max_health:
            self.health = self.max_health

    def damage(self, danger):
        self.health -= danger.damage
        if self.health < 0:
            self.health = 0

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
        circle_border = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
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
        self.health = random.randrange(25, 35, 5)
        self.attack_points = random.randrange(10, 20, 1)
        self.font = pygame.font.Font(None, 24)  # Font for the attack bonus text

    def draw(self):
        circle_border = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
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
        self.attack_bonus = random.randint(5, 20)
        self.life = 3
        self.being_used = False
        self.font = pygame.font.Font(None, 24)  # Font for the attack bonus text

    def draw(self):
        circle = pygame.draw.circle(screen, WHITE, graph_to_screen(self.position), 17)
        circle = pygame.draw.circle(screen, (109, 54, 22), graph_to_screen(self.position), 15)
        load_img = pygame.image.load('assets/icons/arma.png')
        img = pygame.transform.scale(load_img, (20, 20))
        img_rect = img.get_rect(center=circle.center)
        screen.blit(img, img_rect)


class Treasure:
    MAX_TREASURE = 10_000

    def __init__(self, position):
        self.position = position
        self.value = self.MAX_TREASURE

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
        self.rect = pygame.Rect(position[0], position[1], 64, 30)
        self.active = True

    def draw(self, screen):
        if self.active == True:
            pygame.draw.rect(screen, (109, 54, 22), self.rect)
            pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 3, 30))
            pygame.draw.rect(screen, (58, 30, 13), (self.position[0] + 61, self.position[1], 3, 30))
            pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 64, 3))
            pygame.draw.rect(screen, (58, 30, 13), (self.position[0], self.position[1] + 27, 64, 3))

            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        else:
            pygame.draw.rect(screen, (109, 54, 22), self.rect)
            pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 3, 30))
            pygame.draw.rect(screen, (58, 30, 13), (self.position[0] + 61, self.position[1], 3, 30))
            pygame.draw.rect(screen, (142, 101, 77), (self.position[0], self.position[1], 64, 3))
            pygame.draw.rect(screen, (58, 30, 13), (self.position[0], self.position[1] + 27, 64, 3))

            text_surface = self.font.render(self.text, True, GRAY)
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
        screen.blit(number, (self.x + 5, self.y - 2))


# IMPLEMENTAR DIALOGBOX
class DialogBox:
    def __init__(self, message_1, message_2):
        self.message_1 = message_1
        self.message_2 = message_2

    def draw(self):
        background = pygame.draw.rect(screen, (0, 0, 0), (260, 510, 380, 70))
        rect1 = pygame.draw.rect(screen, (0, 0, 0), (260, 515, 380, 30))
        text1 = font.render(self.message_1, True, (255, 255, 255))
        text1_rect = text1.get_rect(center=rect1.center)
        rect2 = pygame.draw.rect(screen, (0, 0, 0), (260, 545, 380, 30))
        text2 = font.render(self.message_2, True, (255, 255, 255))
        text2_rect = text2.get_rect(center=rect2.center)
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)


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
        self.static_entity = None
        self.dynamic_entity = None

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
        self.is_boss_dead = False
        self.current_enemy = None
        self.last_attack = 0

        # Variables for tracking the player's movement over the path
        self.path = path
        self.path_index = 0
        self.is_forward = True

        # Game state variables
        self.game_over = False
        self.player_won = False

        # Checkpoints
        self.checkpoints = [path[len(path) // 2]]
        self.current_checkpoint = None

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
                # Choose a new path to go back
                self.path = random_path(self.graph, (0,0), (7,4))
                self.checkpoints = [self.path[len(self.path) // 2]]

                self.update_graph_colors()

                self.path_index = len(self.path) - 1
                # Reached the end of the path, start walking back
                self.is_forward = False
                next_position = self.path[self.path_index]
                self.player.position = next_position
        else:
            # Move player back on the path
            self.path_index -= 1
            if self.path_index >= 0:
                next_position = self.path[self.path_index]
                self.player.position = next_position
            else:
                # Reached the start of the path, start walking forward again
                self.is_forward = True
                self.path_index = 1

    def update_graph_colors(self):
        # Set all edge colors to blue
        for u, v in self.graph.edges():
            self.graph[u][v]['color'] = BLUE

        # Update edges along the path to a different color
        for i in range(len(self.path) - 1):
            u, v = self.path[i], self.path[i + 1]
            self.graph[u][v]['color'] = (171, 171, 171)

    def handle_monsters_movement(self):
        for monster in self.monsters:
            neighbors = list(self.graph.neighbors(monster.position))
            if neighbors:
                new_position = random.choice(list(neighbors + [monster.position]))
                monster.position = new_position

            # Check for collisions
            # Create a dictionary to store the positions of all monsters
            monster_positions = {}
            for monster in self.monsters:
                position = monster.position
                if position in monster_positions:
                    monster_positions[position].append(monster)
                else:
                    monster_positions[position] = [monster]

            # Check for collisions between monsters at the same position
            for position, monsters_at_position in monster_positions.items():
                if len(monsters_at_position) > 1:
                    biggest_monster = max(monsters_at_position, key=lambda x: x.health)
                    smallest_monster = min(monsters_at_position, key=lambda x: x.health)
                    other_monsters = [monster for monster in monsters_at_position if
                                      monster is not biggest_monster and monster is not smallest_monster]
                    biggest_monster.health -= smallest_monster.attack_points
                    for monster in other_monsters:
                        monster.health -= biggest_monster.attack_points
                    self.monsters.remove(smallest_monster)
                    self.spawn_new_monster()

    def handle_bosses_movement(self):
        for boss in self.bosses:
            neighbors = list(self.graph.neighbors(boss.position))
            if neighbors:
                new_position = random.choice(list(neighbors + [boss.position]))
                boss.position = new_position

    def spawn_new_monster(self):
        # Spawn a new monster at a random position on the graph
        new_position = random.choice(list(self.graph.nodes))
        self.monsters.append(Monster(new_position))

    def reset_collision_flags(self):
        # self.is_collision_with_monster = False
        # self.is_collision_with_boss = False

        self.is_collision_with_weapon = False
        self.is_collision_with_treasure = False
        self.is_collision_with_plant = False
        self.is_collision_with_danger = False

    def handle_collisions(self):
        self.reset_collision_flags()

        # Static collision detection
        for entity in self.weapons + self.dangers + self.plants + [self.treasure]:
            if entity.position == self.player.position:
                if isinstance(entity, Weapon):
                    print(f"Encontrou uma arma com {entity.attack_bonus} pontos de ataque")
                    self.is_collision_with_weapon = True
                    self.static_entity = entity
                elif isinstance(entity, Treasure):
                    self.is_collision_with_treasure = True
                    self.static_entity = entity
                    draw_treasure()
                    print(f"Chegou ao tesouro! O valor total é de {entity.value} moedas de ouro.")
                    self.player.with_treasure = True
                    self.player.max_treasure = self.player.health
                    if self.player.weapon is not None:
                        self.player.max_treasure -= self.player.weapon.attack_bonus

                    self.player.treasure = entity.value * (self.player.max_treasure / 100)

                    print(
                        f"Você pode carregar {self.player.max_treasure}% desse tesouro: {self.player.treasure} moedas")
                elif isinstance(entity, Danger):
                    self.is_collision_with_danger = True
                    self.static_entity = entity
                    draw_danger(entity.damage)
                    # TODO: Implement danger logic
                    print(f"Encontrou um perigo que lhe causou {entity.damage} pontos de dano")
                    self.player.damage(entity)
                    if self.player.health <= 0:
                        self.handle_player_death()
                elif isinstance(entity, Plant):
                    self.is_collision_with_plant = True
                    self.static_entity = entity
                    print(f"Encontrou uma planta medicinal com {entity.cure} pontos de cura")
                else:
                    self.static_entity = None

        # Dynamic collision detection
        for entity in self.monsters + self.bosses:
            if entity.position == self.player.position:
                if isinstance(entity, Monster):
                    print(f"Encontrou um monstro, com ataque: {entity.attack_points} e vida: {entity.health}")
                    print("Começando batalha, é o seu turno")

                    self.is_battling = True
                    self.is_collision_with_monster = True
                    self.dynamic_entity = entity
                    self.current_enemy = entity
                    self.turn_counter = 0
                elif isinstance(entity, Boss):
                    print(f"Encontrou um chefão, com ataque: {entity.attack_points} e vida: {entity.health}")
                    print("Começando batalha, é o seu turno")

                    self.is_battling = True
                    self.dynamic_entity = entity
                    self.is_collision_with_boss = True
                    self.current_enemy = entity
                    self.turn_counter = 0
                else:
                    self.dynamic_entity = None

        for checkpoint in self.checkpoints:
            if self.player.position == checkpoint:
                print("Você encontrou um checkpoint!")
                self.current_checkpoint = checkpoint

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
                        self.is_collision_with_boss = False
                        self.is_collision_with_monster = False
                        print("Você derrotou o inimigo!")
                    else:
                        print(f"Agora o inimigo está com {self.current_enemy.health} pontos de vida")

                    self.switch_battle_turns()
                    self.increment_time()

                elif clicked_button is not None and clicked_button.lower() == "leave":
                    self.player.health -= self.current_enemy.attack_points
                    # self.player.handle_weapon_damage()  # Running damages the weapon anyway
                    self.is_battle_over = True
                    self.is_battling = False

                    self.is_collision_with_boss = False
                    self.is_collision_with_monster = False

                    print(f"Você fugiu e perdeu {self.current_enemy.attack_points} pontos de vida")

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

                if self.player.with_treasure:
                    self.player.treasure -= self.player.treasure * (infringed_attack / 100)

                print("Seu turno")

                self.switch_battle_turns()
                self.increment_time()

            # Check if battle is over
            if self.player.health <= 0 or self.is_monster_dead:
                print("A batalha acabou")

                if self.current_checkpoint:
                    self.player.position = self.current_checkpoint

                self.is_battle_over = True
                self.is_battling = False
                self.current_enemy = None
                self.turn_counter = 0
                self.is_monster_dead = False

                self.is_collision_with_boss = False
                self.is_collision_with_monster = False

                self.player.handle_weapon_damage()

                if self.player.health <= 0:
                    self.handle_player_death()

            elif self.turn_counter >= self.max_turns:
                self.is_battle_over = True
                self.is_battling = False
                self.turn_counter = 0

                self.player.handle_weapon_damage()

                # Enemy runs away
                print("O inimigo fugiu")
                self.is_collision_with_boss = False
                self.is_collision_with_monster = False
                if self.current_enemy is not None:
                    neighbors = list(self.graph.neighbors(self.current_enemy.position))
                    new_position = random.choice(list(neighbors))
                    self.current_enemy.position = new_position
                    self.current_enemy = None

        if clicked_button is not None and clicked_button.lower() == "move":
            update_i()
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
                            self.is_collision_with_weapon = True
                        else:
                            self.is_collision_with_weapon = False
                        self.player.pick_weapon(entity)

                    if isinstance(entity, Plant):
                        print("Você escolheu pegar essa cura")
                        self.player.cure(entity)
                        self.plants.remove(entity)
                        self.is_collision_with_plant = False

                    if isinstance(entity, Treasure):
                        print("Agora você com certeza está carregando o tesouro")
            self.increment_time()

        if clicked_button is not None and clicked_button.lower() == "drop":
            can_still_use = self.player.drop_weapon()
            if can_still_use:
                self.is_collision_with_weapon = True

    def is_game_over(self):
        self.game_over = self.player.health == 0 or self.time_left == 0
        self.player_won = self.player.position == (0, 0) and self.time != 0
        return self.game_over or self.player_won

    def has_player_won(self):
        self.player_won = self.player.position == (0, 0) and self.time != 0
        return self.player_won

    def handle_player_death(self):
        if self.current_checkpoint:
            # Respawn player at the last checkpoint
            if self.player.armed:
                self.player.drop_weapon()
            self.player.position = self.current_checkpoint
            self.player.health = 100  # Reset player's health
            self.current_checkpoint = None

    def increment_time(self):
        self.time += 1
        self.time_left -= 1


class GameInterface:
    MOVE = 0
    PICK_UP = 1
    DROP = 2
    FIGHT = 3
    LEAVE = 4

    def __init__(self, game_manager: GameManager, dialog_box: DialogBox):
        self.buttons = [
            Button("MOVE", (260, 470)),
            Button("PICK UP", (336, 470)),
            Button("DROP", (412, 470)),
            Button("FIGHT", (488, 470)),
            Button("LEAVE", (564, 470))
        ]
        self.game_manager = game_manager
        self.dialog_box = dialog_box

    i = random.randrange(1, 3, 1)

    def draw(self, screen):

        for button in self.buttons:
            button.active = False

        if self.game_manager.is_battling:
            self.buttons[self.FIGHT].active = True
            self.buttons[self.LEAVE].active = True
        elif self.game_manager.is_collision_with_weapon \
                or self.game_manager.is_collision_with_treasure \
                or self.game_manager.is_collision_with_plant:
            self.buttons[self.PICK_UP].active = True
            self.buttons[self.MOVE].active = True
        else:
            self.buttons[self.MOVE].active = True

        if self.game_manager.player.armed:
            self.buttons[self.DROP].active = True

        if self.game_manager.is_collision_with_monster:
            self.buttons[self.FIGHT].draw(screen)
            health, attack = self.game_manager.dynamic_entity.health, self.game_manager.dynamic_entity.attack_points
            draw_monster(health, attack)
            self.dialog_box.message_1 = "Você achou um monstro com"
            self.dialog_box.message_2 = f"HP: {health} e AP: {attack}. Cuidado!"
        if self.game_manager.is_collision_with_weapon:
            self.buttons[self.PICK_UP].draw(screen)
            attack_bonus = self.game_manager.static_entity.attack_bonus
            draw_weapon(attack_bonus)
            self.dialog_box.message_1 = "Você achou uma arma com"
            self.dialog_box.message_2 = f"bônus de {attack_bonus}AP. Bom proveito!"
        if self.game_manager.is_collision_with_treasure:
            self.game_manager.player.with_treasure = True
            self.game_manager.player.max_treasure = self.game_manager.player.health
            if self.game_manager.player.weapon is not None:
                self.game_manager.player.max_treasure -= self.game_manager.player.weapon.attack_bonus

            self.game_manager.player.treasure = self.game_manager.treasure.value * (self.game_manager.player.max_treasure / 100)
            treasure = int(self.game_manager.player.treasure)
            self.buttons[self.PICK_UP].draw(screen)
            draw_treasure()
            self.dialog_box.message_1 = "Você encontrou o tesouro!"
            self.dialog_box.message_2 = f"Leve até {treasure} moedas."
        if self.game_manager.is_collision_with_plant:
            cure = self.game_manager.static_entity.cure
            draw_plant(cure)
            self.dialog_box.message_1 = "Você achou uma planta com"
            self.dialog_box.message_2 = f"cura de {cure}HP. Bom proveito!"
        if self.game_manager.is_collision_with_danger:
            damage = self.game_manager.static_entity.damage
            draw_danger(damage)
            self.dialog_box.message_1 = "Tome cuidado! Você"
            self.dialog_box.message_2 = f"acabou de perder {damage}HP."
        if self.game_manager.is_collision_with_boss:
            health, attack = self.game_manager.dynamic_entity.health, self.game_manager.dynamic_entity.attack_points
            draw_boss(health, attack, i)
            if i == 1:
                self.dialog_box.message_1 = "Você achou um jacarezão com"
                self.dialog_box.message_2 = f"HP: {health} e AP: {attack}. Cuidado!"
            elif i == 2:
                self.dialog_box.message_1 = "Você achou uma onça com"
                self.dialog_box.message_2 = f"HP: {health} e AP: {attack}. Cuidado!"
            else:
                self.dialog_box.message_1 = "Você achou formigas com"
                self.dialog_box.message_2 = f"HP: {health} e AP: {attack}. Cuidado!"

        if not (self.game_manager.is_collision_with_monster or \
                self.game_manager.is_collision_with_weapon or \
                self.game_manager.is_collision_with_treasure or \
                self.game_manager.is_collision_with_boss or \
                self.game_manager.is_collision_with_plant or \
                self.game_manager.is_collision_with_danger):
            self.dialog_box.message_1 = None
            self.dialog_box.message_2 = None

        self.buttons[self.MOVE].draw(screen)
        self.buttons[self.DROP].draw(screen)
        self.buttons[self.PICK_UP].draw(screen)
        self.buttons[self.FIGHT].draw(screen)
        self.buttons[self.LEAVE].draw(screen)
        self.dialog_box.draw()

        time_surface = font.render(f"Tempo: {self.game_manager.time}", True, WHITE)
        screen.blit(time_surface, (640, 22))
        # time_left_surface = font.render(f"Tempo restante: {self.game_manager.time_left}", True, GRAY)
        # screen.blit(time_left_surface, (50, 100))

    def handle_click(self, position):
        for button in self.buttons:
            if button.rect.collidepoint(position) and button.active:
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
            break  # Exit the loop if entity is successfully placed

# Place three bosses on the island
for _ in range(3):
    while True:
        position = (random.randint(0, 7), random.randint(0, 4))
        if is_valid_position(position) and is_empty_position(position,
                                                             monsters + weapons + dangers + plants + bosses):
            bosses.append(Boss(position))
            break

# Find a path from the initial node to the treasure node
path = random_path(G, player.position, treasure.position)

# Create game manager and game interface
dialog_box = DialogBox(None, None)
game_manager = GameManager(G, path, player, treasure, monsters, weapons, plants, bosses, dangers)
game_interface = GameInterface(game_manager, dialog_box)

# Mark the edges along the path as black
for i in range(len(path) - 1):
    G[path[i]][path[i + 1]]['color'] = (171, 171, 171)

# Main loop
main_loop = True
running = False
while main_loop:
    if running:
        clicked_button = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = game_interface.handle_click(pygame.mouse.get_pos())

        game_manager.update_game_state(clicked_button)
        health_bar.attribute = player.health
        treasure_bar.attribute = int(player.treasure)
        attack_bar.attribute = player.attack_points

        # Check game state
        if game_manager.is_game_over():
            running = False

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
        treasure.draw()
        player.draw()

        health_bar.draw(screen)
        treasure_bar.draw(screen)
        attack_bar.draw(screen)

        # Draw game interface
        game_interface.draw(screen)

        # Update the display
        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_manager.player_won = False
                game_manager.game_over = False
                running = True

        tela = None
        if game_manager.player_won:
            tela = tela_vitoria
        elif game_manager.game_over:
            tela = tela_morte
        else:
            tela = tela_inicio

        screen.blit(tela, (0, 0))
        # Update the display
        pygame.display.flip()



# Quit Pygame
pygame.quit()
