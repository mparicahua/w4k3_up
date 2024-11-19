import pygame
import sys
pygame.init()
WIDTH = 960
HEIGHT = 480
PANTALLA_PRESENTACION = 0
PANTALLA_MENU = 1
PANTALLA_JUEGO = 2
FPS = 60
TAMANIO_COLUMNA = 512
TAMANIO_FILA = 512
TAMANIO_IMAGENES_PLATAFORMA = 49
UBICACION_MAPA = "assets/mapa/plataforma01.csv"
# Colores
DARK_RED = (139, 0, 0)
GOLD = (218, 165, 32)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)

#Fuentes
try:
    GOTHIC_BIG = pygame.font.Font("assets/fuentes/MorrisRoman-Black.ttf", 72)
    GOTHIC_MENU  = pygame.font.Font("assets/fuentes/MorrisRoman-Black.ttf", 48)
    GOTHIC_SMALL  = pygame.font.Font("assets/fuentes/MorrisRoman-Black.ttf", 24)
except:
    GOTHIC_BIG = pygame.font.Font(None, 72)
    GOTHIC_MENU = pygame.font.Font(None, 48)
    GOTHIC_SMALL = pygame.font.Font(None, 24)
FUENTE_GRANDE  = pygame.font.Font(None, 48)
FUENTE_NORMAL  = pygame.font.Font(None, 36)
FUENTE_PEQUENIA  = pygame.font.Font(None, 24) 