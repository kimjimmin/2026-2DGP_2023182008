# 실습 과제 진행
from pico2d import *
import math

open_canvas(800, 600)
boy = load_image('character.png')

# 사각형에 필요한 함수
def move_top():
    pass
def move_right():
    pass
def move_bottom():
    pass
def move_left():
    pass

#공통 함수
def draw_boy(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.01)

# 주인공 움직이게 하는 함수
def move_circle():
    for degree in range(360):
        angle = math.radians(degree)
        x = 400 + 200 * math.cos(angle)
        y = 300 + 200 * math.sin(angle)
    
        clear_canvas()
        boy.draw(x, y)
        update_canvas()
        delay(0.01)

def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()
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
