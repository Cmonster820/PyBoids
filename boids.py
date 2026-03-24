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
            average_neighbor_position = sum([boid.position for boid in self.neighbors])/len(self.neighbors)
            average_neighbor_rotation = self.velocity.angle_to(average_neighbor_position)
            self.rotation+=lerp(-MAX_ROTATION_PER_FRAME,MAX_ROTATION_PER_FRAME,average_neighbor_rotation-self.rotation)
            self.rotation+=random.uniform(-RANDOM_ROTATION,RANDOM_ROTATION)
        else:
            self.state = BoidState.SEARCHING
        
        for boid in self.neighbors:
            if self.position.distance_to(boid.position) < RANGE:
                self.rotation+=lerp(-MAX_ROTATION_PER_FRAME,MAX_ROTATION_PER_FRAME,-(self.rotation-self.velocity.angle_to(boid.position)))
        if self.position.x<SIDE_THRESHOLD or SCREEN_WIDTH-self.position.x<SIDE_THRESHOLD:
            self.rotation+=lerp(-3*MAX_ROTATION_PER_FRAME,3*MAX_ROTATION_PER_FRAME, self.velocity.angle_to(pygame.Vector2(-self.velocity.x,self.velocity.y)))
        if self.position.y<SIDE_THRESHOLD or SCREEN_HEIGHT-self.position.y<SIDE_THRESHOLD:
            self.rotation+=lerp(-3*MAX_ROTATION_PER_FRAME,3*MAX_ROTATION_PER_FRAME, self.velocity.angle_to(pygame.Vector2(self.velocity.x,-self.velocity.y)))
        self.rotation+=random.uniform(-RANDOM_ROTATION,RANDOM_ROTATION)
        self.rotation%=360
        self.velocity = self.velocity.rotate(self.rotation-self.velocity.angle_to(pygame.Vector2(0,1)))
        self.velocity = self.velocity.normalize()*self.state.value

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * 5
        a = self.position + forward * 5
        b = self.position - forward * 5 - right
        c = self.position - forward * 5 + right
        return [a, b, c]

    def draw(self,screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        
        
        


class Predator(Boid):
    pass

class Food(pygame.sprite.Sprite):
    pass