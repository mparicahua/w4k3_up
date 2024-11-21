import pygame
class Alma(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.imagen = pygame.image.load("assets/imagenes/alma/tile0.png")

        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cantidad_almas = 1