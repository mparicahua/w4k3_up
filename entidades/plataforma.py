import pygame

class Plataforma(pygame.sprite.Sprite):
    def __init__(self,x,y,imagen,tipo):
        """Tipo R es plataforma regular
        Tipo M es plataforma de muerte
        Tipo D es plataforma deslisable"""
        super().__init__()
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tipo = tipo
