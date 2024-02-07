import pygame
import networkx as nx

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Visualization")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


# Function to draw the graph
def draw_graph(graph, screen):
    # Clear the screen
    screen.fill(WHITE)

    # Draw nodes
    for node in graph.nodes:
        pygame.draw.circle(screen, BLACK, node, 10)

    # Draw edges
    for edge in graph.edges:
        pygame.draw.line(screen, BLUE, edge[0], edge[1], 2)

    # Update the display
    pygame.display.flip()


# Create a sample graph using NetworkX
G = nx.Graph()
G.add_nodes_from([(100, 100), (150, 200), (300, 300), (200, 300)])
G.add_edges_from([((100, 100), (150, 200)), ((150, 200), (300, 300)), ((300, 300), (100, 100)), ((100, 100), (200, 300))])

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the graph on the screen
    draw_graph(G, screen)

# Quit Pygame
pygame.quit()
