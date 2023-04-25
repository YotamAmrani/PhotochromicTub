import time
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

quit = True
t0 = 0
counter = 0
pressed = False


while quit:
    keys = pygame.key.get_pressed()
    # Exit
    if keys[K_q]:
        quit = False
    if keys[K_d] and not pressed:
        pressed = True
        t0 = time.time()
        counter = 0
    elif keys[K_d] and pressed:
        counter += 1
    elif not keys[K_d] and pressed:
        pressed = False
        print("time is: " + str(time.time() - t0))
        print("press count: " + str(counter))
        t0 = time.time()
        counter = 0
    # time.sleep(0.002)
    pygame.event.pump()