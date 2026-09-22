# 실습 과제 진행
from pico2d import *
open_canvas(800, 600)
boy = load_image('character.png')

def move_circle():
    print('circle')
    pass

def move_rectangle():
    print('rectangle')
    pass

def move_triangle():
    print('triangle')
    pass

while True:
    clear_canvas()
    boy.draw(400, 300)
    update_canvas()
    delay(1)
    close_canvas()
