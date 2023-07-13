import pygame
import sys
from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from auxiliar import Auxiliar
from gui_label import Label
from gui_widget import Widget


class FormMenuPrincipal(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,imagen_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,imagen_background,color_border,active)

        self.music_path = r"effect_sound\\menu.mp3"
        self.music = True
        Auxiliar.generar_musica(self.music_path,0.1)

        self.text1 = Widget(master=self,x=ANCHO_VENTANA//2-200,y=100,w=400,h=100,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Pixel_Border\Elements\Element21s.png",text="PIXEL ADVENTURE",font="IMPACT",font_size=40,font_color="Black")
        self.boton1 = Button(master=self,x=ANCHO_VENTANA//2-100,y=260,w=200,h=50,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Pixel_Border\Elements\Element21s.png",on_click=self.on_click_boton3,on_click_param="form_game_L1",text="JUGAR",font="IMPACT",font_size=30,font_color="Black")
        self.boton2 = Button(master=self,x=ANCHO_VENTANA//2-100,y=320,w=200,h=50,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Pixel_Border\Elements\Element21s.png",on_click=self.on_click_boton3,on_click_param="opciones",text="OPCIONES",font="IMPACT",font_size=30,font_color="Black")
        self.boton4 = Button(master=self,x=ANCHO_VENTANA//2-100,y=380,w=200,h=50,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Pixel_Border\Elements\Element21s.png",on_click=self.on_click_boton2,on_click_param=None,text="SALIR",font="IMPACT",font_size=30,font_color="Black")

        self.lista_widget = [self.text1,self.boton1,self.boton2,self.boton4]

    def on_click_boton1(self, parametro):
        self.pb1.value += 1
 
    def on_click_boton2(self, parametro):
        pygame.quit()
        sys.exit()
    
    def on_click_boton3(self, parametro):
        self.set_active(parametro)

    def update(self, lista_eventos,keys,delta_ms,event):
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)
        
    def draw(self): 
        super().draw()
        
        for aux_widget in self.lista_widget:    
            aux_widget.draw()