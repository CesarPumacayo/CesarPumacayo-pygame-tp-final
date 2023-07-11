import pygame
from constantes import *
from auxiliar import Auxiliar

class Enemy():
    def __init__(self, x, y, speed_walk, speed_run, gravity, jump_power, frame_rate_ms, move_rate_ms, jump_height, p_scale=1, interval_time_jump=100):
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("images/enemy/Flying.png", 9, 1, flip=True, scale=2)
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet("images/enemy/Flying.png", 9, 1, flip=False, scale=2)
        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet("images/enemy/Flying.png", 9, 1, flip=True, scale=2)
        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet("images/enemy/Flying.png", 9, 1, flip=False, scale=2)
        self.hit_l = Auxiliar.getSurfaceFromSpriteSheet("images/enemy/Hit.png", 5, 1, flip=False, scale=2)
        self.hit_r = Auxiliar.getSurfaceFromSpriteSheet("images/enemy/Hit.png", 5, 1, flip=True, scale=2)



        self.contador = 0
        self.frame = 0
        self.lives = 1
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_l
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x + self.rect.width/3, y, self.rect.width/3, self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        # HIT 
        self.is_hit = False  # Nuevo atributo
        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.frame_counter = 0

        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0  # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump

        self.hit_l_frame_rate_ms = 200  # Valor más alto para ralentizar la animación de golpe
        self.default_frame_rate_ms = frame_rate_ms  # Almacenar el frame_rate_ms original

        self.is_removed = False

    def change_x(self, delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def check_collision(self, player_rect):
        if self.rect.colliderect(player_rect) and player_rect.bottom < self.rect.centery:
            return True
        return False

    def handle_collision(self, player_rect):
        if not self.is_hit and self.check_collision(player_rect):
            self.animation = self.hit_l
            self.frame = 0
            self.is_hit = True
            self.frame_rate_ms = self.hit_l_frame_rate_ms  # Establecer el nuevo frame_rate_ms

    def do_animation(self, delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                self.frame = 0
                self.frame_rate_ms = self.default_frame_rate_ms  # Restaurar el frame_rate_ms predeterminado para otras animaciones

    def do_movement(self, delta_ms, plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0

            if not self.is_on_plataform(plataform_list):
                if self.move_y == 0:
                    self.is_fall = True
                self.change_y(self.gravity)
            else:
                self.is_fall = False
                self.change_x(self.move_x)
                if self.contador <= 50:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l
                    self.contador += 1 
                elif self.contador <= 100:
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                    self.contador += 1
                else:
                    self.contador = 0

    def is_on_plataform(self, plataforma_list):
        retorno = False
        
        if self.ground_collition_rect.bottom >= GROUND_LEVEL:
            retorno = True     
        else:
            for plataforma in plataforma_list:
                if self.ground_collition_rect.colliderect(plataforma.ground_collition_rect):
                    retorno = True
                    break       
        return retorno

    def update(self, delta_ms, plataforma_list, player_rect):
        self.handle_collision(player_rect)
        
        if self.is_hit:
            self.rect.y += 1.5
            if self.rect.y > ALTO_VENTANA:
                self.remove()
        else:
            self.do_movement(delta_ms, plataforma_list)
            self.do_animation(delta_ms)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

        if self.frame < len(self.animation):
            self.image = self.animation[self.frame]
        else:
            # Manejar el caso en el que self.frame está fuera del rango válido
            # Por ejemplo, puedes restablecer self.frame a 0 o realizar alguna otra acción adecuada.
            self.frame = 0
            self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)

    def receive_shoot(self):
        self.lives -= 1

    def remove(self):
        # Realizar acciones para eliminar o desactivar el objeto Enemy
        # Por ejemplo, podrías establecer una bandera para indicar que el objeto debe eliminarse en la próxima actualización del juego.
        self.is_removed = True


class Enemy_distance:
    def __init__(self, x, y, gravity, frame_rate_ms, move_rate_ms, p_scale=1):
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("images/enemy/trunk/idle/{0}.png", 0, 17, flip=True, scale=2)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/enemy/trunk/idle/{0}.png", 0, 17, flip=False, scale=2)
        self.hit_r = Auxiliar.getSurfaceFromSeparateFiles("images/enemy/trunk/hit/{0}.png", 0, 4, flip=True, scale=2)
        self.hit_l = Auxiliar.getSurfaceFromSeparateFiles("images/enemy/trunk/hit/{0}.png", 0, 4, flip=False, scale=2)

        self.contador = 0
        self.frame = 0
        self.lives = 1
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.gravity = gravity
        self.animation = self.stay_l
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x + self.rect.width/3, y, self.rect.width/3, self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        # HIT 
        self.is_hit = False
        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.frame_counter = 0

        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0

        self.hit_l_frame_rate_ms = 200
        self.default_frame_rate_ms = frame_rate_ms

        self.is_removed = False

    def check_collision(self, player_rect):
        if self.rect.colliderect(player_rect) and player_rect.bottom < self.rect.centery:
            return True
        return False
    
    def is_on_plataform(self, plataforma_list):
        retorno = False
        
        if self.ground_collition_rect.bottom >= GROUND_LEVEL:
            retorno = True     
        else:
            for plataforma in plataforma_list:
                if self.ground_collition_rect.colliderect(plataforma.ground_collition_rect):
                    retorno = True
                    break       
        return retorno     
    
    def handle_collision(self, player_rect):
        if not self.is_hit and self.check_collision(player_rect):
            self.animation = self.hit_l
            self.frame = 0
            self.is_hit = True
            self.frame_rate_ms = self.hit_l_frame_rate_ms
    
    def apply_gravity(self, plataforma_list):
        if not self.is_on_plataform(plataforma_list):
            self.move_y += self.gravity
        else:
            self.move_y = 0
    
    def do_animation(self, delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1
            else:
                self.frame = 0
                self.frame_rate_ms = self.default_frame_rate_ms
    
    def update(self, delta_ms, plataforma_list, player_rect):
        self.handle_collision(player_rect)
        
        if self.is_hit:
            self.rect.y += 1.5
            if self.rect.y > ALTO_VENTANA:
                self.remove()
        else:
            self.apply_gravity(plataforma_list)
            self.do_animation(delta_ms)
            self.rect.y += self.move_y
    
    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
    
        if self.frame < len(self.animation):
            self.image = self.animation[self.frame]
        else:
            self.frame = 0
            self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
    
    def receive_shoot(self):
        self.lives -= 1
    
    def remove(self):
        self.is_removed = True
