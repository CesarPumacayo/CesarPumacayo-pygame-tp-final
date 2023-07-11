import pygame
from constantes import *
from auxiliar import Auxiliar


class Trampa:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.tramp_stay = pygame.image.load("images/enemy/trampa.png").convert_alpha()
        self.image = pygame.transform.scale(self.tramp_stay, (width, height))
        self.triggered = False


    def check_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            return True
        return False

    def update(self, delta_ms, player_rect):
        if self.rect.colliderect(player_rect):
            self.triggered = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)
