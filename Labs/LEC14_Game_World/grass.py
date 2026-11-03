from pico2d import load_image


class Grass_back:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass

class Grass_front:
    def __init__(self):
        self.image = load_image('grass.png')
    
    def draw(self):
        self.image.draw(400, 20)
    
    def update(self):
        pass
