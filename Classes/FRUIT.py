import pygame, sys, random, json
from pygame.math import Vector2
from operator import itemgetter

class FRUIT:
    def __init__(self, surface,food, CELL_SIZE, CELL_NUMBER):
        self.food = pygame.image.load(food)
        self.screen = surface
        self.CELL_SIZE = CELL_SIZE
        self.CELL_NUMBER = CELL_NUMBER
        self.random_fruit()
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * self.CELL_SIZE), int(self.pos.y * self.CELL_SIZE), self.CELL_SIZE, self.CELL_SIZE)
        self.screen.blit(self.food, fruit_rect)

    def random_fruit(self):
        self.x = random.randint(0, self.CELL_NUMBER - 1)
        self.y = random.randint(0, self.CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)