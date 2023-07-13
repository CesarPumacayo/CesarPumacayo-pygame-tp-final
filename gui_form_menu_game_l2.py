import pygame
from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from player import Player
from enemigo import Enemy
from botin import Fruit
from plataforma import Plataform
from background import Background
from bullet import Bullet
from trampas import Trampa
from gui_label import Label
from auxiliar import *
from enemigo import Enemy_distance
from gui_widget import Widget

class FormGameLevel2(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background, imagen_background, color_border,active,config_json, nevel1):
        super().__init__(name,master_surface,x,y,w,h,color_background, imagen_background, color_border,active)
        self.levels = config_json
        self.player_1 = self.generate_player()
        self.music_path = r"effect_sound\\nevel2.wav"
        self.music_menu = r"effect_sound\\menu.mp3"
        self.tiempo_inicial = pygame.time.get_ticks()
        self.music = True
        self.cronometro = 60
        # self.lvl_anterior = lvl1
        self.score_total = 0
        self.pausado = False
        self.font = pygame.font.SysFont("IMPACTO",50)
        self.acumuladorNiveles = nevel1
  
        # --- GUI WIDGET ---

        self.text_lvl = Widget(master=self,x=5,y=25,w=200,h=50,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Data_Border\Buttons\Button_XL_01.png",text="NIVEL 2",font='opensans.ttf',font_size=40,font_color=C_WHITE)
        
        self.button_menu = Button(master=self,x=750,y=0,w=140,h=50,color_background=None,color_border=None,image_background="images\gui\jungle\match3\\table_2.png",on_click=self.on_click_boton_menu,on_click_param="menu_principal",text="MENU",font="Verdana",font_size=30,font_color=C_WHITE)
         
        self.text_score = Label(master=self,x=1200,y=30,w=200,h=50,color_background=None,color_border=None,image_background=None,
                                  text=f'SCORE: {str(self.player_1.score)}',font='Arial',font_size=30,font_color=C_WHITE)
        
        self.text_time = Label(master=self,x=1350,y=750,w=200,h=50,color_background=None,color_border=None,image_background=None,
                                  text=f': {str(self.cronometro)}',font='Arial',font_size=30,font_color=C_WHITE)
        
        self.reloj = Label(master=self,x=1350,y=750,w=50,h=50,color_background=None,color_border=None,image_background="images\gui\jungle\\bubble\clock.png",
                                  text='',font='Arial',font_size=30,font_color=C_WHITE)
        
        self.pb_lives = ProgressBar(master=self,x=1000,y=50,w=150,h=30,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Data_Border/Bars/Bar_Background01.png",image_progress="images/gui/set_gui_01/Data_Border/Bars/Bar_Segment05.png",value = self.player_1.lives, value_max=5)
                
        self.widget_list = [self.text_lvl,self.button_menu,self.text_score,self.text_time,self.reloj ,self.pb_lives]

        # --- GAME ELEMENTS ---
        self.static_background = Background(x=0,y=0,width=w,height=h,path="images\jungle.png")

        self.enemies_list_melee = []
        self.generate_enemies()

        self.enemies_list_distance = []
        self.generate_enemies_distance()
        
        self.platform_list = []
        self.generate_platform()

        self.fruit_list = []
        self.generate_fruit()

        self.tramp_list = []
        self.generate_trampas()

        self.timer_3s = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_3s, 3000)  # Cada 3 segundos dispara

        self.bullet_list = []

    def on_click_boton_menu(self, parametro):
        self.reiniciar_nivel()
        self.reproducir_musica(self.music_menu)
        self.music = True
        self.set_active("menu_principal") 

    def on_click_boton1(self, parametro):
        self.set_active(parametro)


    def shot_enemy(self):
        pygame.time.set_timer(self.timer_3s, 3000) 
        for enemy_element in self.enemies_list_distance:
            self.bullet_list.append(Bullet(
                enemy_element, enemy_element.rect.centerx, enemy_element.rect.centery,
                self.player_1.rect.centerx, self.player_1.rect.centery, 5,
                path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png", frame_rate_ms=100, move_rate_ms=20,
                width=5, height=5
            ))

    def reiniciar_nivel(self):

        self.cronometro = 60
        self.music = True
        self.player_1 = self.generate_player()
        self.platform_list = []
        self.enemies_list_melee = []
        self.enemies_list_distance= []
        self.fruit_list = []
        self.generate_enemies_distance()
        self.generate_enemies()
        self.generate_platform()
        self.generate_fruit()
        
    def generate_player(self):
        data_player = self.levels[1]["player"]
        player = Player(x=data_player["x"],y=data_player["y"],speed_walk=data_player["speed_walk"],speed_run=data_player["speed_run"],
                        gravity=data_player["gravity"],jump_power=data_player["jump_power"],frame_rate_ms=data_player["frame_rate_ms"],
                        move_rate_ms=data_player["move_rate_ms"],jump_height=data_player["jump_height"],
                        p_scale=data_player["p_scale"],interval_time_jump=data_player["interval_time_jump"])
        return player

    def generate_enemies(self):
        data_enemies = self.levels[1]["enemies"]
        for enemy in data_enemies:
            self.enemies_list_melee.append(Enemy(x=enemy["x"],y=enemy["y"],speed_walk=enemy["speed_walk"],gravity=enemy["gravity"],frame_rate_ms=enemy["frame_rate_ms"],
                            move_rate_ms=enemy["move_rate_ms"],p_scale=enemy["p_scale"],interval_time_jump=enemy["interval_time_jump"]))
        
    def generate_enemies_distance(self):
        data_enemies = self.levels[1]["enemies_distance"]
        for enemy in data_enemies:
            self.enemies_list_distance.append(Enemy_distance(x=enemy["x"],y=enemy["y"],gravity=enemy["gravity"],frame_rate_ms=enemy["frame_rate_ms"],
                            move_rate_ms=enemy["move_rate_ms"],p_scale=enemy["p_scale"]))

    def generate_platform(self):
        data_platforms = self.levels[1]["platforms"]
        for platform in data_platforms:
            self.platform_list.append(Plataform(x=platform["x"],y=platform["y"],height=platform["height"],width=platform["width"],
                            image=platform["image"],column=platform["column"]))
            
            
    def generate_fruit(self):
        data_fruit = self.levels[1]["fruit"]
        for fruit in data_fruit:
            self.fruit_list.append(Fruit(x=fruit["x"], y=fruit["y"], frame_rate_ms=fruit["frame_rate_ms"], move_rate_ms=fruit["move_rate_ms"]))



    def generate_trampas(self):
        data_trampa = self.levels[1]["trampa"]
        for trampa in data_trampa:
            self.tramp_list.append(Trampa(x= trampa["x"], y= trampa["y"], width= trampa["width"], height= trampa["height"]))




    def reproducir_musica(self,music_path):
        if self.music:
            Auxiliar.generar_musica(music_path,0.1)
            self.music = False


    def descontar_tiempo(self,lista_eventos,evento_1000ms):
        for event in lista_eventos:
            if event.type == evento_1000ms:
                self.cronometro -= 1  

                
    def check_collision(self):

        for bullet in self.player_1.bullet_list:
            for enemy in self.enemies_list_distance:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.remove()  # Marcar el enemigo como eliminado
                    self.player_1.score += 50  # Aumentar la puntuación del jugador

        for enemy in self.enemies_list_distance:
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

                
        for enemy in self.enemies_list_melee:
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

        self.fruit_list = [fruit for fruit in self.fruit_list if not fruit.remove_fruit]

        for trampas in self.tramp_list:
            if self.player_1.rect.colliderect(trampas.rect) and self.player_1.rect.top < trampas.rect.top:
                if not self.player_1.immune:
                    self.player_1.lives -= 1
                    self.player_1.immune = True


    def descontar_tiempo(self,lista_eventos,evento_1000ms):
        for event in lista_eventos:
            if event.type == evento_1000ms:
                self.cronometro -= 1  

    def update(self, lista_eventos, keys, delta_ms, event, evento_1000ms):
        for evento in lista_eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    self.pausado = not self.pausado

        if self.pausado:
            pausa_texto = self.font.render("PAUSA", True, (255, 255, 255))
            self.surface.blit(pausa_texto, (self.w/2 - pausa_texto.get_width()/2, self.h/2 - pausa_texto.get_height()/2))
            return
        
        else:
            if self.music:
                Auxiliar.generar_musica(self.music_path,0.1)
            self.music = False



        if self.player_1.score >= 450:
            self.score_total = self.player_1.score
            print(self.score_total)
            self.reiniciar_nivel()
            self.set_active("form_game_L3")
                
        if self.player_1.lives < 1 or self.cronometro < 1:
            self.score_total = 0
            self.reiniciar_nivel()
            self.reproducir_musica(self.music_menu)
            self.set_active("form_game_lose")

        for aux_widget in self.widget_list:
            aux_widget.update(lista_eventos)

        for bullet_element in self.bullet_list:
            bullet_element.update(delta_ms, self.platform_list, self.enemies_list_melee, self.player_1)

        for bullet_element in self.player_1.bullet_list:
            bullet_element.update(delta_ms, self.platform_list, self.enemies_list_melee or self.enemies_list_distance,
                                  self.player_1)

        for fruit in self.fruit_list:
            fruit.update(delta_ms, self.platform_list, self.player_1.rect)
              

        for enemy_element in self.enemies_list_melee:
            enemy_element.do_animation(delta_ms)
            enemy_element.update(delta_ms, self.platform_list, self.player_1.rect)


        for enemy_element2 in self.enemies_list_distance:
            enemy_element2.do_animation(delta_ms)
            enemy_element2.update(delta_ms, self.platform_list, self.player_1.rect)

        for evento in lista_eventos:
            if evento.type == self.timer_3s:
                self.shot_enemy()


        for trampas in self.tramp_list:
            trampas.update(delta_ms, self.player_1.rect)

        # self.player_1.update(delta_ms, self.platform_list)

        # self.player_1.events(delta_ms, keys)


        self.enemies_list_distance = [enemy for enemy in self.enemies_list_distance if not enemy.is_removed]


        self.descontar_tiempo(lista_eventos,evento_1000ms)

        self.score_total = self.player_1.score
        
        self.text_score._text = f'SCORE: {str(self.player_1.score)}'
        self.text_time._text = f': {str(self.cronometro)}'
        self.player_1.events(delta_ms, keys)
        self.player_1.update(delta_ms, self.platform_list)

        self.pb_lives.value = self.player_1.lives

        self.check_collision()

    def draw(self):
        super().draw()
        self.static_background.draw(self.surface)

        for aux_widget in self.widget_list:
            aux_widget.draw()

        for plataforma in self.platform_list:
            plataforma.draw(self.surface)

        for enemy_element in self.enemies_list_melee:
            enemy_element.draw(self.surface)

        for trampas in self.tramp_list:
            trampas.draw(self.surface)
        self.player_1.draw(self.surface)
        
        for fruit_element in self.fruit_list:
            fruit_element.draw(self.surface)

            
        for enemy_element2 in self.enemies_list_distance:
            enemy_element2.draw(self.surface)

        for bullet_element in self.bullet_list:
            bullet_element.draw(self.surface)

        for bullet_element in self.player_1.bullet_list:
            bullet_element.draw(self.surface)


