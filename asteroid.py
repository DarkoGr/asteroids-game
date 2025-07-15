import pygame
import random
from circleshape import CircleShape

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

