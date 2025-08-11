import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot
import random
from explosion import Explosion 


EXPLOSION_ANIMATION_FRAMES = []

def main():
    pygame.init()
    
    font = pygame.font.Font(None, 36)
    FPS_clock = pygame.time.Clock()
    dt = 0
    score = 0
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
            
            image = pygame.image.load(path).convert_alpha()
            loaded_asteroid_images.append(image)
            print(f"Slika asteroida učitana: {path}")

        except pygame.error as e:
            print(f"GREŠKA pri učitavanju slike asteroida '{path}': {e}. Nastavljam bez nje.")
            
    
    if not loaded_asteroid_images:
        print("Upozorenje: Nijedna slika asteroida nije učitana! Korišćenje podrazumevanog sivog kruga.")
        
        default_image = pygame.Surface((50, 50), pygame.SRCALPHA) 
        pygame.draw.circle(default_image, (150, 150, 150), (25, 25), 25) 
        loaded_asteroid_images.append(default_image)

    Asteroid.all_asteroid_images = loaded_asteroid_images

    explosion_spritesheet_path = f"/mnt/c/Users/{windows_username}/Desktop/image_0de47a_padded_231x231.png"

    FRAME_WIDTH = 240 
    FRAME_HEIGHT = 258

    temp_loaded_explosion_images = []

    num_cols = 0 
    num_rows = 0

    try:
        
        spritesheet = pygame.image.load(explosion_spritesheet_path).convert_alpha()
        print(f"✅ Sprite sheet eksplozije učitan: {explosion_spritesheet_path}")

        
        num_cols = spritesheet.get_width() // FRAME_WIDTH
        num_rows = spritesheet.get_height() // FRAME_HEIGHT

        if num_cols > 0 and num_rows > 0:
            
            for row in range(num_rows):
                for col in range(num_cols):
                    x_offset = col * FRAME_WIDTH
                    y_offset = row * FRAME_HEIGHT
                    
                    frame_surface = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
                    frame_surface.blit(spritesheet, (0, 0), (x_offset, y_offset, FRAME_WIDTH, FRAME_HEIGHT))
                    
                    temp_loaded_explosion_images.append(frame_surface)
        else:
            
            print(f"DEBUG ERROR: Nema frejmova za sečenje! Proverite FRAME_WIDTH/HEIGHT ({FRAME_WIDTH}x{FRAME_HEIGHT}) i dimenzije sprite sheet-a ({spritesheet.get_width()}x{spritesheet.get_height()}).")
            
            default_explosion_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(default_explosion_image, (255, 100, 0), (25, 25), 25)
            temp_loaded_explosion_images.append(default_explosion_image)
                
    except pygame.error as e:
        print(f"GREŠKA pri učitavanju ili sečenju sprite sheet-a '{explosion_spritesheet_path}': {e}. Eksplozije neće biti prikazane.")
        
        default_explosion_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(default_explosion_image, (255, 100, 0), (25, 25), 25)
        temp_loaded_explosion_images.append(default_explosion_image)

    

    global EXPLOSION_ANIMATION_FRAMES
    EXPLOSION_ANIMATION_FRAMES = temp_loaded_explosion_images

    
    print(f"DEBUG PROVERA (main): Dužina EXPLOSION_ANIMATION_FRAMES: {len(EXPLOSION_ANIMATION_FRAMES)}")
    if not EXPLOSION_ANIMATION_FRAMES:
        print("DEBUG PROVERA (main): Lista EXPLOSION_ANIMATION_FRAMES je prazna! Slike eksplozije se ne seku ispravno!")
    else:
        print(f"DEBUG PROVERA (main): Prvi frejm eksplozije ima dimenzije: {EXPLOSION_ANIMATION_FRAMES[0].get_size()}")

    
    

    try:
        background_image = pygame.image.load(background_image_path).convert()
        background_image = pygame.transform.scale(background_image, screen_tuple)
        print(f"Pozadina učitana: {background_image_path}") 
    except pygame.error as e:
        print(f"GREŠKA pri učitavanju pozadine '{image_filename}': {e}. Korišćenje crne pozadine.")
        background_image = pygame.Surface(screen_tuple) 
        background_image.fill((0,0,0))
        
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroids_field = pygame.sprite.Group()
    shooting = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    
    Shot.containers = (shooting, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)


    player = Player(x, y)
    asteroid_spawner = AsteroidField()

    

    while True:
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, (0, 255, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)

        debug_rect_outer = pygame.Rect(
            -ASTEROID_EDGE_SPAWN_OFFSET, 
            -ASTEROID_EDGE_SPAWN_OFFSET, 
            SCREEN_WIDTH + 2 * ASTEROID_EDGE_SPAWN_OFFSET, 
            SCREEN_HEIGHT + 2 * ASTEROID_EDGE_SPAWN_OFFSET
        )
        pygame.draw.rect(screen, (255, 165, 0), debug_rect_outer, 1)
        for sprite in drawable:
            sprite.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))    

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
                Explosion(player.position.x, player.position.y, player.radius * 3, EXPLOSION_ANIMATION_FRAMES)
                score += 20
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
            if ast.radius <= ASTEROID_MIN_RADIUS:
                score += 20
            else:
                score += 10

            Explosion(ast.position.x, ast.position.y, ast.radius * 2, EXPLOSION_ANIMATION_FRAMES)
            ast.split()

            

        


if __name__ == "__main__":
    main()