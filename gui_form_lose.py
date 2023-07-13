from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_widget import Widget
from auxiliar import *

class FormLose(Form):
    """
    Formulario que aparece cuando el jugador muere o se queda sin tiempo
    """
    def __init__(self,name,master_surface,x,y,w,h,color_background,imagen_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,imagen_background,color_border,active)


        self.music_path = r"effect_sound\defeat.wav"

        self.text1 = Widget(master=self,x=25,y=60,w=250,h=50,color_background=None,color_border=None,image_background="images\gui\jungle\\bubble\\table.png",text="NIVEL PERDIDO",font="IMPACT",font_size=30,font_color="Red")
        self.boton1 = Button(master=self,x=30,y=140,w=70,h=70,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Comic\Buttons\\repeat.png",on_click=self.on_click_reset,on_click_param="form_game_L1",text=None)
        self.boton2 = Button(master=self,x=190,y=140,w=70,h=70,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Comic\Buttons\home.png",on_click=self.on_click_boton1,on_click_param="menu_principal",text=None)
        self.boton3 = Button(master=self,x=110,y=140,w=70,h=70,color_background=None,color_border=None,image_background="images\gui\set_gui_01\Comic\Buttons\info.png",on_click=self.on_click_boton1,on_click_param="opciones",text=None)
        
        self.lista_widget = [self.text1,self.boton1,self.boton2,self.boton3]

    def on_click_boton1(self, parametro):
        """
        Este metodo se encarga de obtener un parametro y pasarlo a otro metodo

        Parametro: un str que representa la clave del formulario
        """
        self.set_active(parametro)
    
    def on_click_reset(self, parametro):
        """
        Este metodo se encarga de resetear el nivel correspondiente y activar el nuevo dependiendo del parametro

        Parametro: recibe un str que representa la clave del formulario a activar
        """
        self.forms_dict[self.boton1.on_click_param].reiniciar_nivel()
        self.set_active(parametro)


    def cambiar_nivel(self,parametro):
        """
        Este metodo se encarga de cambiar el nivel del parametro donde se va a ejecutar este formulario

        Parametro: recibe un str que representa el nivel actual donde trabajara el formulario
        """
        self.boton1.on_click_param = parametro

    def update(self, lista_eventos, keys=None, delta_ms=None, event=None, evento_1000ms=None):
        """
        Este metodo se encarga de actualizar el los distintos widget

        Parametros: recibe una lista de eventos
        """
        for aux_widget in self.lista_widget:
            aux_widget.update(lista_eventos)
    
    def draw(self): 
        """
        Este metodo se encarga de dibujar los distintos widget en pantalla
        """
        super().draw()
        for aux_widget in self.lista_widget:    
            aux_widget.draw()

            