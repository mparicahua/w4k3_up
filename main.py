import pygame
import sys
import csv
from mundo import Mundo
pygame.init()
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animaciones = {"corriendo": {"frames":[],"frameIndex":1,"numeroFrames":6,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"","repetir":True},
                            "parado": {"frames":[],"frameIndex":1,"numeroFrames":17,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"","repetir":True},
                            "saltando": {"frames":[],"frameIndex":1,"numeroFrames":5,"cooldownAnimacion":200,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"","repetir":True},
                            "dasheando": {"frames":[],"frameIndex":1,"numeroFrames":15,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"D","repetir":True},
                            "muriendo": {"frames":[],"frameIndex":1,"numeroFrames":15,"cooldownAnimacion":100,"actualizado_fecha":pygame.time.get_ticks(),"tipo":"D","repetir":False}
                            }
        self.cargar_animacion()
        self.imagen = self.animaciones["saltando"]["frames"][self.animaciones["saltando"]["frameIndex"]]
        #self.imagen.fill((0, 255, 100))
        

        self.saltando = False
        self.rect = self.imagen.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 70
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.mirando_derecha = True

        self.doble_salto_disponible = True
        self.doble_salto_habilitado = False 
        self.seguimiento_camara_y = True 
        self.seguimiento_camara_x = True 

        #Pruebas dash
        self.dash_habilitado = False
        self.puede_dash = True
        self.dash_cooldown = 0
        self.dash_duracion = 0
        self.dash_velocidad = 15
        ##########################

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

    def update(self):
        #Animaciones
        if self.saltando:
            self.imagen = self.animaciones["saltando"]["frames"][self.animaciones["saltando"]["frameIndex"]]
        else:
            if  self.velocidad_x != 0:
                self.imagen = self.animaciones["corriendo"]["frames"][self.animaciones["corriendo"]["frameIndex"]]
            else :
                self.imagen = self.animaciones["parado"]["frames"][self.animaciones["parado"]["frameIndex"]]
        if self.puede_dash == False:
            self.imagen = self.animaciones["dasheando"]["frames"][self.animaciones["saltando"]["frameIndex"]]

            
        for nombre_animacion in self.animaciones.keys():
            if pygame.time.get_ticks() - self.animaciones[nombre_animacion]["actualizado_fecha"] >= self.animaciones[nombre_animacion]["cooldownAnimacion"]:
                self.animaciones[nombre_animacion]["frameIndex"] += 1
                self.animaciones[nombre_animacion]["actualizado_fecha"] = pygame.time.get_ticks()
            if self.animaciones[nombre_animacion]["frameIndex"] >= len(self.animaciones[nombre_animacion]["frames"]):
                self.animaciones[nombre_animacion]["frameIndex"]  = 1 
        
        #################################################

        if self.dash_duracion > 0:
            self.dash_duracion -= 1
            if self.dash_duracion <= 0:
                self.velocidad_x = 0
        

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
            if self.dash_cooldown <= 0:
                self.puede_dash = True


        self.velocidad_y += 0.5 
        if self.velocidad_y > 10: 
            self.velocidad_y = 10
        # Mover horizontalmente
        self.rect.x += self.velocidad_x
        

        lista_coliciones_plataformas_verticales = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in lista_coliciones_plataformas_verticales:
            if self.velocidad_x > 0:
                self.rect.right = plataforma.rect.left
            elif self.velocidad_x < 0:
                self.rect.left = plataforma.rect.right
            self.velocidad_x = 0

        # Mover verticalmente
        self.rect.y += self.velocidad_y

        lista_coliciones_plataformas_horizontales = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in lista_coliciones_plataformas_horizontales:
            if self.velocidad_y > 0:
                self.rect.bottom = plataforma.rect.top
                self.saltando = False
                self.doble_salto_disponible = True
            elif self.velocidad_y < 0:
                self.rect.top = plataforma.rect.bottom
            self.velocidad_y = 0

        
        
    def saltar(self):
        if self.saltando == False:
            self.velocidad_y = -10
            self.saltando = True
        elif self.doble_salto_habilitado and self.doble_salto_disponible:
            self.velocidad_y = -10
            self.doble_salto_disponible = False
    def ejecutar_dash(self):
        if self.dash_habilitado and self.puede_dash:
            self.dash_duracion = 10
            self.puede_dash = False
            self.dash_cooldown = 30
            if self.mirando_derecha:
                self.velocidad_x = self.dash_velocidad
            else:
                self.velocidad_x = -self.dash_velocidad
            self.velocidad_y *= 0.3
    def moverIzquierda(self):
        if self.dash_duracion <= 0:
            self.velocidad_x = -5
            self.mirando_derecha = False

    def moverDerecha(self):
        if self.dash_duracion <= 0: 
            self.velocidad_x = 5
            self.mirando_derecha = True

    def detenerse(self):
        if self.dash_duracion <= 0:
            self.velocidad_x = 0
class Plataforma(pygame.sprite.Sprite):
    def __init__(self,x,y,imagen):
        super().__init__()
        self.imagen = imagen
        #self.imagen.fill((0, 0, 0))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
    def crear_plataforma(x, y, ancho, alto): 
   
        nueva_plataforma = Plataforma(x, y, ancho, alto)
        todos_sprites.add(nueva_plataforma)
        plataformas.add(nueva_plataforma)
class MenuItem:
    def __init__(self, texto, position, callback):
        self.texto_normal = gothic_menu.render(texto, True, GRAY)
        self.texto_seleccionado = gothic_menu.render(">"+texto, True, GOLD)
        self.rect = self.texto_normal.get_rect(center=position)
        self.callback = callback
        self.seleccionado = False

    def dibujar(self, surface):
        texto_dibujar = self.texto_seleccionado if self.seleccionado else self.texto_normal
        surface.blit(texto_dibujar, self.rect)

    def manejar_eveto(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.seleccionado = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.seleccionado:
            self.callback()
#variables
WIDTH = 960
HEIGHT = 480
PANTALLA_PRESENTACION = 0
PANTALLA_MENU = 1
PANTALLA_JUEGO = 2
estado_actual_pantalla = PANTALLA_PRESENTACION

# Colores
DARK_RED = (139, 0, 0)
GOLD = (218, 165, 32)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)




#Fuentes
try:
    gothic_big = pygame.font.Font("assets/fuentes/MorrisRoman-Black.ttf", 72)
    gothic_menu = pygame.font.Font("assets/fuentes/MorrisRoman-Black.ttf", 48)
    gothic_small = pygame.font.Font("assets/fuentes/MorrisRoman-Black.ttf", 24)
except:
    gothic_big = pygame.font.Font(None, 72)
    gothic_menu = pygame.font.Font(None, 48)
    gothic_small = pygame.font.Font(None, 24)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


########################################################
#define game variables
scroll = 0
bg_images = []
for i in range(1, 5):
  bg_image = pygame.image.load(f"assets/imagenes/background/background{i}.png").convert_alpha()
  bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
  for x in range(5):
    speed = 1
    for i in bg_images:
      screen.blit(i, ((x * bg_width) - scroll * speed, 0))
      speed += 0.2

########################################################





soul = Jugador()

# lista_plataformas = [
#     [0, screen.get_height() - 20, screen.get_width()*10, 4000],#Piso del nivel
#     [-500,-500,500,screen.get_height() + 1000],#pared izquierda
#     [100, screen.get_height() - 40, 100, 40],
#     [200, screen.get_height() - 120, 100, 10],
#     [screen.get_width()*10, screen.get_height()+2000, screen.get_width()*10, 2000],#Piso del nivel 2
# ]
def comenzar_juego():
    global estado_actual_pantalla
    estado_actual_pantalla = PANTALLA_JUEGO

def terminar_juego():
    pygame.quit()
    sys.exit()

# Configuración del menú principal
menu_items = [
    MenuItem("Nuevo Juego", (screen.get_width() - 200, screen.get_height()/2 ), comenzar_juego),
    MenuItem("Opciones", (screen.get_width() - 200, screen.get_height()/2 + 100) , lambda: None),
    MenuItem("Salir", (screen.get_width() - 200, screen.get_height()/2 + 200), terminar_juego)
]

#titulo PANTALLA DE PRESENTACION
titulo_presentacion = gothic_big.render("Wake Up", True, DARK_RED)
mensaje_presentacion = gothic_small.render("Pulsa cualquier boton", True, GRAY)
titulo_presentacion_posicion = titulo_presentacion.get_rect(center=(screen.get_width()/2, screen.get_height()/3))
mensaje_presentacion_posicion = mensaje_presentacion.get_rect(center=(screen.get_width()/2, screen.get_height()*2/3))



todos_sprites = pygame.sprite.Group()
plataformas = pygame.sprite.Group()
todos_sprites.add(soul)

# for plataforma in  lista_plataformas:
#     p = Plataforma(plataforma[0], plataforma[1], plataforma[2], plataforma[3])
#     todos_sprites.add(p)
#     plataformas.add(p)
# Plataforma.crear_plataforma(140,500, 140,20) #1
# Plataforma.crear_plataforma(490,500, 70, 100 ) #2
# Plataforma.crear_plataforma(560,420,140,200) #3
# Plataforma.crear_plataforma(630,280,70,20) #4
# Plataforma.crear_plataforma(420,180,280,20) #5
# Plataforma.crear_plataforma(0,180, 280, 20) #6
# Plataforma.crear_plataforma(140,80,140,20)#7
# Plataforma.crear_plataforma(350,0, 140, 20) # plataforma del medio y = 0 #8
# Plataforma.crear_plataforma(560, -80, 140, 20) #9
# Plataforma.crear_plataforma(350,-160, 140, 20) #10
# Plataforma.crear_plataforma(140, -240, 70, 20) #11
# Plataforma.crear_plataforma(630,-240, 70,20) #12
# Plataforma.crear_plataforma(910, -80,70,20) #13
# Plataforma.crear_plataforma(1120, -160,70,20) #14
# Plataforma.crear_plataforma(1330, -240,70,20) #15
# Plataforma.crear_plataforma(1540, -160,70,20) #16
# Plataforma.crear_plataforma(1750, -240,70,20) #17
# Plataforma.crear_plataforma(1260,500,70,120) #18
# Plataforma.crear_plataforma(1330,280,70,20) #19
# Plataforma.crear_plataforma(1540,200,70,20) #20
# Plataforma.crear_plataforma(1750, 120,70,20) #21
# Plataforma.crear_plataforma(1820,420,140,20) #22
# #plataformas verticales ancho < alto
# Plataforma.crear_plataforma(350,180,70,300) #23
# Plataforma.crear_plataforma(770,-240, 70,720) #24

pygame.mixer.music.load("assets/musica/Other World.mp3")
pygame.mixer.music.play(100)


# Configuración de fuentes
fuente_grande = pygame.font.Font(None, 48)
fuente_normal = pygame.font.Font(None, 36)
fuente_pequeña = pygame.font.Font(None, 24) 

camera_x = 0
camera_y = 0



world_data = []
for fila in range(512):
    filas = [-1] * 512
    world_data.append(filas)

with open("assets/mapa/plataforma02.csv",newline='')as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    for x,fila in enumerate(reader):
        for y,columna in enumerate(fila):
            world_data[x][y] = int(columna)



tile_list = []
for x in range(49):
    tile_image = pygame.image.load(f"assets/imagenes/plataformas/tile{x}.png")
    tile_image = pygame.transform.scale(tile_image,(60,60))
    tile_list.append(tile_image)

mundo = Mundo()
mundo.process_data(world_data,tile_list)

for tile in  mundo.map_tiles:
    p = Plataforma(tile[2] ,tile[3],tile[0])
    todos_sprites.add(p)
    plataformas.add(p)




clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                soul.saltar()
            if event.key == pygame.K_z:
                soul.activar_doble_salto()
            if event.key == pygame.K_x:
                soul.activar_seguimeinto_camara_x()
            if event.key == pygame.K_c:
                soul.activar_seguimeinto_camara_y()
            if event.key == pygame.K_v:  
                soul.activar_dash()
            if event.key == pygame.K_e:  
                soul.ejecutar_dash()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                soul.detenerse()
        if estado_actual_pantalla == PANTALLA_PRESENTACION:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                estado_actual_pantalla = PANTALLA_MENU
        elif estado_actual_pantalla == PANTALLA_MENU:
            for item in menu_items:
                item.manejar_eveto(event)
    if estado_actual_pantalla == PANTALLA_PRESENTACION:
        screen.fill((0, 0, 0))
        screen.blit(titulo_presentacion, titulo_presentacion_posicion)
        screen.blit(mensaje_presentacion, mensaje_presentacion_posicion)

    elif estado_actual_pantalla == PANTALLA_MENU:
        screen.fill((52, 73, 94))
        fondo_menu = pygame.image.load("assets/imagenes/portada/Facing_Straight.png")
        screen.blit(fondo_menu,(0,0))
        
        for item in menu_items:
            item.dibujar(screen)

    elif estado_actual_pantalla == PANTALLA_JUEGO:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            soul.moverIzquierda()

        if keys[pygame.K_RIGHT]:
            soul.moverDerecha()
       

        camera_x = (soul.rect.centerx - WIDTH // 2) if soul.seguimiento_camara_x else 0
        camera_y = (soul.rect.centery - HEIGHT // (3/2)) if soul.seguimiento_camara_y else 0
        
        todos_sprites.update()
        espacio_linea = 0
        
        if keys[pygame.K_LEFT] and scroll > 0:
            scroll += (soul.velocidad_x)/4
        if keys[pygame.K_RIGHT] and scroll < 3000:
            scroll += (soul.velocidad_x)/4
        draw_bg()
        for sprite in todos_sprites:
            #coregir bug visual de volver quitar seguimiento x o y
            sprite.rect.x = sprite.rect.x - camera_x
            sprite.rect.y = sprite.rect.y - camera_y

            if hasattr(sprite, 'mirando_derecha'):
                imagen_flip = pygame.transform.flip(sprite.imagen,not sprite.mirando_derecha,False)
                screen.blit(imagen_flip, (sprite.rect.x , sprite.rect.y ))
            else:
                screen.blit(sprite.imagen, (sprite.rect.x , sprite.rect.y ))
            
            ###############################################################
            # pos_texto = fuente_pequeña.render(f"Tipo:{type(sprite)} X: {sprite.rect.x}, Y: {sprite.rect.y}", True, (100, 100, 100))
            # screen.blit(pos_texto, (400, 10 + espacio_linea)) 
            # espacio_linea += 20
        #mundo.draw(screen)
        #Variables en tiempo real
        if soul.doble_salto_habilitado:
            estado = "Doble Salto: Activado"
            color = (0, 255, 0)
        else:
            estado = "Doble Salto: Desactivado"
            color = (255, 0, 0)
        if soul.dash_habilitado:
            estado_dash = "Dash: Activado"
            color_dash = (0, 255, 0)
        else:
            estado_dash = "Dash: Desactivado"
            color_dash = (255, 0, 0)
        if soul.seguimiento_camara_x:
            estado_camara_x = "Seguimiento Camara X: Activado"
            color_camara_x = (0, 255, 0)
        else:
            estado_camara_x = "Seguimiento Camara X: Desactivado"
            color_camara_x = (255, 0, 0)
        if soul.seguimiento_camara_y:
            estado_camara_y = "Seguimiento Camara Y: Activado"
            color_camara_y = (0, 255, 0)
        else:
            estado_camara_y = "Seguimiento Camara Y: Desactivado"
            color_camara_y = (255, 0, 0)

        
        pos_texto = fuente_pequeña.render(f"X: {soul.rect.x}, Y: {soul.rect.y}", True, (100, 100, 100))
        screen.blit(pos_texto, (10, 10)) 
        pos_texto = fuente_pequeña.render(f"Velocidad X: {soul.velocidad_x}, Velocidad Y: {soul.velocidad_y}", True, (100, 100, 100))
        screen.blit(pos_texto, (10, 30))

        texto_estado = fuente_pequeña.render(estado, True, color)
        screen.blit(texto_estado, (10, 50))
        texto_estado = fuente_pequeña.render(estado_dash, True, color_dash)
        screen.blit(texto_estado, (10, 70))


        texto_estado = fuente_pequeña.render(estado_camara_x, True, color_camara_x)
        screen.blit(texto_estado, (10, 90))
        texto_estado = fuente_pequeña.render(estado_camara_y, True, color_camara_y)
        screen.blit(texto_estado, (10, 110))


        pos_texto = fuente_pequeña.render(f"Camara X: {camera_x}", True, (100, 100, 100))
        screen.blit(pos_texto, (10, 130)) 
        pos_texto = fuente_pequeña.render(f"Camara Y: {camera_y}", True, (100, 100, 100))
        screen.blit(pos_texto, (10, 150)) 
        pos_texto = fuente_pequeña.render(f"Scroll Paralax: {scroll}", True, (100, 100, 100))
        screen.blit(pos_texto, (10, 170)) 
    pygame.display.flip()
    clock.tick(60)
pygame.quit()