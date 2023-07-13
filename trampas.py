import pygame
from constantes import *
from auxiliar import Auxiliar


class Trampa:
    def __init__(self, x, y, width, height):
        '''
        Metodo constructor proceso y distancia en la inicializacion
        -----------
        Parametros:
        self , x , y , width , heiht (ATRIBUTOS) 
        ----------
        No retorna
        '''
        self.rect = pygame.Rect(x, y, width, height)
        self.tramp_stay = pygame.image.load("images/enemy/trampa.png").convert_alpha()
        self.image = pygame.transform.scale(self.tramp_stay, (width, height))
        self.triggered = False


    def check_collision(self, player_rect):
        '''
        Chequea la colision entre el rect del jugador y la trampa
        -----------
        Parametros:
            player_rect: rectangulo del jugador
        '''
        if self.rect.colliderect(player_rect):
            return True
        return False

    def update(self, delta_ms, player_rect):
        '''
        Actualiza el estado de la trampa
        -----------------
        Parametros:
            delta_ms: tiempo_transcurrido en milisegundos
            player_rect: rectangulo del jugador 
        ------------
        Retorno:
            No retorna    
        '''
         
        if self.rect.colliderect(player_rect):
            self.triggered = True

    def draw(self, surface):
        '''
        Dibuja la trampa en una superficie.

        Parámetros:
            surface (pygame.Surface): Superficie donde se dibujará la trampa.

        No hay valor de retorno.
        '''
        surface.blit(self.image, self.rect)
