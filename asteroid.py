import pygame
import random
from circleshape import CircleShape
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        min_speed = -50
        max_speed = 50
        velocity_x = random.uniform(min_speed, max_speed)
        velocity_y = random.uniform(min_speed, max_speed)
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y)
    
    def draw(self, screen):
        return pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    
        
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 
        else:
            split_asteroid_angle = random.uniform(20, 50)
            new_velocity_first = self.velocity.rotate(split_asteroid_angle)
            new_velocity_second = self.velocity.rotate(-split_asteroid_angle)
            new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
            smaller_asteroid_1 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
            smaller_asteroid_2 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
            smaller_asteroid_1.velocity = new_velocity_first * 1.2
            smaller_asteroid_2.velocity = new_velocity_second* 1.2

            

