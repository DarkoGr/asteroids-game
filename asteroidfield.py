import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):

    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_EDGE_SPAWN_OFFSET, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_EDGE_SPAWN_OFFSET, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_EDGE_SPAWN_OFFSET),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_EDGE_SPAWN_OFFSET
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius, velocity)
        

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            initial_velocity = edge[0] * speed
            initial_velocity = initial_velocity.rotate(random.randint(-30, 30))
            
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            radius_for_debug = ASTEROID_MIN_RADIUS * kind
            #print(f"DEBUG: Spawning Asteroid at X={position.x:.2f}, Y={position.y:.2f} with radius={ASTEROID_MIN_RADIUS * random.randint(1, ASTEROID_KINDS)}")
            
            self.spawn(radius_for_debug, position, initial_velocity)