import pygame, random, sys, pyautogui
from pygame.locals import *

WINDOW_WIDTH, WINDOW_HEIGHT = pyautogui.size()


TEXT_COLOR          = (0, 0, 0)

BACKGROUND_COLOR    = (255, 255, 255)

FPS                 = 60

BADDIE_MAX_SIZE     = 40
BADDIE_MIN_SIZE     = 10
BADDIE_MIN_SPPED    = 1
BADDIE_MAX_SPPED    = 8
ADD_NEW_BADDIE_RATE = 6
PLAYER_MOVE_RATE    = 5

def terminate():
    pygame.quit()
    sys.exit()

def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type   == QUIT:
                terminate()
            if event.type   == KEYDOWN:
                if event.key    == K_ESCAPE:
                    terminate()
                return

def player_has_hit_baddie(player_rect, baddies):
    for baddie in baddies:
        if player_rect.colliderect(baddie['rect']):
            return True
    return False

def draw_text(text, font, surface, x, y):
    text_obj        = font.render(text, True, TEXT_COLOR)
    text_rect       = text_obj.get_rect()
    text_rect.left  = int(x)
    text_rect.top   = int(y)
    surface.blit(text_obj, text_rect)

pygame.init()

main_clock  = pygame.time.Clock()
window_surface  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),  pygame.FULLSCREEN, 0, 32)

pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font            = pygame.font.SysFont(None, 48)

game_over_sound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

player_image    = pygame.image.load('player.png')
player_rect     = player_image.get_rect()
baddie_image    = pygame.image.load('baddie.png')

window_surface.fill(BACKGROUND_COLOR)

draw_text('Dodger', font, window_surface, WINDOW_WIDTH/3, WINDOW_HEIGHT/3)
draw_text('Press Any Key To Start', font, window_surface, (WINDOW_WIDTH/3) - 30, (WINDOW_HEIGHT/3) + 50)

pygame.display.update()


wait_for_player_to_press_key()

top_score   = 0
while True:
    baddies = []
    score   = 0
    player_rect.top = int(WINDOW_HEIGHT - 50)
    player_rect.left= int(WINDOW_WIDTH / 2)

    move_right = move_left = move_up = move_down = False

    reverse_cheat   = slow_cheat    = False

    baddie_add_counter  = 0

    pygame.mixer.music.play(-1, 0.0)

    while  True:
        score   += 1
        for event in pygame.event.get():
            if event.type   == QUIT:
                terminate()
            if event.type   == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_z:
                    reverse_cheat   = True
                if event.key == K_x:
                    slow_cheat      = True
                if event.key == K_a or event.key == K_LEFT:
                    move_left   = True
                    move_right  = False
                if event.key == K_d or event.key == K_RIGHT:
                    move_right  = True
                    move_left   = False
                if event.key == K_UP or event.key == K_w:
                    move_up     = True
                    move_down   = False
                if event.key == K_DOWN or event.key == K_s:
                    move_down   = True
                    move_up     = False
            if event.type   == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_z:
                    reverse_cheat   = False
                if event.key == K_x:
                    slow_cheat      = False
                if event.key == K_a or event.key == K_LEFT:
                    move_left   = False
                if event.key == K_d or event.key == K_RIGHT:
                    move_right  = False
                if event.key == K_UP or event.key == K_w:
                    move_up     = False
                if event.key == K_DOWN or event.key == K_s:
                    move_down   = False
            if event.type   == MOUSEMOTION:
                player_rect.centerx = event.pos[0]
                player_rect.centery = event.pos[1]

        if not reverse_cheat and not slow_cheat:
            baddie_add_counter  += 1

        if baddie_add_counter == ADD_NEW_BADDIE_RATE:
            baddie_add_counter  = 0
            baddie_size         = random.randint(BADDIE_MIN_SIZE, BADDIE_MAX_SIZE)                
            new_baddie          = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH - baddie_size), 
                                                        0 - baddie_size, 
                                                        baddie_size, baddie_size),
                                    'speed': random.randint(BADDIE_MIN_SPPED, BADDIE_MAX_SPPED),
                                    'surface': pygame.transform.scale(baddie_image, (baddie_size, baddie_size))}

            baddies.append(new_baddie)

        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if move_right and player_rect.right < WINDOW_WIDTH:
            player_rect.move_ip(PLAYER_MOVE_RATE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, PLAYER_MOVE_RATE * -1)
        if move_down and player_rect.bottom < WINDOW_HEIGHT:
            player_rect.move_ip(0, PLAYER_MOVE_RATE)
        
        for baddie in baddies:
            if not reverse_cheat and not slow_cheat:
                baddie['rect'].move_ip(0, baddie['speed'])
            elif reverse_cheat:
                baddie['rect'].move_ip(0, -5)
            elif slow_cheat:
                baddie['rect'].move_ip(0, 1)

        for baddie in baddies[:]:
            if baddie['rect'].top > WINDOW_HEIGHT:
                baddies.remove(baddie)
        
        window_surface.fill(BACKGROUND_COLOR)


        draw_text(f'Score {score}', font, window_surface, 10, 0)
        draw_text(f'Top Score {top_score}', font, window_surface, 10, 40)

        window_surface.blit(player_image, player_rect)

        for b in baddies:
            window_surface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if player_has_hit_baddie(player_rect, baddies):
            if score > top_score:
                top_score   = score
            break

        main_clock.tick(FPS)

    pygame.mixer.music.stop()
    game_over_sound.play()

    draw_text('Game Over', font, window_surface, (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3))

    draw_text('Press Any Key To Start', font, window_surface, (WINDOW_WIDTH/3) - 80, (WINDOW_HEIGHT/3) + 50)

    pygame.display.update()
    wait_for_player_to_press_key()
    game_over_sound.stop()
