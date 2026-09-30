from pico2d import *

open_canvas(800, 600)

character = load_image('fox_animation.png')

frame = 0
animation_type = 0

run_x = [
    20,
    275,
    528,
    781,
    1039
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

    # 뛰기
    elif animation_type == 1:
        character.clip_draw(
            run_x[frame], 395,
            250, 198,
            400, 300,
            250, 198
        )

        frame = (frame + 1) % 5

        if frame == 0:
            animation_type = 2

    # 점프
    elif animation_type == 2:
        character.clip_draw(
            frame * 198, 198,
            198, 198,
            400, 300,
            198, 198
        )

        frame = (frame + 1) % 10

        if frame == 0:
            animation_type = 3

    # 공격
    elif animation_type == 3:
        character.clip_draw(
            frame * 283, 0,
            283, 198,
            400, 300,
            283, 198
        )

        frame = (frame + 1) % 7

        if frame == 0:
            animation_type = 0

    update_canvas()
    delay(0.1)

close_canvas()