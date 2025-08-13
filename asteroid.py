import pygame
import random
from circleshape import CircleShape
from constants import *
import random

class Asteroid(CircleShape):
    all_asteroid_images = []
    def __init__(self, x, y, radius, velocity=None, image_surface=None):
        super().__init__(x, y, radius)
        if velocity is None:
            min_speed = 20
            max_speed = 70
            velocity_x = random.uniform(min_speed, max_speed)
            velocity_y = random.uniform(min_speed, max_speed)
        else:
            self.velocity = velocity
        
        self.rotation_speed = random.uniform(-ASTEROID_ROTATION_SPEED, ASTEROID_ROTATION_SPEED) 
        self.current_rotation = random.uniform(0, 360)

        if image_surface:
            self.original_image_source = image_surface 
        elif Asteroid.all_asteroid_images:
            self.original_image_source = random.choice(Asteroid.all_asteroid_images)
        else:
            self.original_image_source = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image_source, (150, 150, 150), (int(self.radius), int(self.radius)), int(self.radius), 2)
        
        scaled_size = int(self.radius * 2) 
        self.original_scaled_image = pygame.transform.scale(self.original_image_source, (scaled_size, scaled_size))
    
        self.image = self.original_scaled_image.copy() 
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    
        
    def update(self, dt):
        self.position += self.velocity * dt

        # if self.position.x + self.radius < 0:
        #     self.position.x += SCREEN_WIDTH + (2 * self.radius)
        # elif self.position.x - self.radius > SCREEN_WIDTH:
        #     self.position.x -= SCREEN_WIDTH + (2 * self.radius)

        # if self.position.y + self.radius < 0:
        #     self.position.y += SCREEN_HEIGHT + (2 * self.radius)
        # elif self.position.y - self.radius > SCREEN_HEIGHT:
        #     self.position.y -= SCREEN_HEIGHT + (2 * self.radius)

        self.current_rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.original_scaled_image, self.current_rotation)
        self.rect = self.image.get_rect(center=self.position)

    def split(self):
        self.kill()
        if self.radius / 2 < ASTEROID_MIN_RADIUS:
            return 
        else:
            split_asteroid_angle = random.uniform(20, 50)
            new_velocity_first = self.velocity.rotate(split_asteroid_angle)
            new_velocity_second = self.velocity.rotate(-split_asteroid_angle)
            new_asteroid_radius = self.radius / 2
            smaller_asteroid_1 = Asteroid(self.position.x, self.position.y, new_asteroid_radius, self.original_image_source)
            smaller_asteroid_2 = Asteroid(self.position.x, self.position.y, new_asteroid_radius, self.original_image_source)
            smaller_asteroid_1.velocity = new_velocity_first * 1.2
            smaller_asteroid_2.velocity = new_velocity_second* 1.2

            

