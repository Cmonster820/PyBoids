import pygame # type: ignore
import random
from constants import *
from enum import *
from utils import *

class BoidState(Enum):
    SEARCHING = 0
    NORMAL = 1
    EVADE = 2
    CHASE = 3

class Boid(pygame.sprite.Sprite):
    def __init__(self, position = None):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        if position is None:
            self.position = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) 
        else:
            self.position = position
        self.rotation = random.uniform(0,360)
        self.velocity = pygame.Vector2(SPEED_BOID_SEARCHING).rotate(self.rotation)
        self.neighbors = []


    def update(self, group):
        min_dist = float("inf")
        closest_boid = Boid()
        for boid in group:
            dist = self.position.distance_to(boid.position)
            if min_dist < dist:
                closest_boid = boid
                min_dist = dist
            if dist<NEIGHBOR_RANGE:
                self.neighbors.append(boid)
        
        


class Predator(Boid):
    pass

class Food(pygame.sprite.Sprite):
    pass