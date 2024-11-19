import pygame
from constantes import GOTHIC_MENU,GRAY,GOLD
class MenuItem:
    def __init__(self, texto, position, callback):
        self.texto_normal = GOTHIC_MENU.render(texto, True, GRAY)
        self.texto_seleccionado = GOTHIC_MENU.render(">"+texto, True, GOLD)
        self.rect = self.texto_normal.get_rect(center=position)
        self.callback = callback
        self.seleccionado = False

    def dibujar(self, surface):
        texto_dibujar = self.texto_seleccionado if self.seleccionado else self.texto_normal
        surface.blit(texto_dibujar, self.rect)

    def manejar_evento(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.seleccionado = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.seleccionado:
            self.callback()