from pico2d import *
from math import sin, cos, radians

WIDTH, HEIGHT = 800, 600
STEP = 5
DELAY = 0.01

open_canvas(WIDTH, HEIGHT)
boy = load_image('character.png')


def draw(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(DELAY)


# 점 A -> 점 B 이동
def move_line(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    steps = int(max(abs(dx), abs(dy)) / STEP)

    for i in range(steps + 1):
        t = i / steps
        draw(a[0] + dx * t, a[1] + dy * t)


# 여러 점을 차례대로 연결해서 이동
def move_path(points):
    for a, b in zip(points, points[1:] + points[:1]):
        move_line(a, b)


def move_circle():
    for degree in range(360):
        angle = radians(degree)
        draw(
            400 + 200 * cos(angle),
            300 + 200 * sin(angle)
        )


rectangle = [
    (50, 550),
    (750, 550),
    (750, 50),
    (50, 50)
]

triangle = [
    (400, 550),
    (100, 50),
    (700, 50)
]


while True:
    move_circle()
    move_path(rectangle)
    move_path(triangle)