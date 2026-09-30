from pico2d import *

open_canvas(800, 600)

character = load_image('fox_animation.png')

frame = 0
animation_type = 0     # 0 = 걷기, 1 = 뛰기, 2 = 점프, 3 = 공격


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


def draw_frame(x, y, width, height):
    character.clip_draw(
        x, y,
        width, height,
        400, 300,
        width, height
    )


def draw_walk(frame):
    draw_frame(
        frame * 210,
        595,
        210,
        198
    )


def draw_run(frame):
    draw_frame(
        run_x[frame],
        400,
        240,
        160
    )


def draw_jump(frame):
    draw_frame(
        jump_x[frame],
        203,
        190,
        190
    )


def draw_attack(frame):
    draw_frame(
        attack_x[frame],
        23,
        230,
        180
    )


# 다음 프레임으로 이동
def next_frame(frame, frame_count, animation_type, next_animation):
    frame = (frame + 1) % frame_count

    if frame == 0:
        animation_type = next_animation

    return frame, animation_type


while True:
    clear_canvas()

    # 걷기
    if animation_type == 0:
        draw_walk(frame)

        frame, animation_type = next_frame(
            frame,
            7,
            animation_type,
            1
        )


    # 뛰기
    elif animation_type == 1:
        draw_run(frame)

        frame, animation_type = next_frame(
            frame,
            5,
            animation_type,
            2
        )


    # 점프
    elif animation_type == 2:
        draw_jump(frame)

        frame, animation_type = next_frame(
            frame,
            10,
            animation_type,
            3
        )


    # 공격
    elif animation_type == 3:
        draw_attack(frame)

        frame, animation_type = next_frame(
            frame,
            7,
            animation_type,
            0
        )


    update_canvas()
    delay(0.1)

close_canvas()