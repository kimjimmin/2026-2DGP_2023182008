from pico2d import *

open_canvas(800, 600)

character = load_image('fox_animation.png')

while True:
    clear_canvas()

    # 첫 번째 여우 프레임을 잘라서 화면 중앙에 출력
    character.clip_draw(
        0, 580,        # 원본 이미지에서 시작 위치 x, y
        220, 180,      # 잘라낼 크기
        400, 300       # 화면에 출력할 위치 (정중앙)
    )

    update_canvas()
    delay(0.01)