import pygame, sys, random, json
from pygame.math import Vector2
from operator import itemgetter

class SCOREBOARD:
    def __init__(self, surface, font, color_title, color_element):
        self.screen = surface
        self.font = font
        self.color_title = color_title
        self.color_element = color_element
        self.x = 800
        self.y = 0
        self.background_scoreboard = pygame.image.load("Images/scorebaord_box.png")
        self.sorted_scores_dic_str = []
        with open('Data/scores.json', 'r') as f:
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
        self.screen.blit(self.background_scoreboard, scoreboard_rect)

        scoreboard_title_rect = pygame.Rect(self.x + 85, self.y + 22, 303, 100)
        self.scoreboard_title = self.font.render("Leaderboard",True,self.color_title)
        self.screen.blit(self.scoreboard_title, scoreboard_title_rect)
        
        scoreboard_value_x = 835
        scoreboard_value_y = 60
        
        for element in self.sorted_scores_dic_str:
            scoreboard_score_rect = pygame.Rect(scoreboard_value_x, scoreboard_value_y, 303, 400)
            self.socreboard_names = self.font.render(element, True, self.color_element)
            self.screen.blit(self.socreboard_names, scoreboard_score_rect)
            scoreboard_value_y += 25
    def update_score(self, name, score):
        if name in self.scores_dic:
            self.scores_dic[name] += score
        else:
            self.scores_dic[name] = score
        with open('Data/scores.json', 'w') as f:
            json.dump(self.scores_dic, f)
        self.sorted_scores_dic_str = []
        self.sort_scores()
