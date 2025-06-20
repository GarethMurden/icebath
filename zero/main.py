import argparse
import os
import pygame
import platform
import threading
import time
import RPi.GPIO as GPIO

import temperature

dirname, _ = os.path.split(os.path.abspath(__file__))
THIS_DIRECTORY = f'{dirname}{os.sep}'

VERSION = 'v1.5'
SCREEN_WIDTH = 1280 #800
SCREEN_HEIGHT = 720 #600

GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 14
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

FONT = None
COLOURS = None
IMAGES = None
CURRENT_TEMPERATURE = ' '
PREVIOUS_TEMPERATURE = None
RUNNING = True
UNITS = 'c'
CALIBRATION = 0.0

def set_calibration(channel):
    global CALIBRATION
    CALIBRATION += 0.5
    if CALIBRATION > 10.0:
        CALIBRATION = -10.0
    save_calibration()

def init(windowed=False, logo=False):
    global FONT, COLOURS, IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT, UNITS, CALIBRATION

    if os.path.exists(f'{THIS_DIRECTORY}calibration.txt'):
        with open(f'{THIS_DIRECTORY}calibration.txt', 'r') as f:
            try:
                CALIBRATION = float(f.read().strip())
            except:
                CALIBRATION = 0.0

    if os.path.exists(f'{THIS_DIRECTORY}fahrenheit'):
        UNITS = 'f'
    else:
        UNITS = 'c'

    sensor_thread = threading.Thread(target=get_temperature)
    sensor_thread.start()

    pygame.init()

    if windowed:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

    pygame.font.init()
    FONT = {
        'large': pygame.font.Font(f'{THIS_DIRECTORY}assets{os.sep}font.ttf', int(SCREEN_HEIGHT / 1.5)),
        'small': pygame.font.Font(f'{THIS_DIRECTORY}assets{os.sep}font.ttf', int(SCREEN_HEIGHT / 6)),
        'tiny':  pygame.font.Font(f'{THIS_DIRECTORY}assets{os.sep}font.ttf', int(SCREEN_HEIGHT / 8))
    }
    COLOURS = {
        'black':    (  0,   0,   0),
        'white':    (255, 255, 255)
    }
    if logo:
        IMAGES = {
            'logo': pygame.image.load(f'{THIS_DIRECTORY}assets/logo.png').convert(),
        }
        logo_width, logo_height = IMAGES['logo'].get_size()
        if logo_height > SCREEN_HEIGHT:
            logo_ratio = logo_height / logo_width
            new_logo_height = int(SCREEN_HEIGHT)
            new_logo_width = int(logo_ratio * new_logo_height)
            IMAGES['logo'] = pygame.transform.scale(
                IMAGES['logo'],
                (
                    new_logo_width,
                    new_logo_height
                )
            )
    return screen

def get_temperature():
    global CURRENT_TEMPERATURE
    while RUNNING:
        if platform.system() == 'Windows':
            reading_c, reading_f = temperature.simulate()
        else:
            reading_c, reading_f = temperature.read()
        if UNITS == 'c':
            reading = reading_c
        else:
            reading = reading_f
        if reading is not None:
            CURRENT_TEMPERATURE = str(round(reading + CALIBRATION, 1))
        time.sleep(5)

def show_logo(screen, alpha):
    image_width, image_height = IMAGES['logo'].get_size()
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.blit(
        IMAGES['logo'],
        (
            int(round((SCREEN_WIDTH / 2) - (image_width / 2), 0)),
            int(round((SCREEN_HEIGHT / 2) - (image_height / 2), 0))
        )
    )
    surface = pygame.transform.flip(surface, True, True)
    screen.blit(surface, (0,0))
    mask = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )
    mask.fill(
        (
            COLOURS['black'][0],
            COLOURS['black'][1],
            COLOURS['black'][2],
            alpha
        )
    )
    screen.blit(
        mask,
        (0, 0)
    )
    return alpha

def show_temp(screen):
    global PREVIOUS_TEMPERATURE
    if PREVIOUS_TEMPERATURE != CURRENT_TEMPERATURE:
        PREVIOUS_TEMPERATURE = CURRENT_TEMPERATURE
        if CURRENT_TEMPERATURE != ' ':
            try:
                temperature_int = float(CURRENT_TEMPERATURE)
                surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.fill(COLOURS['black'])

                text_width, text_height = FONT['large'].size(CURRENT_TEMPERATURE)
                coordinates = (
                    int(round((SCREEN_WIDTH / 2) - (text_width / 2), 0)),
                    int(round((SCREEN_HEIGHT / 2) - (text_height / 2), 0))
                )
                surface.blit(
                    FONT['large'].render(
                        CURRENT_TEMPERATURE,
                        True,
                        COLOURS['white']
                    ),
                    coordinates
                )
                text = "o"
                symbol_coordinates = (
                    int(coordinates[0] + text_width),
                    int(coordinates[1] + (text_height / 2))
                )
                surface.blit(
                    FONT['tiny'].render(
                        text,
                        True,
                        COLOURS['white']
                    ),
                    symbol_coordinates
                )
                text = UNITS.upper()
                c_width, c_height = FONT['small'].size(text)
                surface.blit(
                    FONT['small'].render(
                        text,
                        True,
                        COLOURS['white']
                    ),
                    (
                        int(symbol_coordinates[0] + c_width / 1.5),
                        int(symbol_coordinates[1] + c_height / 4)
                    )
                )
                # surface = pygame.transform.flip(surface, True, False)
                surface = pygame.transform.flip(surface, False, True)
                screen.blit(surface, (0, 0))
            except Exception as e:
                print(e)
                raise
    return screen

def save_calibration():
    with open(f'{THIS_DIRECTORY}calibration.txt', 'w') as f:
        f.write(str(CALIBRATION))

def main(windowed=False, logo=False):
    global RUNNING, CALIBRATION
    screen = init(windowed, logo)
    pygame.display.set_caption(f'Odin Projector | {VERSION}')
    clock = pygame.time.Clock()

    alpha = 0
    if logo:
        mode = 'logo'
    else:
        mode = 'temp'

    while RUNNING:
        if mode == 'logo':
            screen.fill(COLOURS['black'])
            alpha = show_logo(screen, alpha)
            if alpha < 255:
                alpha = min(alpha + 1, 255)
                if alpha > 50:
                    alpha = min(alpha + 50, 255)
            else:
                mode = 'temp'
        if mode == 'temp':
            screen = show_temp(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                RUNNING = False

        pygame.display.flip()
        clock.tick(25)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--window', action='store_true')
    parser.add_argument('-l', '--show_logo', action='store_true')
    args = parser.parse_args()

    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=set_calibration, bouncetime=400)

    try:
        main(windowed=args.window, logo=args.show_logo)
    except KeyboardInterrupt:
        RUNNING = False
