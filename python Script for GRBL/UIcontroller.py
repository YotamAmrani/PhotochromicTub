import time
import pygame
import math
import numpy as np


CLEAN_MSG = "                                    " \
            "                                    "
PRINTING_MSG ="מדפיס כעת..."
INSTRUCTIONS_MSG = "השתמש בלחצנים להזזת המנורה"

BG_COLOR = (137, 207, 240)
RECT_COLOR = np.add(np.array(BG_COLOR),np.array((30,30,15)))
RECT_OFFSET = 40
FONT_COLOR = (0,0,0)
green = (0, 255, 0)
blue = (0, 0, 128)
last_msg = "היי מה שלומכם?"


class UiProperties:
    def __init__(self, screen):
        self._screen = screen
        self._bg_color = BG_COLOR
        self._bg_rect = None
        self._bg_rect_offset = RECT_OFFSET
        self._bg_rect_corner_size = 40
        self._bg_rect_color = RECT_COLOR
        self._header_msg = ""
        self._header_center = [self._screen.get_width() // 2, self._screen.get_height() // 3]
        self._instructions_msg = ""
        self._instructions_center = [self._screen.get_width() // 2, self._screen.get_height() // 3 + 60]
        self._animation_start_time = RECT_OFFSET + 10
        self._animation_circle_color = (0,0,0)
        self._animation_circle_size = 7

    def set_bg_color(self):
        self._screen.fill(self._bg_color)
        pygame.display.flip()

    def draw_frame_rectangle(self, stroke_width=0, corner_size=10):
        pygame.draw.rect(self._screen, self._bg_rect_color, pygame.Rect(self._bg_rect_offset, self._bg_rect_offset,
                                                                        self._screen.get_width() - (self._bg_rect_offset * 2),
                                                    self._screen.get_height() - (self._bg_rect_offset * 2)), stroke_width, corner_size)
        pygame.display.flip()

    def set_header(self, text_to_display, font_size=48, font_file_path="C:\Windows\Fonts\Assistant-Bold.ttf"):
        self._header_msg = text_to_display
        font = pygame.font.Font(font_file_path, font_size)
        text = font.render(text_to_display[::-1], True, FONT_COLOR, RECT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self._header_center[0], self._header_center[1])
        self._screen.blit(text, text_rect)

    def set_instruction(self, text_to_display, font_size=36, font_file_path="C:\Windows\Fonts\Assistant-Bold.ttf"):
        self._header_msg = text_to_display
        font = pygame.font.Font(font_file_path, font_size)
        text = font.render(text_to_display[::-1], True, FONT_COLOR, RECT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self._instructions_center[0], self._instructions_center[1])
        self._screen.blit(text, text_rect)

    def clean_text(self):
        self.set_header(CLEAN_MSG)
        self.set_instruction(CLEAN_MSG)

    def draw_animation(self):
        if self._animation_start_time == RECT_OFFSET + 10:
            self._animation_start_time = pygame.time.get_ticks()
        t = ((pygame.time.get_ticks() - self._animation_start_time)/5) % self._screen.get_width()
        x = t
        y = math.sin(t/50)*50 + self._screen.get_height() - self._screen.get_height()/3

        if t >= (RECT_OFFSET + 10) and t < self._screen.get_width() - (RECT_OFFSET+10):
            pygame.draw.circle(self._screen, self._animation_circle_color, (x,y), self._animation_circle_size)
        elif t >= self._screen.get_width() - RECT_OFFSET + 10:
            # draw_frame_rectangle(RECT_COLOR, 40, 0, 10)
            # set_display_text(last_msg)
            self._animation_start_time = RECT_OFFSET + 10
            if str(self._animation_circle_color) == str((0,0,0)):
                self._animation_circle_color = RECT_COLOR
                self._animation_circle_size = 8
            else:
                self._animation_circle_color = (0,0,0)
                self._animation_circle_size = 7




#
# while quit:
#     keys = pygame.key.get_pressed()
#     screen.blit(text, text_rect)
#
#     if keys[K_a]:
#         clean_text()
#         set_display_text(PRINTING_MSG)
#
#     if keys[K_b]:
#         clean_text()
#         set_display_text(INSTRUCTIONS_MSG)
#
#     if start_time == RECT_OFFSET + 10:
#         start_time = pygame.time.get_ticks()
#     t = ((pygame.time.get_ticks() - start_time)/5) % screen.get_width()
#     x = t
#     y = math.sin(t/50)*50 + screen.get_height() - screen.get_height()/3
#
#     if t >= (RECT_OFFSET + 10) and t < screen.get_width() - (RECT_OFFSET+10):
#         pygame.draw.circle(screen, circle_color, (x,y), circle_size)
#     elif t >= screen.get_width() - RECT_OFFSET + 10:
#         # draw_frame_rectangle(RECT_COLOR, 40, 0, 10)
#         # set_display_text(last_msg)
#         start_time = RECT_OFFSET + 10
#         if circle_color == 'black':
#             circle_color = RECT_COLOR
#             circle_size = 11
#         else:
#             circle_color = 'black'
#             circle_size = 10
#
#
#     # Exit
#     if keys[K_q]:
#         quit = False
#
#