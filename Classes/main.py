import pygame, sys, random, json
from pygame.math import Vector2
from operator import itemgetter

from BUTTON import BUTTON
from FRUIT import FRUIT
from SNAKE import SNAKE
from SCOREBOARD import SCOREBOARD

class MAIN:
    def __init__(self):
        self.snake = SNAKE(screen, CELL_SIZE, CELL_NUMBER)
        self.fruit = FRUIT(screen, 'Images/apple.png', CELL_SIZE, CELL_NUMBER)
        self.scoreboard = SCOREBOARD(screen,font, grey, green_font)
        self.button_restart = BUTTON(screen, font, grey, 805, 700, 144, 52, "Restart", "Images/orange_button.png")
        self.button_quit = BUTTON(screen, font, grey, 955, 700, 144, 52, "QUIT", "Images/red_button.png")
        self.name_input = []
        self.player_name = str()
        self.is_name = False
        self.name_not_empty = False
        self.play_ia = False


    def loop(self):
        if self.play_ia:
            self.snake.snake_move_ia()
        else:
            self.snake.snake_move()
        self.check_contacts()
    
    def draw_components(self):
        self.draw_grass()
        self.button_restart.draw_buttons()
        self.button_quit.draw_buttons()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.scoreboard.draw_scoreboard()
        self.draw_score()
        
    def check_contacts(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.random_fruit()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_end()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.random_fruit()
            if block == self.snake.body[0]:
                self.game_end()
        if int(self.score) == 397:
            self.game_end()
    def draw_grass(self):
        for row in range(CELL_NUMBER):
            if row % 2 == 0: 
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE,row * CELL_SIZE,CELL_SIZE,CELL_SIZE)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE,row * CELL_SIZE,CELL_SIZE,CELL_SIZE)
                        pygame.draw.rect(screen,grass_color,grass_rect)			

    def game_start(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in range (96, 123):
                self.name_input.append(chr(event.key))
                self.name_not_empty = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.player_name = "".join(self.name_input)
                self.is_name = True
                if self.player_name == "ia":
                    self.play_ia = True
                    self.snake.direction = Vector2(1, 0)
 
                else:
                    self.snake.direction = Vector2(1, 0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
            
    def game_end(self):
        self.is_name = False
        if self.name_not_empty:
            self.scoreboard.update_score(self.player_name, int(self.score))
        self.name_not_empty = False
        self.snake.reset()
        self.name_input = []
        self.game_start()

    def draw_score(self):
        
        name_aff = font.render("".join(self.name_input), True, grey)
        name_aff_rect = pygame.Rect(925, 500, 50, 50)
        screen.blit(name_aff, name_aff_rect)
        if self.is_name:
            self.score = str(len(self.snake.body) - 3)
            score_aff = font.render(self.score, True, grey)
            score_aff_rect = pygame.Rect(945, 550, 50, 50)
            screen.blit(score_aff, score_aff_rect)
        
pygame.init()
# Dimensions
CELL_NUMBER = 20
CELL_SIZE = 40
# Colors
grey = (34,45,46)
grass_color = (167,209,61)
green_font = (0,186,90)
green_bg = (175, 215, 70)
# Font
font = pygame.font.Font("Font/edosz.ttf", 20)
# Size
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE + 303 , CELL_NUMBER * CELL_SIZE))

main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 1)

run = True
while run:
    if not main.is_name:
        main.game_start()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main.loop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main.snake.direction.y != 1:
                        main.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if main.snake.direction.y != -1:
                        main.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main.snake.direction.x != 1:
                        main.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if main.snake.direction.x != -1:
                        main.snake.direction = Vector2(1, 0)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if main.button_quit.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if main.button_restart.is_clicked(mouse_pos):
                    main.snake.reset()
    screen.fill(green_bg)
    main.draw_components()
    pygame.display.update()