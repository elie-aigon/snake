import pygame, sys, random, json
from pygame.math import Vector2
from operator import itemgetter

class BUTTON:
    def __init__(self, surface,font , color,pos_x, pos_y, width, height, text, background):
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.text = text
        self.image = background
        self.font = font
        self.color = color
        self.screen = surface
        self.text_button = self.font.render(self.text, True, self.color)
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.background = pygame.image.load(background).convert_alpha()

    def draw_buttons(self):
        self.screen.blit(self.background, self.button_rect)
        self.screen.blit(self.text_button, (self.x + (self.width // 2) - (self.text_button.get_width() // 2), self.y + (self.height // 2) - (self.text_button.get_height() // 2) - 3))
    
    def is_clicked(self, pos):
        return self.button_rect.collidepoint(pos)