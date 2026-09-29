from pico2d import *

open_canvas(800, 600)
grass = load_image('grass.png')
character = load_image('character.png')

for i in range(2):
    x = 0
    while x < 800:
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, 90)
        update_canvas()
        x += 8
        delay(0.01)
    y =90;
    while y < 540:
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
        y += 8
        delay(0.01)
    while x > 0:
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
        x -= 8
        delay(0.01)

    while y > 90:
        clear_canvas()
        grass.draw(400, 30)
        character.draw(x, y)
        update_canvas()
        y -= 8
        delay(0.01)

update_canvas()
close_canvas()