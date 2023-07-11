import pygame
from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from player import Player
from enemigo import Enemy, Enemy_distance
from botin import Fruit
from plataforma import Plataform
from background import Background
from bullet import Bullet
from trampas import Trampa



from modo import *


class FormGameLevel1(Form):
    def __init__(self, name, master_surface, x, y, w, h, color_background, color_border, active):
        super().__init__(name, master_surface, x, y, w, h, color_background, color_border, active)
        # --- GUI WIDGET ---
        self.boton1 = Button(
            master=self, x=0, y=0, w=140, h=50, color_background=None, color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
            on_click=self.on_click_boton1, on_click_param="form_menu_B", text="BACK", font="Verdana", font_size=30,
            font_color=C_WHITE
        )
        self.boton2 = Button(
            master=self, x=200, y=0, w=140, h=50, color_background=None, color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
            on_click=self.on_click_boton1, on_click_param="form_menu_B", text="PAUSE", font="Verdana", font_size=30,
            font_color=C_WHITE
        )

        # --- GAME ELEMENTS ---
        self.pb_lives = ProgressBar(
            master=self, x=500, y=50, w=240, h=50, color_background=None, color_border=None,
            image_background="images/gui/set_gui_01/Comic_Border/Bars/Bar_Background01.png",
            image_progress="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png", value=5, value_max=5
        )
        #                    ▼ back          ▼ pausa       ▼ vidas
        self.widget_list = [self.boton1, self.boton2, self.pb_lives]

        self.static_background = Background(width=w, height=h, path="images/Background/Yellow.png")

        self.player_1 = Player(
            x=0, y=200, speed_walk=8, speed_run=20, gravity=15, jump_power=30, frame_rate_ms=50,
            move_rate_ms=50, jump_height=140, p_scale=0.2, interval_time_jump=300
        )

        self.trampa_list = Trampa(x=1400, y=GROUND_LEVEL - 50, width=50, height=50)

        self.fruit_list = [Fruit(x=950, y=550, frame_rate_ms=100, move_rate_ms=50)]

        self.enemy_list_melee = [
            Enemy(x=450, y=200, speed_walk=6, speed_run=5, gravity=14, jump_power=30, frame_rate_ms=300,
                  move_rate_ms=50, jump_height=140, p_scale=0.08, interval_time_jump=150),
            Enemy(x=900, y=200, speed_walk=6, speed_run=5, gravity=14, jump_power=30, frame_rate_ms=300,
                  move_rate_ms=50, jump_height=140, p_scale=0.08, interval_time_jump=150)
        ]

        self.enemy_list_distance = [Enemy_distance(x=850, y=305, gravity=14, frame_rate_ms=300, move_rate_ms=50,p_scale=100)]

        self.plataform_list = [
            Plataform(x=350, y=500, width=50, height=50, type=12),
            Plataform(x=400, y=500, width=50, height=50, type=13),
            Plataform(x=450, y=500, width=50, height=50, type=13),
            Plataform(x=500, y=500, width=50, height=50, type=14),
            Plataform(x=600, y=430, width=50, height=50, type=12),
            Plataform(x=650, y=430, width=50, height=50, type=14),
            Plataform(x=750, y=360, width=50, height=50, type=12),
            Plataform(x=800, y=360, width=50, height=50, type=13),
            Plataform(x=850, y=360, width=50, height=50, type=13),
            Plataform(x=900, y=360, width=50, height=50, type=14)
        ]

        platform_width = 100
        platform_height = 100

        for x in range(0, ANCHO_VENTANA, 100):
            self.plataform_list.append(Plataform(x=x, y=GROUND_LEVEL, width=platform_width, height=platform_height, type=1))
            self.plataform_list.append(Plataform(x=x, y=GROUND_LEVEL + 100 , width=platform_width, height=platform_height, type=4))

        self.timer_3s = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_3s, 3000)  # Cada 3 segundos dispara

        self.bullet_list = []

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def shot_enemy(self):
        pygame.time.set_timer(self.timer_3s, 3000) 
        for enemy_element in self.enemy_list_distance:
            self.bullet_list.append(Bullet(
                enemy_element, enemy_element.rect.centerx, enemy_element.rect.centery,
                self.player_1.rect.centerx, self.player_1.rect.centery, 5,
                path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png", frame_rate_ms=100, move_rate_ms=20,
                width=5, height=5
            ))

    def check_collision(self):

        for enemy in self.enemy_list_distance:
            if self.player_1.rect.colliderect(enemy.rect) and self.player_1.rect.top < enemy.rect.top:
                enemy.animation = enemy.hit_l
                enemy.receive_shoot()
                if enemy not in self.player_1.collided_enemies:
                    self.player_1.score += 50
                    self.player_1.collided_enemies.append(enemy)
                print(self.player_1.score)
            elif self.player_1.rect.colliderect(enemy.rect):
                if not self.player_1.immune:
                    self.player_1.lives -= 1
                    self.player_1.immune = True

        for enemy in self.enemy_list_melee:
            if self.player_1.rect.colliderect(enemy.rect) and self.player_1.rect.top < enemy.rect.top:
                enemy.animation = enemy.hit_l
                enemy.receive_shoot()
                if enemy not in self.player_1.collided_enemies:
                    self.player_1.score += 50
                    self.player_1.collided_enemies.append(enemy)
                print(self.player_1.score)
            elif self.player_1.rect.colliderect(enemy.rect):
                if not self.player_1.immune:
                    self.player_1.lives -= 1
                    self.player_1.immune = True

        for fruit in self.fruit_list:
            if self.player_1.rect.colliderect(fruit.rect) and not fruit.collected:
                self.player_1.score += 50
                print(self.player_1.score)
                fruit.collected = True
                fruit.animacion = fruit.hit_fruit
                fruit.frame = 0
                fruit.hit_animation = True

        if self.player_1.rect.colliderect(self.trampa_list.rect) and self.player_1.rect.top < self.trampa_list.rect.top:
            if not self.player_1.immune:
                self.player_1.lives -= 1
                self.player_1.immune = True
                self.player_1.score += 50

        self.fruit_list = [fruit for fruit in self.fruit_list if not fruit.remove_fruit]



    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.widget_list:
            aux_widget.update(lista_eventos)

        for bullet_element in self.bullet_list:
            bullet_element.update(delta_ms, self.plataform_list, self.enemy_list_melee, self.player_1)

        for bullet_element in self.player_1.bullet_list:
            bullet_element.update(delta_ms, self.plataform_list, self.enemy_list_melee or self.enemy_list_distance,
                                  self.player_1)

        for fruit_element in self.fruit_list[:]:
            fruit_element.do_animation(delta_ms)
            fruit_element.update(delta_ms, self.plataform_list, self.player_1.rect)
            if fruit_element.remove_fruit:
                self.fruit_list.remove(fruit_element)

        for enemy_element in self.enemy_list_melee:
            enemy_element.do_animation(delta_ms)
            enemy_element.update(delta_ms, self.plataform_list, self.player_1.rect)


        for enemy_element in self.enemy_list_distance:
            enemy_element.do_animation(delta_ms)
            enemy_element.update(delta_ms, self.plataform_list, self.player_1.rect)

        for evento in lista_eventos:
            if evento.type == self.timer_3s:
                self.shot_enemy()

        self.trampa_list.update(delta_ms, self.player_1.rect)

        self.player_1.update(delta_ms, self.plataform_list)

        self.player_1.events(delta_ms, keys)

        self.check_collision()

        self.pb_lives.value = self.player_1.score
        self.pb_lives.value = self.player_1.lives

    def draw(self):
        super().draw()
        self.static_background.draw(self.surface)

        for aux_widget in self.widget_list:
            aux_widget.draw()

        for plataforma in self.plataform_list:
            plataforma.draw(self.surface)

        for fruit_element in self.fruit_list:
            fruit_element.draw(self.surface)

        for enemy_element in self.enemy_list_melee:
            enemy_element.draw(self.surface)

        for enemy_element2 in self.enemy_list_distance:
            enemy_element2.draw(self.surface)

        for bullet_element in self.bullet_list:
            bullet_element.draw(self.surface)

        for bullet_element in self.player_1.bullet_list:
            bullet_element.draw(self.surface)

        self.trampa_list.draw(self.surface)

        self.player_1.draw(self.surface)

        if get_modo():
            player_rect = self.player_1.rect

            player_lados = {
                "top": pygame.Rect(player_rect.left, player_rect.top, player_rect.width, 2),
                "bottom": pygame.Rect(player_rect.left, player_rect.bottom - 2, player_rect.width, 2),
                "left": pygame.Rect(player_rect.left, player_rect.top, 2, player_rect.height),
                "right": pygame.Rect(player_rect.right - 2, player_rect.top, 2, player_rect.height),
            }

            for lado_rect in player_lados.values():
                pygame.draw.rect(self.surface, "Blue", lado_rect, 2)

            for enemy in self.enemy_list_melee:
                pygame.draw.rect(self.surface, "Red", enemy.rect, 2)

            for enemy in self.enemy_list_distance:
                pygame.draw.rect(self.surface, "Red", enemy.rect, 2)

            for bullet in self.bullet_list:
                pygame.draw.rect(self.surface, "Black", bullet.rect, 2)


            for plataforma in self.plataform_list:
                pygame.draw.rect(self.surface, "Blue", plataforma.rect, 2)