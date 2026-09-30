from pico2d import *

open_canvas(800, 600)

character = load_image('fox_animation.png')

frame = 0
animation_type = 0     # 0 = 걷기, 1 = 뛰기

while True:
    clear_canvas()

    # 걷기
    if animation_type == 0:
        character.clip_draw(
            frame * 210, 595,   # 현재 걷기 프레임의 시작 위치
            210, 198,           # 한 프레임 영역 크기
            400, 300,           # 화면 중앙
            210, 198            # 출력 크기
        )

        frame = (frame + 1) % 7

        # 걷기 한 사이클이 끝나면 뛰기로
        if frame == 0:
            animation_type = 1


    # 뛰기
    elif animation_type == 1:
        character.clip_draw(
            frame * 250, 395,
            250, 198,
            400, 300,
            250, 198
        )

        frame = (frame + 1) % 5

        # 뛰기 한 사이클이 끝나면 다시 걷기로
        if frame == 0:
            animation_type = 0


    update_canvas()
    delay(0.1)

close_canvas()

