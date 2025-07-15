import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot



def main():
    pygame.init()

    FPS_clock = pygame.time.Clock()
    dt = 0


    screen_tuple = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screen_tuple) 
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    x = SCREEN_WIDTH/2
    y = SCREEN_HEIGHT/2
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroids_field = pygame.sprite.Group()
    shooting = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(x, y)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_spawner = AsteroidField()
    Shot.containers = (shooting, updatable, drawable)

    

    while True:
        screen.fill((0,0,0))
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = FPS_clock.tick(60) / 1000

            


        updatable.update(dt)

        for asteroid in asteroids:
            if player.collision(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()

        


if __name__ == "__main__":
    main()