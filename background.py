import pygame
from constantes import *
from auxiliar import Auxiliar


class Background:
    def __init__(self ,width, height,  path):

        self.path = path
        self.height = height
        self.width = width
        self.image = pygame.image.load(path).convert()
        # self.image = pygame.transform.scale(self.image,(width,height))
        self.tiles = []
        self.pos = []



    def get_background(self):
        _,_, width, height = self.image.get_rect()
        self.tiles = []

        for i in range(ANCHO_VENTANA // width + 1):
            for j in range(ALTO_VENTANA // height + 1):
                pos= [i * width, j * height]
                self.tiles.append(pos)
        return self.tiles,self.image


    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, color=(0, 0, 0), rect=self.collition_rect)
        
        self.tiles, self.image = self.get_background()  # Llama al método get_background() para obtener los valores
        
        for pos in self.tiles:
            screen.blit(self.image, pos)
