from circleshape import CircleShape
from constants import *
import pygame
from shot import Shot



class Player(CircleShape):
    def __init__(self, x, y, image):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.last_shot_time = 0.0
        self.lives = PLAYER_LIVES
        self.is_invincible = False
        self.invincible_timer = INVINCIBILITY_DURATION

        self.image = image
        self.original_image = None
        if self.image:
            
            self.original_image = pygame.transform.scale(self.image, (PLAYER_RADIUS * 3, PLAYER_RADIUS * 3))
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(center=self.position)
        else:
            
            self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]    
    
    def draw(self, screen):
        should_draw = True
        if self.is_invincible:
            # Crta se u svakom drugom frejmu
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                should_draw = False

        if should_draw:
            if self.image:
                screen.blit(self.image, self.rect)
            else:
                pygame.draw.polygon(screen, "white", self.triangle(), 2)


    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks() / 1000.0 
            if current_time - self.last_shot_time > PLAYER_SHOT_COOLDOWN:
                self.shoot()
                self.last_shot_time = current_time
        
        if self.position.x < self.radius:
            self.position.x = self.radius

        if self.position.x > SCREEN_WIDTH - self.radius:
            self.position.x = SCREEN_WIDTH - self.radius

        if self.position.y < self.radius:
            self.position.y = self.radius

        if self.position.y > SCREEN_HEIGHT - self.radius:
            self.position.y = SCREEN_HEIGHT - self.radius

        if self.image:
            self.image = pygame.transform.rotate(self.original_image, - self.rotation)
            self.rect = self.image.get_rect(center=self.position)
        
        # invincibility and timer
        if self.is_invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.is_invincible = False
                self.invincible_timer = INVINCIBILITY_DURATION 
    

        


    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position -= forward * PLAYER_SPEED * dt

    def shoot(self):
        
        Shot(self.position.x, self.position.y, SHOT_RADIUS, self.rotation)
    
