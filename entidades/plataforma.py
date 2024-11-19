import pygame

class Plataforma(pygame.sprite.Sprite):
    def __init__(self,x,y,imagen):
        super().__init__()
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
