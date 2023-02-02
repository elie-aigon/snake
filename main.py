import pygame, sys, random, json
from pygame.math import Vector2
from operator import itemgetter

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
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

        self.crunch_sound = pygame.mixer.Sound('crunch.wav')

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
            block_rect = pygame.Rect(block.x * CELL_SIZE,block.y * CELL_SIZE,CELL_SIZE,CELL_SIZE)
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)
    def reset(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(1,0)

    def snake_move(self):
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
        
class BUTTON:
    def __init__(self, pos_x, pos_y, width, height, text, background):
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.text = text
        self.image = background
        self.text_button = font.render(self.text, True, grey)
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.background = pygame.image.load(background).convert_alpha()

    def draw_buttons(self):
        screen.blit(self.background, self.button_rect)
        screen.blit(self.text_button, (self.x + (self.width // 2) - (self.text_button.get_width() // 2), self.y + (self.height // 2) - (self.text_button.get_height() // 2) - 3))
    
    def is_clicked(self, pos):
        return self.button_rect.collidepoint(pos)

class FRUIT:
    def __init__(self, food):
        self.random_fruit()
        self.food = pygame.image.load(food)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(self.food, fruit_rect)

    def random_fruit(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class SCOREBOARD:
    def __init__(self):
        self.x = 800
        self.y = 0
        self.background_scoreboard = pygame.image.load("Images/scorebaord_box.png")
        self.sorted_scores_dic_str = []
        with open('scores.json', 'r') as f:
            self.scores_dic = json.load(f)
        self.sort_scores()

    def sort_scores(self):
        self.sorted_scores_dic = dict(sorted(self.scores_dic.items(), key=itemgetter(1), reverse=True))
        rank = 1
        for key, value in self.sorted_scores_dic.items():
            element = " ".join((str(rank), ':', str(key), ':', str(value)))
            self.sorted_scores_dic_str.append(element)
            rank += 1

    def draw_scoreboard(self):
        scoreboard_rect = pygame.Rect(self.x, self.y, 200, 800)
        screen.blit(self.background_scoreboard, scoreboard_rect)

        scoreboard_title_rect = pygame.Rect(self.x + 85, self.y + 22, 303, 100)
        self.scoreboard_title = font.render("Leaderboard",True, grey)
        screen.blit(self.scoreboard_title, scoreboard_title_rect)
        
        scoreboard_value_x = 835
        scoreboard_value_y = 60
        
        for element in self.sorted_scores_dic_str:
            scoreboard_score_rect = pygame.Rect(scoreboard_value_x, scoreboard_value_y, 303, 400)
            self.socreboard_names = font.render(element, True, green_font)
            screen.blit(self.socreboard_names, scoreboard_score_rect)
            scoreboard_value_y += 25
    def update_score(self, name, score):
        if name in self.scores_dic:
            print(":", name, ":")
            self.scores_dic[name] += score
        else:
            self.scores_dic[name] = score
        with open('scores.json', 'w') as f:
            json.dump(self.scores_dic, f)
        self.sorted_scores_dic_str = []
        self.sort_scores()

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT('Images/apple.png')
        self.scoreboard = SCOREBOARD()
        self.button_restart = BUTTON( 805, 700, 144, 52, "Restart", "Images/orange_button.png")
        self.button_quit = BUTTON( 955, 700, 144, 52, "QUIT", "Images/red_button.png")
        self.name_input = []
        self.player_name = str()
        self.is_name = False
        self.name_not_empty = False
    def loop(self):
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
    def game_end(self):
        self.is_name = False
        if self.name_not_empty:
            self.scoreboard.update_score(self.player_name, int(self.score))
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
font = pygame.font.Font("edosz.ttf", 20)
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE + 303 , CELL_NUMBER * CELL_SIZE))

main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

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