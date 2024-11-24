import pygame
class Alma(pygame.sprite.Sprite):
    cantidad_almas_juego = 0
    def __init__(self,x,y):
        super().__init__()
        self.imagen = pygame.image.load("assets/imagenes/alma/tile0.png")
        rect = pygame.Rect(53, 53, 45, 45)
        self.imagen = self.imagen.subsurface(rect)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cantidad_almas = 1
        Alma.cantidad_almas_juego += 1
    @classmethod
    def total_almas_juego(cls):
        return cls.cantidad_almas_juego