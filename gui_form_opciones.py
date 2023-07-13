import pygame
from pygame.locals import *
from gui_form import Form
from gui_textbox import TextBox
from gui_button import Button
from gui_widget import Widget
from gui_progressbar import *
from constantes import *

class FormOpciones(Form):
    """
    Formulario de opciones donde se pueda ajustar tanto el volumen como cambiarte el nombre
    """
    def __init__(self,name,master_surface,x,y,w,h,color_background,imagen_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,imagen_background,color_border,active)

        self.nombre = "PLAYER"
        self.text1 = Widget(master=self,x=ANCHO_VENTANA//2-100,y=130,w=200,h=50,color_background=None,color_border=None,image_background= "images\gui\set_gui_01\Pixel_Border\Elements\Element21s.png",text="MUSICA",font="IMPACT",font_size=30,font_color="White")
        self.text2 = Widget(master=self,x=ANCHO_VENTANA//2-100,y=280,w=200,h=50,color_background=None,color_border=None,image_background= "images\gui\set_gui_01\Pixel_Border\Elements\Element21s.png",text="EFECTOS",font="IMPACT",font_size=30,font_color="White")
        self.pb1 = ProgressBar(master=self,x=ANCHO_VENTANA//2-200,y=200,w=400,h=35,color_background=None,color_border=None,image_background= "images\gui\set_gui_01\Glitch\Buttons\Button_XL_01.png",image_progress= "images\gui\set_gui_01\Comic_Border\Buttons\Button_S_01.png",value=3,value_max=10)
        self.pb2 = ProgressBar(master=self,x=ANCHO_VENTANA//2-200,y=350,w=400,h=35,color_background=None,color_border=None,image_background= "images\gui\set_gui_01\Glitch\Buttons\Button_XL_01.png",image_progress= "images\gui\set_gui_01\Comic_Border\Buttons\Button_S_01.png",value=3,value_max=10)
        self.boton1 = Button(master=self,x=ANCHO_VENTANA//2-300,y=200,w=35,h=35,color_background=None,color_border=None,image_background= "images\gui\jungle\\btn\prew.png",on_click=self.on_click_boton2,on_click_param="menu",text=None,font=None,font_size=None,font_color=None)
        self.boton2 = Button(master=self,x=ANCHO_VENTANA//2-300,y=350,w=35,h=35,color_background=None,color_border=None,image_background= "images\gui\jungle\\btn\prew.png",on_click=self.on_click_boton3,on_click_param="menu",text=None,font=None,font_size=None,font_color=None)
        self.boton3 = Button(master=self,x=ANCHO_VENTANA//2+250,y=200,w=35,h=35,color_background=None,color_border=None,image_background= "images\gui\jungle\\btn\\next.png",on_click=self.on_click_boton4,on_click_param="menu",text=None,font=None,font_size=None,font_color=None)
        self.boton4 = Button(master=self,x=ANCHO_VENTANA//2+250,y=350,w=35,h=35,color_background=None,color_border=None,image_background= "images\gui\jungle\\btn\\next.png",on_click=self.on_click_boton5,on_click_param="menu",text=None,font=None,font_size=None,font_color=None)
        self.box = TextBox(master=self,x=ANCHO_VENTANA//2-100,y=500,w=200,h=50,color_background=None,color_border=None,image_background= "images\gui\set_gui_01\Pixel_Border\Elements\Element21s.png",on_click=None,on_click_param=None,text="Press Esc (salir)",font="IMPACT",font_size=15,font_color="Black")
        self.lista_widget = [self.text1,self.text2,self.pb1,self.pb2,self.boton1,self.boton2,self.boton3,self.boton4,self.box]

    def on_click_boton1(self, parametro):
        """
        Este metodo se encarga de obtener un parametro y pasarlo a otro metodo

        Parametro: un str que representa la clave del formulario
        """
        self.set_active(parametro)
    
    def cambiar_nombre(self,parametro):
        """
        Este metodo se encarga de cambiar el nombre actual al pasado por parametro

        Parametro: un str que representa el nuevo nombre
        """
        self.nombre = parametro

    def on_click_boton2(self, parametro):
        """
        Este metodo se encarga de decrementar el valor del progressbar
        """
        if self.pb1.value > 0:
            self.pb1.value -= 1
    
    def on_click_boton3(self, parametro):
        """
        Este metodo se encarga de decrementar el valor del progressbar
        """
        if self.pb2.value > 0:
            self.pb2.value -= 1
    
    def on_click_boton4(self, parametro):
        """
        Este metodo se encarga de incrementar el valor del progressbar
        """
        if self.pb1.value < self.pb1.value_max:
            self.pb1.value += 1
    
    def on_click_boton5(self, parametro):
        """
        Este metodo se encarga de incrementar el valor del progressbar
        """
        if self.pb2.value < self.pb2.value_max:
            self.pb2.value += 1
        
    def update(self, lista_eventos, keys, delta_ms, sonidos):
        """
        Este método se encarga de actualizar y controlar el sonido y los distintos widgets

        Parámetros:
        - lista_eventos: una lista de eventos de pygame
        - keys: el estado de las teclas
        - delta_ms: el tiempo transcurrido desde la última actualización en milisegundos
        - sonidos: una lista de sonidos que se desean ajustar
        """
        pygame.mixer.music.set_volume(self.pb1.value / 10)
        for sonido in sonidos:
            sonido.set_volume(self.pb2.value / 10)
        for aux_boton in self.lista_widget:
            aux_boton.update(lista_eventos)
        for evento in lista_eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.set_active("menu_principal")


    def draw(self): 
        """
        Este metodo se encarga de dibujar los distintos widget en pantalla
        """
        super().draw()
        for aux_boton in self.lista_widget:    
            aux_boton.draw()