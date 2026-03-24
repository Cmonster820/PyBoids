import pygame # type: ignore
import random
from constants import *
from enum import *
from utils import *

class BoidState(Enum):
    SEARCHING = SPEED_BOID_SEARCHING
    NORMAL = SPEED_BOID_NORMAL
    EVADE = SPEED_BOID_EVADE
    CHASE = SPEED_PREDATOR

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
        self.velocity = pygame.Vector2(SPEED_BOID_SEARCHING).rotate(self.rotation+90)
        self.neighbors = []
        self.state = BoidState.SEARCHING


    def update(self, group):
        min_dist = float("inf")
        closest_boid = None
        for boid in group:
            dist = self.position.distance_to(boid.position)
            if min_dist < dist:
                closest_boid = boid
                min_dist = dist
            if dist<NEIGHBOR_RANGE:
                self.neighbors.append(boid)
        if len(self.neighbors)>0:
            self.state = BoidState.NORMAL
        else:
            self.state = BoidState.SEARCHING
        average_neighbor_position = sum(neighbors.position)/len(neighbors)
        average_neighbor_rotation = self.velocity.angle_to(average_neighbor_position)
        self.rotation+=lerp(-MAX_ROTATION_PER_FRAME,MAX_ROTATION_PER_FRAME,average_neighbor_rotation-self.rotation)
        self.rotation+=random.uniform(-RANDOM_ROTATION,RANDOM_ROTATION)
        for boid in neighbors:
            if self.position.distance_to(boid.position) < RANGE:
                self.rotation+=lerp(-MAX_ROTATION_PER_FRAME,MAX_ROTATION_PER_FRAME,-(self.rotation-self.velocity.angle_to(boid.position)))
        
        self.rotation+=random.uniform(-RANDOM_ROTATION,RANDOM_ROTATION)
        self.rotation%=360
        self.velocity = self.velocity.rotate(self.rotation-self.velocity.angle_to(Vector2(0,1)))
        self.velocity = self.velocity.normalize()*self.state.value
        
        
        


class Predator(Boid):
    pass

class Food(pygame.sprite.Sprite):
    pass