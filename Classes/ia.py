import pygame, sys, random, json
from pygame.math import Vector2
from operator import itemgetter

class SNAKE_IA:
    def __init__(self, surface, CELL_SIZE, CELL_NUMBER):
        self.CELL_SIZE = CELL_SIZE
        self.CELL_NUMBER = CELL_NUMBER

        self.screen = surface
        self.body = [Vector2(7, 0), Vector2(6, 0), Vector2(5, 0)]
        self.direction = Vector2(1, 0)

        self.new_block = False

        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Images/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sounds/crunch.wav')

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * self.CELL_SIZE,block.y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            if index == 0:
                self.screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                self.screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    self.screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        self.screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        self.screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        self.screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        self.screen.blit(self.body_br,block_rect)
    def reset(self):
        self.body = [Vector2(7,0),Vector2(6,0),Vector2(5,0)]
        self.direction = Vector2(0,0)

    def snake_move_ia(self):
        if self.body[0].x == 0 and self.body[0].y == 0:
            self.direction = Vector2(1, 0)

        if self.body[0].x == 19 and self.body[0].y == 0:
            self.direction = Vector2(0, 1)
        
        # Loop bottom
        if self.body[0].x % 2 != 0 and self.body[0].y == 1:
            self.direction = Vector2(0, 1)

        if self.body[0].x == 0 and self.body[0].y == 1:
            self.direction = Vector2(0, -1)

        elif self.body[0].x % 2 == 0 and self.body[0].y == 1:
            self.direction = Vector2(-1, 0)

        # Loop top
        if self.body[0].x % 2 != 0 and self.body[0].y == 19:
            self.direction = Vector2(-1, 0)
            
        if self.body[0].x % 2 == 0 and self.body[0].y == 19:
            self.direction = Vector2(0, -1)
        
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            
    def add_block(self):
        self.new_block = True
    
    def play_crunch_sound(self):
	    self.crunch_sound.play()