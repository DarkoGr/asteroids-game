import pygame
from constants import *
from player import Player

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

    player = Player(x, y)

    while True:
        screen.fill((0,0,0))
        player.draw(screen)
        pygame.display.flip()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        dt = FPS_clock.tick(60) / 1000
             

        


if __name__ == "__main__":
    main()