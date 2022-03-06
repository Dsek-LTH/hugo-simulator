import socket
import random
import pygame
import math
from pygame.locals import *

pygame.init()

LED_SIZE = 16
LED_MARGIN = 2
LED_BOX = LED_MARGIN * 2 + LED_SIZE

WIDTH = 95
HEIGHT = 7

LEVELS = 10

WINDOW_SIZE = (WIDTH * LED_BOX, HEIGHT * LED_BOX)

display = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Blinkmojt Simulator 2022")


def draw_led(x, y, intensity):
    intensity = math.floor(intensity / (255 / LEVELS)) / LEVELS;
    cx = (x + 0.5)*LED_BOX
    cy = (y + 0.5)*LED_BOX
    pygame.draw.circle(surface=display, center=(cx,cy), color=(128 + (255-128)*intensity if intensity > 0 else 64, 0, 0), radius=LED_SIZE/2)

def draw_frame(image):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            draw_led(x, y, image[y*WIDTH + x])

image = [round(random.random() * 256) for i in range(WIDTH*HEIGHT)]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.1)
sock.bind(("0.0.0.0", 1337))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display.fill((0,0,0))
    draw_frame(image)

    pygame.display.update()

    try:
        buf = sock.recv(WIDTH*HEIGHT)
        if len(buf) == WIDTH*HEIGHT:
            image = buf
    except socket.timeout:
        pass

