import pygame
import sys
import csv
from constantes import WIDTH, HEIGHT,PANTALLA_PRESENTACION ,PANTALLA_MENU ,PANTALLA_JUEGO ,FPS,GOTHIC_BIG,GOTHIC_MENU,GOTHIC_SMALL,DARK_RED,GRAY,FUENTE_GRANDE,FUENTE_NORMAL,FUENTE_PEQUENIA,TAMANIO_COLUMNA ,TAMANIO_FILA ,TAMANIO_IMAGENES_PLATAFORMA,UBICACION_MAPA 

from entidades.jugador import Jugador
from entidades.plataforma import Plataforma
from entidades.camara import Camara
from entidades.menu import MenuItem
from entidades.mundo import Mundo

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.estado_actual_pantalla = PANTALLA_PRESENTACION

        self.todos_sprites = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.almas = pygame.sprite.Group()
        self.jugador = None
        self.camara = None
        self.menu_items =[]
        self.scroll = 0
        self.mundo_diseño = Mundo()
        self.inicializar_juego()
    def check_colicion_horizontal(self):
        self.jugador.rect.x += self.jugador.velocidad_x
        lista_coliciones_plataformas_verticales = pygame.sprite.spritecollide(self.jugador, self.plataformas, False)
        for plataforma in lista_coliciones_plataformas_verticales:
            if self.jugador.velocidad_x > 0:
                self.jugador.rect.right = plataforma.rect.left
            elif self.jugador.velocidad_x < 0:
                self.jugador.rect.left = plataforma.rect.right
            self.jugador.velocidad_x = 0
    def check_colicion_vertical(self):
        self.jugador.rect.y += self.jugador.velocidad_y
        lista_coliciones_plataformas_horizontales = pygame.sprite.spritecollide(self.jugador, self.plataformas, False)
        for plataforma in lista_coliciones_plataformas_horizontales:
            if self.jugador.velocidad_y > 0:
                self.jugador.rect.bottom = plataforma.rect.top
                self.jugador.saltando = False
                self.jugador.doble_salto_disponible = True
            elif self.jugador.velocidad_y < 0:
                self.jugador.rect.top = plataforma.rect.bottom
            self.jugador.velocidad_y = 0
    def comenzar_juego(self):
        self.estado_actual_pantalla = PANTALLA_JUEGO
    def terminar_juego(self):
        pygame.quit()
        sys.exit()  
    def inicializar_juego(self):
        self.inicializar_jugador()
        self.inicializar_platformas()
        
        self.inicializar_musica()
        self.inicializar_items_menu()
        self.inicializar_bg()
    def inicializar_items_menu(self):
        items = [
            ["Nuevo Juego", (self.screen.get_width() - 200, self.screen.get_height()/2 ), self.comenzar_juego],
            ["Opciones", (self.screen.get_width() - 200, self.screen.get_height()/2 + 100) , lambda: None],
            ["Salir", (self.screen.get_width() - 200, self.screen.get_height()/2 + 200), self.terminar_juego]
        ]
        for i in items:
            item = MenuItem(i[0], i[1], i[2])
            self.menu_items.append(item)
    def inicializar_platformas(self):
        data_plataformas = []
        for fila in range(TAMANIO_COLUMNA):
            filas = [-1] * TAMANIO_FILA
            data_plataformas.append(filas)

        with open(UBICACION_MAPA,newline='')as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            for x,fila in enumerate(reader):
                for y,columna in enumerate(fila):
                    data_plataformas[x][y] = int(columna)
        tile_list = []
        for x in range(TAMANIO_IMAGENES_PLATAFORMA):
            tile_image = pygame.image.load(f"assets/imagenes/plataformas/tile{x}.png")
            tile_image = pygame.transform.scale(tile_image,(60,60))
            tile_list.append(tile_image)


        self.mundo_diseño.process_data(data_plataformas,tile_list)

        for tile in  self.mundo_diseño.mapa_tiles:
            p = Plataforma(tile[2] ,tile[3],tile[0])
            self.todos_sprites.add(p)
            self.plataformas.add(p)
    def inicializar_bg(self):
        for i in range(1, 5):
            bg_image = pygame.image.load(f"assets/imagenes/background/background{i}.png").convert_alpha()
            self.mundo_diseño.bg_imagenes.append(bg_image)
    def inicializar_jugador(self):
        self.camara = Camara()
        self.jugador = Jugador()
        self.todos_sprites.add(self.jugador)   
    def inicializar_musica(self):
        pygame.mixer.music.load("assets/musica/Other World.mp3")
        pygame.mixer.music.play(100)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jugador.saltar()
                if event.key == pygame.K_z:
                    self.jugador.activar_doble_salto()
                if event.key == pygame.K_x:
                    self.jugador.activar_seguimeinto_camara_x()
                if event.key == pygame.K_c:
                    self.jugador.activar_seguimeinto_camara_y()
                if event.key == pygame.K_v:  
                    self.jugador.activar_dash()
                if event.key == pygame.K_e:  
                    self.jugador.ejecutar_dash()
                if event.key == pygame.K_BACKSPACE:  
                    self.jugador.activar_muerte_jugador()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.jugador.detenerse()
            if self.estado_actual_pantalla == PANTALLA_PRESENTACION:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    self.estado_actual_pantalla = PANTALLA_MENU
            elif self.estado_actual_pantalla == PANTALLA_MENU:
                for item in self.menu_items:
                    item.manejar_evento(event)        
    def update(self):
        if self.estado_actual_pantalla == PANTALLA_JUEGO:
            self.todos_sprites.update()
            self.camara.update(self.jugador)
    def render(self):
        titulo_presentacion = GOTHIC_BIG.render("Wake Up", True, DARK_RED)
        mensaje_presentacion = GOTHIC_SMALL.render("Pulsa cualquier boton", True, GRAY)
        titulo_presentacion_posicion = titulo_presentacion.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/3))
        mensaje_presentacion_posicion = mensaje_presentacion.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()*2/3))


        if self.estado_actual_pantalla == PANTALLA_PRESENTACION:
            self.screen.fill((0, 0, 0))
            self.screen.blit(titulo_presentacion, titulo_presentacion_posicion)
            self.screen.blit(mensaje_presentacion, mensaje_presentacion_posicion)
        elif self.estado_actual_pantalla == PANTALLA_MENU:
            self.screen.fill((52, 73, 94))
            fondo_menu = pygame.image.load("assets/imagenes/portada/Facing_Straight.png")
            fondo_menu = pygame.transform.scale(fondo_menu,(60,60))
            self.screen.blit(fondo_menu,(0,0))
            for item in self.menu_items:
                item.dibujar(self.screen)
        elif self.estado_actual_pantalla == PANTALLA_JUEGO:
            self.screen.fill((255, 255, 255))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.scroll += (self.jugador.velocidad_x)/4
                self.jugador.moverIzquierda()

            if keys[pygame.K_RIGHT]:
                self.scroll += (self.jugador.velocidad_x)/4
                self.jugador.moverDerecha()
            self.mundo_diseño.dibujar_bg(self.screen,self.scroll)
            for sprite in self.todos_sprites:
                #coregir bug visual de volver quitar seguimiento x o y
                sprite.rect.x = sprite.rect.x - self.camara.x
                sprite.rect.y = sprite.rect.y - self.camara.y

                if hasattr(sprite, 'mirando_derecha'):
                    imagen_flip = pygame.transform.flip(sprite.imagen,not sprite.mirando_derecha,False)
                    self.screen.blit(imagen_flip, (sprite.rect.x , sprite.rect.y ))
                else:
                    self.screen.blit(sprite.imagen, (sprite.rect.x , sprite.rect.y ))
            #Variables en tiempo real
            if self.jugador.doble_salto_habilitado:
                estado = "Doble Salto: Activado"
                color = (0, 255, 0)
            else:
                estado = "Doble Salto: Desactivado"
                color = (255, 0, 0)
            if self.jugador.dash_habilitado:
                estado_dash = "Dash: Activado"
                color_dash = (0, 255, 0)
            else:
                estado_dash = "Dash: Desactivado"
                color_dash = (255, 0, 0)
            if self.jugador.seguimiento_camara_x:
                estado_camara_x = "Seguimiento Camara X: Activado"
                color_camara_x = (0, 255, 0)
            else:
                estado_camara_x = "Seguimiento Camara X: Desactivado"
                color_camara_x = (255, 0, 0)
            if self.jugador.seguimiento_camara_y:
                estado_camara_y = "Seguimiento Camara Y: Activado"
                color_camara_y = (0, 255, 0)
            else:
                estado_camara_y = "Seguimiento Camara Y: Desactivado"
                color_camara_y = (255, 0, 0)

            
            pos_texto = FUENTE_PEQUENIA.render(f"X: {self.jugador.rect.x}, Y: {self.jugador.rect.y}", True, (100, 100, 100))
            self.screen.blit(pos_texto, (10, 10)) 
            pos_texto = FUENTE_PEQUENIA.render(f"Velocidad X: {self.jugador.velocidad_x}, Velocidad Y: {self.jugador.velocidad_y}", True, (100, 100, 100))
            self.screen.blit(pos_texto, (10, 30))

            texto_estado = FUENTE_PEQUENIA.render(estado, True, color)
            self.screen.blit(texto_estado, (10, 50))
            texto_estado = FUENTE_PEQUENIA.render(estado_dash, True, color_dash)
            self.screen.blit(texto_estado, (10, 70))


            texto_estado = FUENTE_PEQUENIA.render(estado_camara_x, True, color_camara_x)
            self.screen.blit(texto_estado, (10, 90))
            texto_estado = FUENTE_PEQUENIA.render(estado_camara_y, True, color_camara_y)
            self.screen.blit(texto_estado, (10, 110))


            pos_texto = FUENTE_PEQUENIA.render(f"Camara X: {self.camara.x}", True, (100, 100, 100))
            self.screen.blit(pos_texto, (10, 130)) 
            pos_texto = FUENTE_PEQUENIA.render(f"Camara Y: {self.camara.y}", True, (100, 100, 100))
            self.screen.blit(pos_texto, (10, 150)) 
            pos_texto = FUENTE_PEQUENIA.render(f"Estoy vivo: {self.jugador.estoy_vivo}", True, (100, 100, 100))
            self.screen.blit(pos_texto, (10, 170)) 
            
        pygame.display.flip()  
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.check_colicion_horizontal()
            self.check_colicion_vertical()
            self.render()
            #self.mundo_diseño.dibujar_bg(self.screen,self.scroll)
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
