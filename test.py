import pygame

class Boutton:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 24)
        self.surface = self.font.render(self.text, True, (255, 255, 255))
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(self.surface, (self.x + (self.width // 2) - (self.surface.get_width() // 2), self.y + (self.height // 2) - (self.surface.get_height() // 2)))
    
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)

boutton = Boutton(100, 100, 100, 50, "Cliquez ici")

pygame.init()
fenetre = pygame.display.set_mode((400, 300))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if boutton.est_clique(event.pos):
                print("Boutton cliqué")
    
    fenetre.fill((0, 0, 0))
    boutton.draw(fenetre)
    pygame.display.update()

pygame.quit()
