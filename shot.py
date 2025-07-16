from circleshape import CircleShape
from constants import *
import pygame

class Shot(CircleShape):
    def __init__(self, x, y, radius, player_angle):
        super().__init__(x, y, radius)

        self.velocity = pygame.Vector2(0.1).rotate(player_angle + 45) * PLAYER_SHOOT_SPEED

   
    def draw(self, screen):
        
        return pygame.draw.circle(screen, "white", self.position, self.radius)
        
    def update(self, dt):
        
        self.position += self.velocity * dt

        
        # Ovo sprečava nakupljanje metaka koji se više ne vide
        if (self.position.x < -self.radius or 
            self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or 
            self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()