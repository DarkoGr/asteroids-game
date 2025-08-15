import pygame
import random
from constants import *
pygame.init()
pygame.mixer.pre_init(48000, -16, 2, 16384)
pygame.mixer.init()
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot
from explosion import Explosion 

background_music_path = f"/mnt/c/Users/X1extreme/Desktop/game_music1.mp3"

try:
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.set_volume(0.2)
    print("Muzika u pozadini učitana.")
except pygame.error as e:
    print(f"Greška pri učitavanju muzike: {e}")

pygame.mixer.music.play(-1)

explosion_sound_path = f"/mnt/c/Users/X1extreme/Desktop/explosion.mp3"

try:
    explosion_sound = pygame.mixer.Sound(explosion_sound_path)
    explosion_sound.set_volume(1.0)
    print("Zvuk eksplozije učitan.")
except pygame.error as e:
    print(f"Greška pri učitavanju zvuka eksplozije: {e}")

EXPLOSION_ANIMATION_FRAMES = []
HEART_IMAGE = None
SCORES_FILE = f"/mnt/c/Users/X1extreme/Desktop/scores.txt"


def load_high_scores():
    high_scores = []
    try:
        with open(SCORES_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    high_scores.append((parts[0], int(parts[1])))
    except FileNotFoundError:
        print("SCORES_FILE not found")
    return high_scores

def save_high_scores(scores):
    with open(SCORES_FILE, 'w') as file:
        for name, score in scores:
            file.write(f"{name} {score}\n")

def handle_game_over(screen, score):
    high_scores = load_high_scores()
    
    is_high_score = False
    if len(high_scores) < 3 or score > high_scores[-1][1]:
        is_high_score = True
        
    running = True
    input_text = ""
    font = pygame.font.Font(None, 48)
    
    cursor_visible = True
    cursor_blink_rate = 500 
    last_cursor_toggle_time = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if is_high_score:
                    if event.key == pygame.K_RETURN:
                        high_scores.append((input_text, score))
                        high_scores.sort(key=lambda x: x[1], reverse=True)
                        save_high_scores(high_scores[:3])
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                else:
                    # Y/N logic
                    if event.key == pygame.K_y:
                        running = False  # restarts game
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit() 
        
        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_toggle_time > cursor_blink_rate:
            cursor_visible = not cursor_visible
            last_cursor_toggle_time = current_time

        screen.fill((0, 0, 0))
        
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        
        scores_title = font.render("TOP 3 SCORES", True, (255, 255, 0))
        screen.blit(scores_title, scores_title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50)))
        
        sorted_scores = sorted(high_scores, key=lambda x: x[1], reverse=True)
        for i, (name, s) in enumerate(sorted_scores[:3]):
            score_line = font.render(f"{i+1}. {name}: {s}", True, (255, 255, 255))
            screen.blit(score_line, score_line.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100 + i * 50)))
            
        if is_high_score:
            prompt_text = font.render("New High Score! Enter your name:", True, (255, 255, 255))
            input_surface = font.render(input_text, True, (255, 255, 255))
            input_rect = input_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))
            
            screen.blit(prompt_text, prompt_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 100)))
            screen.blit(input_surface, input_rect)
            
            if cursor_visible:
                cursor_rect = pygame.Rect(input_rect.right + 5, input_rect.top, 3, input_rect.height)
                pygame.draw.rect(screen, (255, 255, 255), cursor_rect)
        else:
            continue_text = font.render("Continue? (Y/N)", True, (150, 150, 150))
            screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50)))

        author_font = pygame.font.Font(None, 30)
        author_text = author_font.render("Made by:  Darko Grubić", True, (150, 150, 150))
        author_rect = author_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        screen.blit(author_text, author_rect)
        
        pygame.display.flip()


def main():
    pygame.init()
    
    font = pygame.font.Font(None, 36)
    FPS_clock = pygame.time.Clock()
    dt = 0
    score = 0
    screen_tuple = (SCREEN_WIDTH, SCREEN_HEIGHT) 
    screen = pygame.display.set_mode(screen_tuple)
    pygame.display.set_caption("Asteroids")
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    windows_username = "X1extreme" 
    image_filename = "pozadina.png"
    player1_image = "ship5.png"
    heart_image = "hearts1.png"
    intro_end_time = pygame.time.get_ticks() + 5000

    background_image_path = f"/mnt/c/Users/{windows_username}/Desktop/{image_filename}"
    player1_image_path = f"/mnt/c/Users/{windows_username}/Desktop/{player1_image}"

    

    asteroid_image_paths = [
        f"/mnt/c/Users/{windows_username}/Desktop/asteroid1.png",
        f"/mnt/c/Users/{windows_username}/Desktop/asteroid2.png",
        f"/mnt/c/Users/{windows_username}/Desktop/asteroid3.png",
    ]
    
    loaded_asteroid_images = []

    hearts_path = f"/mnt/c/Users/{windows_username}/Desktop/{heart_image}"
    HEART_SIZE = (40, 40)

    try:
        single_heart = pygame.image.load(hearts_path).convert_alpha()
        global HEART_IMAGE
        HEART_IMAGE = pygame.transform.scale(single_heart, HEART_SIZE)
        print(f"Heart image loaded and scaled to:{HEART_SIZE}.")
    except pygame.error as e:
        print(f"Error: Heart image '{hearts_path}': {e}.")
                                     
    
    
    

    for path in asteroid_image_paths:
        try:
            
            image = pygame.image.load(path).convert_alpha()
            loaded_asteroid_images.append(image)
            print(f"Asteroid image loaded: {path}")

        except pygame.error as e:
            print(f"Error asteroid image'{path}': {e}.")
            
    
    if not loaded_asteroid_images:
        print("Using circles instead of asteroids")
        
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
            
            print("No frames to cut")
            
            default_explosion_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(default_explosion_image, (255, 100, 0), (25, 25), 25)
            temp_loaded_explosion_images.append(default_explosion_image)
                
    except pygame.error as e:
        print("No explosions")
        
        default_explosion_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(default_explosion_image, (255, 100, 0), (25, 25), 25)
        temp_loaded_explosion_images.append(default_explosion_image)

    

    global EXPLOSION_ANIMATION_FRAMES
    EXPLOSION_ANIMATION_FRAMES = temp_loaded_explosion_images

    


    try:
        player1_image = pygame.image.load(player1_image_path).convert_alpha()
        print(f"Slika igrača učitana: {player1_image_path}")
    except pygame.error as e:
        print(f"Error: Player image missing'{player1_image_path}': {e}.")
        player1_image = None
    

    try:
        background_image = pygame.image.load(background_image_path).convert()
        background_image = pygame.transform.scale(background_image, screen_tuple)
        print(f"Background loaded: {background_image_path}") 
    except pygame.error as e:
        print(f"Error: background loading '{image_filename}': {e}.")
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


    player = Player(x, y, player1_image)
    asteroid_spawner = AsteroidField()
    
    start_time = pygame.time.get_ticks()

    
    

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

        score_text = font.render(f"Score: {score}", True, (150, 200, 250))
        screen.blit(score_text, (10, 10))    
        
        if HEART_IMAGE:
            HEARTS_RIGHT_MARGIN = 40
            HEART_SPACING = 7
            for i in range(player.lives):
                heart_x = SCREEN_WIDTH - HEARTS_RIGHT_MARGIN - (i + 1) * (HEART_SIZE[0] + HEART_SPACING)
                heart_y = 10

                screen.blit(HEART_IMAGE, (heart_x, heart_y))
            if pygame.time.get_ticks() < intro_end_time:
                intro_text = font.render("Made by:   DarkoGrr", True, (150, 200, 250))
                text_rect = intro_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))
                screen.blit(intro_text, text_rect)

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
                Explosion(player.position.x, player.position.y, player.radius * 3, EXPLOSION_ANIMATION_FRAMES, explosion_sound)
                score += 20
                asteroid.kill()
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
                player.velocity = pygame.Vector2(0, 0)
                player.rotation = 180

                if player.lives == 0:
                    handle_game_over(screen, score)
                    # Resetujemo igru za sledeću rundu
                    player.lives = 3
                    score = 0
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
                    player.velocity = pygame.Vector2(0, 0)
                    player.rotation = 180
                    # Uklanjamo sve asteroide i metke da bi igra bila čista
                    asteroids.empty()
                    shooting.empty()
            
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

            Explosion(ast.position.x, ast.position.y, ast.radius * 2, EXPLOSION_ANIMATION_FRAMES, explosion_sound)
            ast.split()

            

        


if __name__ == "__main__":
    main()