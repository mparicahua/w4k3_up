class Mundo:
    def __init__(self):
        self.mapa_tiles= []
        self.bg_imagenes = []
    def process_data(self, data, tile_list):
        for y, row in enumerate(data):
            for x, tile in enumerate (row):
                if tile >= 0:
                    image = tile_list[tile]
                    image_rect = image.get_rect()
                    image_x = x * 60
                    image_y = y * 60
                    image_rect.x = image_x
                    image_rect.y = image_y
                    tile_data = [image, image_rect, image_x,image_y]
                    self.mapa_tiles.append(tile_data)
    def dibujar_bg(self,screen,scroll):
        bg_width = self.bg_imagenes[0].get_width()
        for x in range(5):
            speed = 1
            for i in self.bg_imagenes:
                screen.blit(i, ((x * bg_width) - scroll * speed, 0))
                speed += 0.2