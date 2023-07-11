import pygame
from constantes import *
from auxiliar import Auxiliar

class Fruit:
    def __init__(self, x, y, frame_rate_ms, move_rate_ms, p_scale=1):
        self.fruit = Auxiliar.getSurfaceFromSpriteSheet("images/items/Bananas.png", 17, 1, flip=True, scale=2)
        self.hit_fruit = Auxiliar.getSurfaceFromSpriteSheet("images/items/Collected.png", columnas=6, filas=1, scale=2)

        self.animacion = self.fruit
        self.rect = self.fruit[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        self.tiempo_transcurrido_animation = 0
        self.frame = 0
        self.hit_animation = False
        self.hit_animation_timer = 0
        self.hit_animation_delay = 100  # Retraso entre los fotogramas de la animación de golpe (en milisegundos)
        self.collected = False
        self.remove_fruit = False

    def check_collision(self, player_rect):
        if self.rect.colliderect(player_rect) and not self.collected:
            self.collected = True
            self.animacion = self.hit_fruit
            self.frame = 0
            self.hit_animation = True
            self.remove_fruit = True

    def stay(self, plataform_list):
        for plataforma in plataform_list:
            if self.rect.colliderect(plataforma.rect):
                self.rect.bottom = plataforma.rect.top
                break

    def do_animation(self, delta_ms):
        self.tiempo_transcurrido_animation += delta_ms

        if self.hit_animation:
            self.hit_animation_timer += delta_ms
            if self.hit_animation_timer >= self.hit_animation_delay:
                self.hit_animation = False
                self.remove_fruit = True

        if not self.hit_animation and self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            if self.frame < len(self.animacion) - 1:
                self.frame += 1
            else:
                self.frame = 0

    def update(self, delta_ms, plataform_list, player_rect):
        self.stay(plataform_list)
        self.do_animation(delta_ms)

        if self.rect.colliderect(player_rect):
            self.check_collision(player_rect)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

        if self.frame < len(self.animacion):
            self.image = self.animacion[self.frame]
        else:
            self.frame = 0
            self.image = self.animacion[self.frame]
        screen.blit(self.image, self.rect)
