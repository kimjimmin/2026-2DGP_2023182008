# 실습 과제 진행
from pico2d import *
import math

#상수화
WIDTH = 800
HEIGHT = 600
MOVE_DELAY = 0.01

#상수화 - 사각형 좌표
LEFT = 50
RIGHT = 750
BOTTOM = 50
TOP = 550
MOVE_STEP = 5

#상수화 - 삼각형 좌표
TRI_TOP_X = 400
TRI_TOP_Y = 550

TRI_LEFT_X = 100
TRI_LEFT_Y = 50

TRI_RIGHT_X = 700
TRI_RIGHT_Y = 50

open_canvas(WIDTH, HEIGHT)
boy = load_image('character.png')

# 사각형에 구현에 필요한 함수
def move_top():
    for x in range(LEFT, RIGHT + 1, MOVE_STEP):
        draw_boy(x, TOP)

def move_right():
      for y in range(TOP, BOTTOM - 1, -MOVE_STEP):
        draw_boy(RIGHT, y)

def move_bottom():
    for x in range(RIGHT, LEFT - 1, -MOVE_STEP):
        draw_boy(x, BOTTOM)

def move_left():
    for y in range(BOTTOM, TOP + 1, MOVE_STEP):
        draw_boy(LEFT, y)

# 삼각형 구현에 필요한 함수
def move_triangle_left():
    move_line(400, 550, 100, 50, 100)

def move_triangle_bottom():
     move_line(100, 50, 700, 50, 120)

def move_triangle_right():
    move_line(700, 50, 400, 550, 100)

def move_line(start_x, start_y, end_x, end_y, steps):
    for i in range(steps + 1):
        t = i / steps

        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t

        draw_boy(x, y)    

#공통 함수
def draw_boy(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(MOVE_DELAY)

# 주인공 움직이게 하는 함수
def move_circle():
    for degree in range(360):
        angle = math.radians(degree)
        x = 400 + 200 * math.cos(angle)
        y = 300 + 200 * math.sin(angle)
        draw_boy(x, y)

def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()

def move_triangle():
    move_triangle_left()
    move_triangle_bottom()
    move_triangle_right()

# 전체 움직임 구현
def move_boy():
    move_circle()
    move_rectangle()
    move_triangle()

def main():
    while True:
        move_boy()


main()
