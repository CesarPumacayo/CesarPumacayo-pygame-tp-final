import pygame
from pygame.locals import *
import sys
from constantes import *
from gui_form import Form
from gui_form_menu_game_l1 import FormGameLevel1
from gui_form_menu_game_l2 import FormGameLevel2
from gui_form_menu_game_l3 import FormGameLevel3

from gui_menu_principal import FormMenuPrincipal
from auxiliar import *
from gui_form_lose import FormLose
from gui_form_win import FormMenuWin
from gui_form_opciones import FormOpciones
import pygame.mixer

pygame.mixer.init()


sonido1 = pygame.mixer.Sound("effect_sound\\menu.mp3")
sonido2 = pygame.mixer.Sound("effect_sound\defeat.wav")
sonido3 = pygame.mixer.Sound("effect_sound\win.mp3")
sonido4 = pygame.mixer.Sound("effect_sound\\final.mp3")
sonido5 = pygame.mixer.Sound("effect_sound\cutie_pie.mp3")



# Crear la lista de sonidos
sonidos = [sonido1, sonido2, sonido3,sonido4, sonido5]

flags = DOUBLEBUF 
screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA), flags, 16)
music_path = r"effect_sound\\menu.mp3"

pygame.init()
pygame.mixer.init()

evento_1000ms = pygame.USEREVENT
pygame.time.set_timer(evento_1000ms, 1000)

clock = pygame.time.Clock()


config_json = Auxiliar.leer_archivo("levels.json")

form_menu_principal = FormMenuPrincipal(name="menu_principal", x=0, y=0, master_surface= screen, w=ANCHO_VENTANA, h=ALTO_VENTANA, color_background="Black", imagen_background="images\\menu_jungle.png", color_border="Black",active=True)
form_opciones = FormOpciones(name="opciones",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background="Black",imagen_background = "images\\menu_jungle.png" ,color_border="Black",active=True)

form_game_L1 = FormGameLevel1(name="form_game_L1", master_surface=screen, x=0, y=0, w=ANCHO_VENTANA, h=ALTO_VENTANA, color_background=(0,255,255), imagen_background="images\menu_jungle.png", color_border=(255,0,255), active=True, config_json=config_json)
form_game_L2 = FormGameLevel2(name="form_game_L2", master_surface=screen, x=0, y=0, w=ANCHO_VENTANA, h=ALTO_VENTANA, color_background=(0,255,255), imagen_background="images\menu_jungle.png", color_border=(255,0,255), active=True, config_json=config_json, nevel1=form_game_L1)
form_game_L3 = FormGameLevel3(name="form_game_L3", master_surface=screen, x=0, y=0, w=ANCHO_VENTANA, h=ALTO_VENTANA, color_background=(0,255,255), imagen_background="images\menu_jungle.png", color_border=(255,0,255), active=True, config_json=config_json, nevel12=form_game_L2)

form_gui_lose = FormLose(name="form_game_lose",master_surface = screen,x=500,y=200,w=300,h=230,imagen_background="images\gui\jungle\\rating\\bg.png",color_background="Black",color_border="Black",active=False)
for_gui_win = FormMenuWin(name="form_win",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=C_BLACK,color_border=(255,0,255),active=False,nevel3=form_game_L3)

while True:     
    lista_eventos = pygame.event.get()
    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)

    aux_form_active = Form.get_active()

    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    if aux_form_active is not None:
        try:
            aux_form_active.update(lista_eventos,keys,delta_ms,event,evento_1000ms)
        except:
            aux_form_active.update(lista_eventos,keys,delta_ms,sonidos)
        aux_form_active.draw()

    pygame.display.flip()

