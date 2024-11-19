from constantes import WIDTH, HEIGHT
class Camara:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def update(self, objeto):
        if objeto.seguimiento_camara_x:
            self.x = (objeto.rect.centerx - WIDTH // 2) if objeto.seguimiento_camara_x else 0
        if objeto.seguimiento_camara_y:
            self.y = (objeto.rect.centery - HEIGHT // (3/2)) if objeto.seguimiento_camara_y else 0