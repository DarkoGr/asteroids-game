import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot
import random



def main():
    pygame.init()

    FPS_clock = pygame.time.Clock()
    dt = 0

    screen_tuple = (SCREEN_WIDTH, SCREEN_HEIGHT) 
    screen = pygame.display.set_mode(screen_tuple)
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    windows_username = "X1extreme" 
    image_filename = "pozadina.png"

    background_image_path = f"/mnt/c/Users/{windows_username}/Desktop/{image_filename}"

    asteroid_image_paths = [
        f"/mnt/c/Users/{windows_username}/Desktop/asteroid1.png",
        f"/mnt/c/Users/{windows_username}/Desktop/asteroid2.png",
        f"/mnt/c/Users/{windows_username}/Desktop/asteroid3.png",
    ]
    
    loaded_asteroid_images = []

    for path in asteroid_image_paths:
        try:
            # Učitaj sliku. .convert_alpha() je bitno za PNG slike sa transparentnom pozadinom.
            image = pygame.image.load(path).convert_alpha()
            loaded_asteroid_images.append(image)
            print(f"✅ Slika asteroida učitana: {path}")
        except pygame.error as e:
            # Ako dođe do greške (npr. slika ne postoji), ispiši poruku i nastavi dalje.
            print(f"❌ GREŠKA pri učitavanju slike asteroida '{path}': {e}. Nastavljam bez nje.")
            
    # Važna provera: Ako nijedna slika nije uspela da se učita, dodaj bar jednu podrazumevanu.
    # Ovo sprečava pad programa ako slike nedostaju.
    if not loaded_asteroid_images:
        print("⚠️ Upozorenje: Nijedna slika asteroida nije učitana! Korišćenje podrazumevanog sivog kruga.")
        # Kreiranje podrazumevane Pygame Surface (površine) koja izgleda kao sivi krug.
        default_image = pygame.Surface((50, 50), pygame.SRCALPHA) # SRCALPHA za transparentnost
        pygame.draw.circle(default_image, (150, 150, 150), (25, 25), 25) # Crtanje sivog kruga
        loaded_asteroid_images.append(default_image)

    Asteroid.all_asteroid_images = loaded_asteroid_images

    
    background_image = pygame.image.load(background_image_path).convert()

    try:
        background_image = pygame.image.load(background_image_path).convert()
        background_image = pygame.transform.scale(background_image, screen_tuple)
        print(f"Pozadina učitana: {background_image_path}") 
    except pygame.error as e:
        print(f"GREŠKA pri učitavanju pozadine '{image_filename}': {e}. Korišćenje crne pozadine.")
        background_image = None 
    
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
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, (0, 255, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)

         #Počinje na -offset, proteže se do SCREEN_WIDTH + offset
        debug_rect_outer = pygame.Rect(
            -ASTEROID_EDGE_SPAWN_OFFSET, 
            -ASTEROID_EDGE_SPAWN_OFFSET, 
            SCREEN_WIDTH + 2 * ASTEROID_EDGE_SPAWN_OFFSET, 
            SCREEN_HEIGHT + 2 * ASTEROID_EDGE_SPAWN_OFFSET
        )
        pygame.draw.rect(screen, (255, 165, 0), debug_rect_outer, 1)
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = FPS_clock.tick(60) / 1000

        updatable.update(dt)

        for asteroid in asteroids:
            if player.collision(asteroid) and not player.is_invincible:
                player.is_invincible = True
                player.invincible_timer = INVINCIBILITY_DURATION
                player.lives -= 1
                asteroid.kill()
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
                player.velocity = pygame.Vector2(0, 0)
                player.rotation = 180

                if player.lives == 0:
                    print("Game over!")
                    pygame.quit()
                    sys.exit()
            
        #asteroid & bullet collision

        shot_to_remove = []
        asteroid_to_remove = []

        for asteroid in asteroids:
            for shot in shooting:
                if shot.collision(asteroid):
                    shot_to_remove.append(shot)
                    asteroid_to_remove.append(asteroid)
                    break

        for sh in shot_to_remove:
            sh.kill()     

        for ast in asteroid_to_remove:
            ast.split()

            

        


if __name__ == "__main__":
    main()