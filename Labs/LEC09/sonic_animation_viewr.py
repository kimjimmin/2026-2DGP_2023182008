"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
from dataclasses import dataclass

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CENTER = (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 300
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


@dataclass(frozen=True)
class Animation:
    id: str
    name: str
    frames: tuple
    frame_seconds: float = 0.1


# 프레임은 원본 왼쪽 위 기준 (left, top, width, height).
ANIMATIONS = (
    Animation('idle', '대기', ((1, 39, 29, 39),)),
)


def draw_frame(sprite, animation, frame_index):
    left, top, width, height = animation.frames[frame_index]
    bottom = sprite.h - top - height
    sprite.clip_draw(left, bottom, width, height,
                     *CENTER, DISPLAY_WIDTH, DISPLAY_HEIGHT)


def load_sprite(path=SPRITE_PATH):
    if not path.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {path}')
    try:
        return pico2d.load_image(str(path))
    except Exception as error:
        raise RuntimeError(f'스프라이트 로딩 실패: {path}: {error}') from error


def handle_events():
    for event in pico2d.get_events():
        if event.type == pico2d.SDL_QUIT:
            return False
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
    return True


def main(frame_limit=None):
    """뷰어를 실행한다."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite = load_sprite()
        drawn = 0
        while frame_limit is None or drawn < frame_limit:
            if not handle_events():
                break
            pico2d.clear_canvas()
            draw_frame(sprite, ANIMATIONS[0], 0)
            pico2d.update_canvas()
            pico2d.delay(0.01)
            drawn += 1
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
