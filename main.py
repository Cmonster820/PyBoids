import pygame # type: ignore
import sys
from boids import *
from constants import *

def main():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    boids = pygame.sprite.Group()
    predators = pygame.sprite.Group()
    food = pygame.sprite.Group()
    Boid.containers = (updatable,drawable)
    Food.containers = (food,updatable,drawable)
    Predator.containers = (predators,updatable)
    print(f"Starting Boids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    for i in range(10):
        Boid()
    while 1: #game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        for thing in updatable:
            thing.update(boids)
            thing.position+=thing.velocity*dt
        screen.fill("black")
        for thing in drawable:
            thing.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()