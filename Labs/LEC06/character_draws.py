# 실습 과제 진행
from pico2d import *
import math

open_canvas(800, 600)
boy = load_image('character.png')

# 사각형에 구현에 필요한 함수
def move_top():
    for x in range(50, 751, 5):
        draw_boy(x, 550)

def move_right():
      for y in range(550, 49, -5):
        draw_boy(750, y)

def move_bottom():
    for x in range(750, 49, -5):
        draw_boy(x, 50)

def move_left():
    for y in range(50, 551, 5):
        draw_boy(50, y)

# 삼각형 구현에 필요한 함수
def move_triangle_left():
    for i in range(101):
        x = 400 - 3 * i
        y = 550 - 5 * i

        draw_boy(x, y)

def move_triangle_bottom():
     for x in range(100, 701, 5):
        draw_boy(x, 50)

def move_triangle_right():
    for i in range(101):
        x = 700 - 3 * i
        y = 50 + 5 * i

        draw_boy(x, y)

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

while True:
    move_boy()
