import pygame
import os   # helps defining the path to the Assets folder
pygame.font.init()  # initializes fonts for pygame
pygame.mixer.init()     # initializes mixer (sound module) for pygame

# pygame coordinate system surface (display) and objects is (0, 0) at left upper corner

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER_WIDTH = 2
BORDER = pygame.Rect(WIDTH // 2 - BORDER_WIDTH // 2, 0, BORDER_WIDTH, HEIGHT)   # integer division //

FPS = 60

# spaceships common variables
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
RIGHT_ROTATE, LEFT_ROTATE = 90, 270
VEL = 5 / FPS * 60
BULLET_VEL = 7 / FPS * 60
MAGAZINE_CAP = 5
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# red spaceship variables
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), LEFT_ROTATE)

RED_HIT = pygame.USEREVENT + 1


# yellow spaceship variables
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))  # os dependent path
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), RIGHT_ROTATE)

YELLOW_HIT = pygame.USEREVENT + 2

pygame.display.set_caption("Space ship battle")
pygame.init()


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), True, WHITE)
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))   # draws a object surface center WINDOW point
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left for left spaceship
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # right for left spaceship
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up for left spaceship
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:  # down for left spaceship
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left for right spaceship
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right for right spaceship
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up for right spaceship
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:  # down for right spaceship
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))  # adds a RED_HIT event to event queue
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))   # adds a YELLOW_HIT event to event queue
            red_bullets.remove(bullet)  # TODO consider if this makes sense
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WINDOW.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2,
                            HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    pygame.event.clear()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)     # fps cap
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # quits app when X pressed
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and len(yellow_bullets) < MAGAZINE_CAP:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(                                                   # yellow bullet render
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)  # integer division //
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAGAZINE_CAP:
                    bullet = pygame.Rect(                           # red bullet render
                        red.x, red.y + red.height // 2 - 2, 10, 5)  # integer division //
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            draw_winner(winner_text)    # Someone won
            break

        keys_pressed = pygame.key.get_pressed()  # gets all pressed keys
        yellow_handle_movement(keys_pressed, yellow)    # function for movement of the yellow spaceship
        red_handle_movement(keys_pressed, red)   # function for movement of the red spaceship

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()


if __name__ == "__main__":  # prevents running main if file not run directly
    main()
