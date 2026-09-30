from pico2d import *

open_canvas(800, 600)

character = load_image('fox_animation.png')

frame = 0
animation_type = 0     # 0 = 걷기, 1 = 뛰기, 2 = 점프, 3 = 공격


# 각 프레임의 실제 시작 X 위치
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


while True:
    clear_canvas()

    # 걷기
    if animation_type == 0:
        character.clip_draw(
            frame * 210, 595,
            210, 198,
            400, 300,
            210, 198
        )

        frame = (frame + 1) % 7

        if frame == 0:
            animation_type = 1


    # 뛰기 - 5프레임
    elif animation_type == 1:
        character.clip_draw(
            run_x[frame], 400,
            240, 160,
            400, 300,
            240, 160
        )

        frame = (frame + 1) % 5

        if frame == 0:
            animation_type = 2


    # 점프 - 10프레임
    elif animation_type == 2:
        character.clip_draw(
            jump_x[frame], 203,
            190, 190,
            400, 300,
            190, 190
        )

        frame = (frame + 1) % 10

        if frame == 0:
            animation_type = 3


    # 공격 - 7프레임
    elif animation_type == 3:
        character.clip_draw(
            attack_x[frame], 23,
            230, 180,
            400, 300,
            230, 180
        )

        frame = (frame + 1) % 7

        if frame == 0:
            animation_type = 0


    update_canvas()
    delay(0.1)

close_canvas()