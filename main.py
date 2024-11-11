import pygame
import sys
pygame.init()

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen = pygame.Surface((30, 50))
        self.imagen.fill((0, 255, 100))
        self.saltando = False
        self.rect = self.imagen.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 70
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.mirando_derecha = True
        self.doble_salto_disponible = True
        self.doble_salto_habilitado = False 
        self.seguimiento_camara_y = True 
        self.seguimiento_camara_x = True 
    
    def activar_doble_salto(self):
        self.doble_salto_habilitado = not self.doble_salto_habilitado
    def activar_seguimeinto_camara_y(self):
        self.seguimiento_camara_y = not self.seguimiento_camara_y
    def activar_seguimeinto_camara_x(self):
        self.seguimiento_camara_x = not self.seguimiento_camara_x

    def update(self):
        self.velocidad_y += 0.5  # Gravedad
        if self.velocidad_y > 10:  # Velocidad terminal
            self.velocidad_y = 10
        # Mover horizontalmente
        self.rect.x += self.velocidad_x
        

        lista_coliciones_plataformas_verticales = pygame.sprite.spritecollide(self, plataformas, False)
        for plataforma in lista_coliciones_plataformas_verticales:
            if self.velocidad_x > 0:
                self.rect.right = plataforma.rect.left
            elif self.velocidad_x < 0:
                self.rect.left = plataforma.rect.right

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
        elif self.doble_salto_habilitado and self.doble_salto_disponible:  # Doble salto
            self.velocidad_y = -10
            self.doble_salto_disponible = False
    def moverIzquierda(self):
        self.velocidad_x = -5
        self.mirando_derecha = False
    def moverDerecha(self):
        self.velocidad_x = 5
        self.mirando_derecha = True
    def detenerse(self):
        self.velocidad_x = 0
class Rectangulo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen = pygame.Surface((30, 50))
        self.imagen.fill("blue")
        self.posicion=[0,0]
    def moverDerecha(self):
        self.posicion[0] += 5
        print(self.posicion)
    def moverIzquierda(self):
        self.posicion[0] -= 5
        print(self.posicion)
    def moverArriba(self):
        self.posicion[1] -= 5
        print(self.posicion)
    def moverAbajo(self):
        self.posicion[1] += 5
        print(self.posicion)
class Plataforma(pygame.sprite.Sprite):
    def __init__(self,x,y,ancho,alto):
        super().__init__()
        self.imagen = pygame.Surface((ancho, alto))
        self.imagen.fill((0, 255, 0))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
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
WIDTH = 800
HEIGHT = 600
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

soul = Jugador()

lista_plataformas = [
    [0, screen.get_height() - 20, screen.get_width()*10, 4000],#Piso del nivel
    [-500,-500,500,screen.get_height() + 1000],#pared izquierda
    [100, screen.get_height() - 40, 100, 40],
    [200, screen.get_height() - 100, 100, 10],
    [screen.get_width()*10, screen.get_height()+2000, screen.get_width()*10, 2000],#Piso del nivel 2
]
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

for plataforma in  lista_plataformas:
    p = Plataforma(plataforma[0], plataforma[1], plataforma[2], plataforma[3])
    todos_sprites.add(p)
    plataformas.add(p)



# Configuración de fuentes
fuente_grande = pygame.font.Font(None, 48)
fuente_normal = pygame.font.Font(None, 36)
fuente_pequeña = pygame.font.Font(None, 24) 

camera_x = 0
camera_y = 0

habilitar_camara_y = True
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
        screen.fill((0, 0, 0))
        for item in menu_items:
            item.dibujar(screen)

    elif estado_actual_pantalla == PANTALLA_JUEGO:
        screen.fill("white")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            soul.moverIzquierda()
        if keys[pygame.K_RIGHT]:
            soul.moverDerecha()

        camera_x = (soul.rect.centerx - WIDTH // 2) if soul.seguimiento_camara_x else 0
        camera_y = soul.rect.centery - HEIGHT // (6/5) if soul.seguimiento_camara_y else 0

        todos_sprites.update()
        espacio_linea = 0
        for sprite in todos_sprites:
            
            screen.blit(sprite.imagen, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))
            pos_texto = fuente_pequeña.render(f"Tipo:{type(sprite)} X: {sprite.rect.x}, Y: {sprite.rect.y}", True, (100, 100, 100))
            screen.blit(pos_texto, (400, 10 + espacio_linea)) 
            espacio_linea += 20
        #Variables en tiempo real
        if soul.doble_salto_habilitado:
            estado = "Doble Salto: Activado"
            color = (0, 255, 0)
        else:
            estado = "Doble Salto: Desactivado"
            color = (255, 0, 0)
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
        texto_estado = fuente_pequeña.render(estado_camara_x, True, color_camara_x)
        screen.blit(texto_estado, (10, 70))
        texto_estado = fuente_pequeña.render(estado_camara_y, True, color_camara_y)
        screen.blit(texto_estado, (10, 90))


        pos_texto = fuente_pequeña.render(f"Camara X: {camera_x}", True, (100, 100, 100))
        screen.blit(pos_texto, (10, 110)) 
        pos_texto = fuente_pequeña.render(f"Camara Y: {camera_y}", True, (100, 100, 100))
        screen.blit(pos_texto, (10, 130)) 
    pygame.display.flip()
    clock.tick(60)
pygame.quit()