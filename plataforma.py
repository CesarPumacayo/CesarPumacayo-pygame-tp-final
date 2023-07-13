import pygame
from constantes import *
from auxiliar import Auxiliar


class Plataform:
    def __init__(self, x, y,width, height, image="images\\tileset\\forest\Tiles\\0.png", type=1,column=0):

        self.image_list= Auxiliar.getSurfaceFromSeparateFiles(image,1,18,flip=False,w=width,h=height)
        
        self.column = column
        self.image = self.image_list[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(self.rect)
        self.ground_collition_rect = pygame.Rect(self.rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        if self.column == 1:
            self.rect_left_side_col = pygame.Rect(self.rect.x + 10, self.rect.y+15, 10, self.rect.h-30)
            self.rect_right_side_col = pygame.Rect(self.rect.x + self.rect.w - 20, self.rect.y+15, 10, self.rect.h-30) 
            self.rect_bottom_col = pygame.Rect(self.rect.x+5, self.rect.y + self.rect.h - 12, self.rect.w-10, GROUND_RECT_H)



    def draw(self,screen):
        screen.blit(self.image,self.rect)
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        
        