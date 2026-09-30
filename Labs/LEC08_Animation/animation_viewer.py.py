from pico2d import *

open_canvas(800, 600)

character = load_image('fox_animation.png')

frame = 0
animation_type = 0


# 애니메이션 번호
WALK = 0
RUN = 1
JUMP = 2
ATTACK = 3


# 각 애니메이션 프레임의 X 위치
walk_x = [
    0,
    210,
    420,
    630,
    840,
    1050,
    1260
]

run_x = [
    20,
    275,
    528,
    781,
    1039
]

jump_x = [
    15,
    206,
    395,
    590,
    788,
    982,
    1165,
    1364,
    1575,
    1776
]

attack_x = [
    21,
    235,
    430,
    654,
    877,
    1098,
    1315
]


# 애니메이션 정보
animations = {
    WALK: {
        'x': walk_x,
        'y': 595,
        'width': 210,
        'height': 198,
        'next': RUN
    },

    RUN: {
        'x': run_x,
        'y': 400,
        'width': 240,
        'height': 160,
        'next': JUMP
    },

    JUMP: {
        'x': jump_x,
        'y': 203,
        'width': 190,
        'height': 190,
        'next': ATTACK
    },

    ATTACK: {
        'x': attack_x,
        'y': 23,
        'width': 230,
        'height': 180,
        'next': WALK
    }
}


# 현재 애니메이션의 프레임 출력
def draw_animation(animation_type, frame):
    animation = animations[animation_type]

    character.clip_draw(
        animation['x'][frame],
        animation['y'],
        animation['width'],
        animation['height'],

        400,
        300,

        animation['width'],
        animation['height']
    )


# 다음 프레임 계산
def update_animation(animation_type, frame):
    animation = animations[animation_type]

    frame += 1

    # 현재 애니메이션이 끝났다면
    if frame >= len(animation['x']):
        frame = 0
        animation_type = animation['next']

    return animation_type, frame


while True:
    clear_canvas()

    draw_animation(
        animation_type,
        frame
    )

    animation_type, frame = update_animation(
        animation_type,
        frame
    )

    update_canvas()
    delay(0.1)

close_canvas()