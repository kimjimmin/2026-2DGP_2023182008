"""소닉 스프라이트 애니메이션 뷰어."""

import pico2d
from pathlib import Path
from dataclasses import dataclass
from time import monotonic

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CENTER = (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 300
REPEAT_COUNT = 5
WAIT_SECONDS = 1.0
DEV_INSPECT = False
dev_frame = 0
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


@dataclass(frozen=True)
class Animation:
    id: str
    name: str
    frames: tuple
    frame_seconds: float = 0.1


# 프레임은 원본 왼쪽 위 기준 (left, top, width, height).
ANIMATIONS = (
    Animation('idle', '대기', (
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
        (86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38),
        (182, 40, 29, 38),
    )),
    Animation('look_up', '위 보기', ((211, 39, 29, 38), (240, 39, 29, 38))),
    # 단독 포즈는 관찰 시간을 확보하고, 공 형태는 한 프레임으로 도약한다.
    Animation('crouch', '웅크리기', ((270, 45, 24, 32),), 0.25),
    Animation('curl', '몸 말기', ((302, 51, 29, 26),), 0.25),
    Animation('walk', '걷기', (
        (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
        (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
        (206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
        (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
    )),
    Animation('jog', '빠른 걷기', (
        (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
    )),
    Animation('dash', '질주', (
        (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
    )),
    Animation('spin', '공중 회전', (
        (1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29),
        (98, 169, 31, 29), (131, 168, 29, 30), (162, 168, 29, 31),
        (193, 170, 30, 29), (230, 170, 31, 29),
    )),
    Animation('jump_ball', '공 형태 도약', ((268, 170, 30, 30),), 0.6),
    Animation('rolling_ball', '공 형태 구르기', (
        (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
        (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
    )),
    Animation('run', '달리기', (
        (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
        (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
    )),
    Animation('fast_run', '고속 달리기', (
        (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
        (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
    )),
    Animation('turn', '몸 방향 회전', (
        (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
        (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
    )),
    Animation('hurt', '뒤로 튕기기', ((184, 341, 40, 28), (232, 341, 39, 27)), 0.2),
    Animation('brake', '제동', (
        (1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
        (99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 36),
        (217, 379, 33, 36), (254, 378, 33, 36),
    )),
    Animation('fall', '공중 자세', ((6, 429, 34, 40), (49, 426, 34, 43)), 0.25),
    Animation('stand', '서 있기', ((96, 427, 23, 39), (125, 427, 23, 39)), 0.2),
)


@dataclass
class Player:
    animations: tuple = ANIMATIONS
    animation_index: int = 0
    frame_index: int = 0
    elapsed: float = 0.0
    completed: int = 0
    started: float = 0.0
    state: str = 'playing'
    wait_started: float = 0.0

    @property
    def animation(self):
        return self.animations[self.animation_index]

    def update(self, now):
        if self.state == 'waiting':
            if now - self.wait_started >= WAIT_SECONDS:
                self.animation_index = (self.animation_index + 1) % len(self.animations)
                self.started = now
                self.elapsed = 0.0
                self.completed = 0
                self.frame_index = 0
                self.state = 'playing'
            return
        self.elapsed = max(0.0, now - self.started)
        duration = len(self.animation.frames) * self.animation.frame_seconds
        self.completed = int(self.elapsed / duration)
        if self.completed >= REPEAT_COUNT:
            self.completed = REPEAT_COUNT
            self.elapsed = duration * REPEAT_COUNT
            self.frame_index = len(self.animation.frames) - 1
            self.state = 'waiting'
            self.wait_started = now
            return
        self.frame_index = (int(self.elapsed / self.animation.frame_seconds)
                            % len(self.animation.frames))


def draw_frame(sprite, animation, frame_index, position=CENTER):
    left, top, width, height = animation.frames[frame_index]
    bottom = sprite.h - top - height
    sprite.clip_draw(left, bottom, width, height,
                     *position, DISPLAY_WIDTH, DISPLAY_HEIGHT)


def load_sprite(path=SPRITE_PATH):
    if not path.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {path}')
    try:
        return pico2d.load_image(str(path))
    except Exception as error:
        raise RuntimeError(f'스프라이트 로딩 실패: {path}: {error}') from error


def handle_events():
    global dev_frame
    for event in pico2d.get_events():
        if event.type == pico2d.SDL_QUIT:
            return False
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
        if DEV_INSPECT and event.type == pico2d.SDL_KEYDOWN:
            if event.key == pico2d.SDLK_RIGHT:
                dev_frame = (dev_frame + 1) % len(ANIMATIONS[0].frames)
    return True


def main(frame_limit=None):
    """뷰어를 실행한다."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        # 기본 회색 배경에서 파란 몸체·흰 장갑을 구분한다.
        pico2d.hide_lattice()
        sprite = load_sprite()
        player = Player(started=monotonic())
        drawn = 0
        while frame_limit is None or drawn < frame_limit:
            if not handle_events():
                break
            player.update(monotonic())
            pico2d.clear_canvas()
            index = dev_frame if DEV_INSPECT else player.frame_index
            draw_frame(sprite, player.animation, index)
            pico2d.update_canvas()
            pico2d.delay(0.01)
            drawn += 1
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
