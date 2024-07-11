from math import cos, sin, atan2

import pygame

from boid import Boid, compute_distance_matrix


def rotate_2d(vector, angle):
    cos_ = cos(angle)
    sin_ = sin(angle)
    return [vector[0] * cos_ + vector[1] * sin_, -vector[0] * sin_ + vector[1] * cos_]


def draw_boids(screen, boids):
    for boid in boids:
        angle = atan2(-boid.velocity[1], boid.velocity[0])
        triangle_coordinates = [
            boid.position,
            boid.position + rotate_2d((-15, 5), angle),
            boid.position + rotate_2d((-15, -5), angle),
        ]
        pygame.draw.polygon(screen, (85, 125, 237), triangle_coordinates)


def update_position_boids(boids):
    distance_matrix = compute_distance_matrix(boids)
    for boid in boids:
        boid.update(boids, distance_matrix)


if __name__ == '__main__':

    # Initializing the boids
    window_size = (1000, 1000)
    FPS = 30
    number_of_boids = 90
    boids = [Boid(window_size) for _ in range(number_of_boids)]

    # Initialization of the modules
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode(window_size)

    # Run until the user asks to quit
    clock = pygame.time.Clock()
    running = True
    while running:

        # Fix the frames per seconds number
        clock.tick(FPS)

        # Quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the screen
        screen.fill((41, 44, 51))
        draw_boids(screen, boids)
        pygame.display.flip()

        # Update the position of the boids
        update_position_boids(boids)

    pygame.quit()
