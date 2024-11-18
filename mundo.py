class Mundo:
    def __init__(self):
        self.map_tiles= []
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
                    self.map_tiles.append(tile_data)
