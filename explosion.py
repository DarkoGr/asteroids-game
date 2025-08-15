import pygame
from constants import * 

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size, explosion_images, explosion_sound):
        super().__init__(self.containers) 

        self.position = pygame.Vector2(x, y)
        self.size = size 
        self.images = explosion_images 
        self.image_index = 0
        self.image = self.images[self.image_index]
        
        
        self.image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))
        self.rect = self.image.get_rect(center=self.position)

        self.animation_speed = 0.1 
        self.time_since_last_frame = 0.0

        explosion_sound.play()

    def update(self, dt):
        self.time_since_last_frame += dt

        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0.0
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.kill() 
            else:
                self.image = self.images[self.image_index]
                self.image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))
                self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)