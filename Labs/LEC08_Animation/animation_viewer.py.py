from pico2d import *

open_canvas(800, 600)

character = load_image('fox_animation.png')

frame = 0

while True:
    clear_canvas()

    character.clip_draw(
        frame * 210, 595,   # 현재 걷기 프레임의 시작 위치
        210, 198,           # 한 프레임 영역 크기
        400, 300,           # 화면 중앙
        210, 198            # 출력 크기
    )

    update_canvas()

    frame = (frame + 1) % 7

    delay(0.1)

close_canvas()

