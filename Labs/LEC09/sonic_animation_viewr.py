"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


def main():
    """뷰어를 실행한다."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
