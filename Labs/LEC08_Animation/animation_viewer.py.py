from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('sonic-sprite.png')

frame = 0

clear_canvas()
character.draw(400, 90)
update_canvas()
delay(5)

