from constantes import TAMANIO_PLATAFORMA,NUMERO_BG_PARALLAX
class Mundo:
    def __init__(self):
        self.mapa_tiles= []
        self.bg_imagenes = []
    def process_data(self, data, tile_list):
        for y, row in enumerate(data):
            for x, tile in enumerate (row):
                if tile >= 0:
                    tipo_plataforma = "R"
                    tipo_objeto = "P"
                    if tile == 8:
                        tipo_plataforma = "M"
                    if tile == 24:
                        tipo_objeto = "A"
                    image = tile_list[tile]
                    image_rect = image.get_rect()
                    image_x = x * TAMANIO_PLATAFORMA
                    image_y = y * TAMANIO_PLATAFORMA
                    image_rect.x = image_x
                    image_rect.y = image_y
                    tile_data = [image, image_rect, image_x,image_y,tipo_plataforma,tipo_objeto]
                    self.mapa_tiles.append(tile_data)
    def dibujar_bg(self,screen,scroll):
        bg_width = self.bg_imagenes[0].get_width()
        for x in range(NUMERO_BG_PARALLAX):
            velocidad = 1
            for i in self.bg_imagenes:
                screen.blit(i, ((x * bg_width) - scroll * velocidad, 0))
                velocidad += 0.2