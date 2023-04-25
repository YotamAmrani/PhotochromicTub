import time
import pygame
import math
import numpy as np
from pygame.locals import *


CLEAN_MSG = "                                               " \
            "                                                   "
PRINTING_MSG ="מדפיס כעת..."
INSTRUCTIONS_MSG = "השתמש בלחצנים להזזת המנורה"

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
BG_COLOR = (137, 207, 240)
RECT_COLOR = np.add(np.array(BG_COLOR),np.array((30,30,15)))
RECT_OFFSET = 40
FONT_COLOR = (0,0,0)
green = (0, 255, 0)
blue = (0, 0, 128)
last_msg = "היי מה שלומכם?"


def set_bg_color(color):
    screen.fill(color)
    pygame.display.flip()


def set_font(text_to_display, font_file_path = "C:\Windows\Fonts\Assistant-Bold.ttf"):
    font = pygame.font.Font(font_file_path, 48)
    text = font.render(text_to_display[::-1], True, FONT_COLOR, RECT_COLOR)
    textRect = text.get_rect()
    textRect.center = (screen.get_width() // 2, screen.get_height() // 3)
    return text, textRect


def draw_frame_rectangle(color, offset,stroke_width=0, corner_size=10):
    pygame.draw.rect(screen, color, pygame.Rect(offset, offset, screen.get_width()-(offset*2), screen.get_height()-(offset*2)),  stroke_width, corner_size)


def clean_text():
    set_display_text(CLEAN_MSG)
    screen.blit(text, text_rect)


def set_display_text(text_msg):
    global text
    global text_rect
    global last_msg
    last_msg = text_msg
    text, text_rect = set_font(text_msg)


text, text_rect = set_font(last_msg)
set_bg_color(BG_COLOR)
draw_frame_rectangle( RECT_COLOR , RECT_OFFSET ,0, 10 )
circle_color = 'black'
circle_size = 10
start_time = RECT_OFFSET + 10

while quit:
    keys = pygame.key.get_pressed()
    screen.blit(text, text_rect)

    if keys[K_a]:
        clean_text()
        set_display_text(PRINTING_MSG)

    if keys[K_b]:
        clean_text()
        set_display_text(INSTRUCTIONS_MSG)

    if start_time == RECT_OFFSET + 10:
        start_time = pygame.time.get_ticks()
    t = ((pygame.time.get_ticks() - start_time)/5) % screen.get_width()
    x = t
    y = math.sin(t/50)*50 + screen.get_height() - screen.get_height()/3

    if t >= (RECT_OFFSET + 10) and t < screen.get_width() - (RECT_OFFSET+10):
        pygame.draw.circle(screen, circle_color, (x,y), circle_size)
    elif t >= screen.get_width() - RECT_OFFSET + 10:
        # draw_frame_rectangle(RECT_COLOR, 40, 0, 10)
        # set_display_text(last_msg)
        start_time = RECT_OFFSET + 10
        if circle_color == 'black':
            circle_color = RECT_COLOR
            circle_size = 11
        else:
            circle_color = 'black'
            circle_size = 10


    # Exit
    if keys[K_q]:
        quit = False



    # UPDATE for every frame
    pygame.event.pump()
    pygame.display.update()

pygame.quit()