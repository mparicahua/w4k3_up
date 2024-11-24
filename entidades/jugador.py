import pygame
from constantes import WIDTH, HEIGHT
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animaciones = {"corriendo": {"frames":[],"frameIndex":0,"numeroFrames":6,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"","bucle":True,"seleccionado":False},
                            "parado": {"frames":[],"frameIndex":0,"numeroFrames":17,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"","bucle":True,"seleccionado":False},
                            "saltando": {"frames":[],"frameIndex":0,"numeroFrames":5,"cooldownAnimacion":200,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"","bucle":True,"seleccionado":False},
                            "dasheando": {"frames":[],"frameIndex":0,"numeroFrames":15,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"D","bucle":True,"seleccionado":False},
                            "muriendo": {"frames":[],"frameIndex":0,"numeroFrames":19,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"","bucle":False,"seleccionado":False}
                            }
        self.cargar_animacion()
        self.imagen = self.animaciones["saltando"]["frames"][self.animaciones["saltando"]["frameIndex"]]
        self.animaciones["saltando"]["seleccionado"] = True
        self.saltando = False
        self.rect = self.imagen.get_rect()
        self.rect.x = 575
        self.rect.y = 600
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.mirando_derecha = True
        self.cantidad_almas = 0
        self.doble_salto_disponible = True
        self.doble_salto_habilitado = True 
        self.seguimiento_camara_y = True 
        self.seguimiento_camara_x = True 
        self.estoy_vivo = True
        #Pruebas dash
        self.dash_habilitado = True
        self.dash_disponible = True
        self.dash_cooldown = 0
        self.dash_duracion = 0
        self.dash_velocidad = 15
        ##########################
        self.pausado = False
    def cargar_animacion(self):
        for nombre_animacion in self.animaciones.keys():
            for i in range(self.animaciones[nombre_animacion]["numeroFrames"]):
                img = pygame.image.load(f"assets/imagenes/personajes/soul/{nombre_animacion}/frame{i}.png")
                if  self.animaciones[nombre_animacion]["tipo"] =="D":
                    rect = pygame.Rect(45, 44, 105, 66)
                    sprite_recortado = img.subsurface(rect)
                    self.animaciones[nombre_animacion]["frames"].append(sprite_recortado)
                else:
                    rect = pygame.Rect(53, 44, 45, 66)
                    sprite_recortado = img.subsurface(rect)
                    self.animaciones[nombre_animacion]["frames"].append(sprite_recortado)
    def activar_doble_salto(self):
        self.doble_salto_habilitado = not self.doble_salto_habilitado
    def activar_dash(self):
        self.dash_habilitado = not self.dash_habilitado
    def activar_seguimeinto_camara_y(self):
        self.seguimiento_camara_y = not self.seguimiento_camara_y
    def activar_seguimeinto_camara_x(self):
        self.seguimiento_camara_x = not self.seguimiento_camara_x
    def activar_muerte_jugador(self):
        self.estoy_vivo = False

    def update(self):
        #Animaciones
        if self.estoy_vivo:
            if self.saltando:
                self.imagen = self.animaciones["saltando"]["frames"][self.animaciones["saltando"]["frameIndex"]]
                self.animaciones["saltando"]["seleccionado"] = True
                self.animaciones["corriendo"]["seleccionado"] = False
                self.animaciones["parado"]["seleccionado"] = False
                self.animaciones["dasheando"]["seleccionado"] = False
                self.animaciones["muriendo"]["seleccionado"] = False
            else:
                if  self.velocidad_x != 0:
                    self.imagen = self.animaciones["corriendo"]["frames"][self.animaciones["corriendo"]["frameIndex"]]
                    self.animaciones["saltando"]["seleccionado"] = False
                    self.animaciones["corriendo"]["seleccionado"] = True
                    self.animaciones["parado"]["seleccionado"] = False
                    self.animaciones["dasheando"]["seleccionado"] = False
                    self.animaciones["muriendo"]["seleccionado"] = False
                else :
                    self.imagen = self.animaciones["parado"]["frames"][self.animaciones["parado"]["frameIndex"]]
                    self.animaciones["saltando"]["seleccionado"] = False
                    self.animaciones["corriendo"]["seleccionado"] = False
                    self.animaciones["parado"]["seleccionado"] = True
                    self.animaciones["dasheando"]["seleccionado"] = False
                    self.animaciones["muriendo"]["seleccionado"] = False
            if self.dash_disponible == False:
                self.imagen = self.animaciones["dasheando"]["frames"][self.animaciones["saltando"]["frameIndex"]]
                self.animaciones["saltando"]["seleccionado"] = False
                self.animaciones["corriendo"]["seleccionado"] = False
                self.animaciones["parado"]["seleccionado"] = False
                self.animaciones["dasheando"]["seleccionado"] = True
                self.animaciones["muriendo"]["seleccionado"] = False
        else:
            self.imagen = self.animaciones["muriendo"]["frames"][self.animaciones["muriendo"]["frameIndex"]]
            self.animaciones["saltando"]["seleccionado"] = False
            self.animaciones["corriendo"]["seleccionado"] = False
            self.animaciones["parado"]["seleccionado"] = False
            self.animaciones["dasheando"]["seleccionado"] = False
            self.animaciones["muriendo"]["seleccionado"] = True
            
        for nombre_animacion in self.animaciones.keys():
            if self.animaciones[nombre_animacion]["seleccionado"]:
                if pygame.time.get_ticks() - self.animaciones[nombre_animacion]["actualizado_fecha"] >= self.animaciones[nombre_animacion]["cooldownAnimacion"]:
                    if self.animaciones[nombre_animacion]["bucle"] :
                        self.animaciones[nombre_animacion]["frameIndex"] += 1
                    elif self.animaciones[nombre_animacion]["frameIndex"] + 1 != len(self.animaciones[nombre_animacion]["frames"]):
                        self.animaciones[nombre_animacion]["frameIndex"] += 1
                    self.animaciones[nombre_animacion]["actualizado_fecha"] = pygame.time.get_ticks()
                if self.animaciones[nombre_animacion]["frameIndex"] >= len(self.animaciones[nombre_animacion]["frames"]):
                        self.animaciones[nombre_animacion]["frameIndex"]  = 0 
            else:
                
                self.animaciones[nombre_animacion]["frameIndex"] = 0  
        
        ###################################################################################################################################################
        if not self.pausado:
            if self.dash_duracion > 0:
                self.dash_duracion -= 1
                if self.dash_duracion <= 0:
                    self.velocidad_x = 0
            if self.dash_cooldown > 0:
                self.dash_cooldown -= 1
                if self.dash_cooldown <= 0:
                    self.dash_disponible = True
            self.velocidad_y += 0.5 
            if self.velocidad_y > 10: 
                self.velocidad_y = 10

    def saltar(self):
        if self.estoy_vivo and not self.pausado:
            if self.saltando == False:
                self.velocidad_y = -10
                self.saltando = True
            elif self.doble_salto_habilitado and self.doble_salto_disponible:
                self.velocidad_y = -10
                self.doble_salto_disponible = False
    def ejecutar_dash(self):
        if self.dash_habilitado and self.dash_disponible and self.estoy_vivo and not self.pausado:
            self.dash_duracion = 10
            self.dash_disponible = False
            self.dash_cooldown = 30
            if self.mirando_derecha:
                self.velocidad_x = self.dash_velocidad
            else:
                self.velocidad_x = -self.dash_velocidad
            self.velocidad_y *= 0.3
    def moverIzquierda(self):
        if self.dash_duracion <= 0 and self.estoy_vivo and not self.pausado:
            self.velocidad_x = -5
            self.mirando_derecha = False

    def moverDerecha(self):
        if self.dash_duracion <= 0 and self.estoy_vivo and not self.pausado:
            self.velocidad_x = 5
            self.mirando_derecha = True

    def detenerse(self):
        if self.dash_duracion <= 0 :
            self.velocidad_x = 0
    def respawnear (self,x,y):
        self.estoy_vivo = True
        self.imagen = self.animaciones["saltando"]["frames"][self.animaciones["saltando"]["frameIndex"]]
        self.rect.x = x
        self.rect.y = y