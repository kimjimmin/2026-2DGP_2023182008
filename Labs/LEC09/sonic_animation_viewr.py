"""소닉 스프라이트 애니메이션 뷰어."""

from dataclasses import dataclass
from math import sin, pi, isfinite
from pathlib import Path
import sys
from time import monotonic

import pico2d

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CENTER = (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 300
SCREEN_MARGIN = 24
REPEAT_COUNT = 5
WAIT_SECONDS = 1.0
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


def display_bounds(position):
    """그리기 크기와 동일한 사각형으로 이동 경계도 검사한다."""
    x, y = position
    return (x - DISPLAY_WIDTH / 2, y - DISPLAY_HEIGHT / 2,
            x + DISPLAY_WIDTH / 2, y + DISPLAY_HEIGHT / 2)


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


# (이동 유형, 5회 재생 전체의 수평 이동 거리, 1회 도약 높이)
MOTIONS = {
    'idle': ('still', 0, 0), 'look_up': ('still', 0, 0),
    'crouch': ('still', 0, 0), 'curl': ('still', 0, 0),
    'walk': ('linear', 120, 0), 'jog': ('linear', 140, 0),
    'dash': ('linear', 180, 0), 'spin': ('hop', 0, 90),
    'jump_ball': ('hop', 0, 110), 'rolling_ball': ('linear', 160, 0),
    'run': ('linear', 180, 0), 'fast_run': ('linear', 220, 0),
    'turn': ('still', 0, 0), 'hurt': ('hop', -90, 60),
    'brake': ('brake', 140, 0), 'fall': ('hop', 0, 80),
    'stand': ('still', 0, 0),
}


def position_at(animation, elapsed):
    """프레임 재생과 같은 경과 시간으로 연속적인 화면 좌표를 구한다."""
    kind, distance, height = MOTIONS[animation.id]
    cycle = len(animation.frames) * animation.frame_seconds
    total = cycle * REPEAT_COUNT
    elapsed = max(0.0, min(elapsed, total))
    progress = elapsed / total
    if kind == 'brake':
        progress = 1 - (1 - progress) ** 2
    x = CENTER[0] + distance * progress
    y = CENTER[1]
    if kind == 'hop' and elapsed < total:
        phase = (elapsed % cycle) / cycle
        y += height * sin(pi * phase)
    return x, y


def check_motion_bounds(animation):
    """지원하는 경로의 극값을 검사한다. 경계에서 위치를 강제로 멈추지 않는다."""
    kind, distance, height = MOTIONS[animation.id]
    for x in (CENTER[0], CENTER[0] + distance):
        for y in (CENTER[1], CENTER[1] + height):
            left, bottom, right, top = display_bounds((x, y))
            if (left < SCREEN_MARGIN or bottom < SCREEN_MARGIN
                    or right > CANVAS_WIDTH - SCREEN_MARGIN
                    or top > CANVAS_HEIGHT - SCREEN_MARGIN):
                raise ValueError(f'{animation.id}: 이동 경로가 화면 여백을 벗어납니다.')


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

    @property
    def position(self):
        return position_at(self.animation, self.elapsed)

    def begin_next(self, now):
        """다음 동작은 공통 시작 위치에서 첫 프레임부터 재생한다."""
        self.animation_index = (self.animation_index + 1) % len(self.animations)
        self.started = now
        self.elapsed = 0.0
        self.completed = 0
        self.frame_index = 0
        self.wait_started = 0.0
        self.state = 'playing'

    def update(self, now):
        if self.state == 'waiting':
            if now >= self.wait_started + WAIT_SECONDS:
                self.begin_next(now)
            return
        self.elapsed = max(0.0, now - self.started)
        duration = len(self.animation.frames) * self.animation.frame_seconds
        # 0.7 / 0.1 등이 정수 경계 직전으로 계산되는 부동소수점 오차 보정.
        frame_number = int((self.elapsed + 1e-9) / self.animation.frame_seconds)
        self.completed = frame_number // len(self.animation.frames)
        if self.completed >= REPEAT_COUNT:
            self.completed = REPEAT_COUNT
            self.elapsed = duration * REPEAT_COUNT
            self.frame_index = len(self.animation.frames) - 1
            self.state = 'waiting'
            self.wait_started = now
            return
        self.frame_index = frame_number % len(self.animation.frames)


def draw_frame(sprite, animation, frame_index, position=CENTER):
    left, top, width, height = animation.frames[frame_index]
    bottom = sprite.h - top - height
    sprite.clip_draw(left, bottom, width, height,
                     *position, DISPLAY_WIDTH, DISPLAY_HEIGHT)


def validate_animations(animations, image_width, image_height):
    if not animations:
        raise ValueError('재생할 동작 목록이 비어 있습니다.')
    seen = set()
    for animation in animations:
        label = animation.id
        if not label or label in seen:
            raise ValueError(f'{label}: 동작 ID가 비어 있거나 중복됩니다.')
        seen.add(label)
        if not animation.frames:
            raise ValueError(f'{label}: 프레임 목록이 비어 있습니다.')
        seconds = animation.frame_seconds
        if not isinstance(seconds, (int, float)) or not isfinite(seconds) or seconds <= 0:
            raise ValueError(f'{label}: 프레임 시간은 유한한 양수여야 합니다.')
        for index, frame in enumerate(animation.frames):
            if len(frame) != 4 or any(type(value) is not int for value in frame):
                raise ValueError(f'{label} 프레임 {index}: 정수 좌표 4개가 필요합니다.')
            left, top, width, height = frame
            if (min(left, top) < 0 or min(width, height) <= 0
                    or left + width > image_width or top + height > image_height):
                raise ValueError(f'{label} 프레임 {index}: 이미지 영역을 벗어난 좌표 {frame}')
        if label not in MOTIONS:
            raise ValueError(f'{label}: 이동 정보가 없습니다.')
        kind, distance, height = MOTIONS[label]
        if kind not in ('still', 'linear', 'hop', 'brake'):
            raise ValueError(f'{label}: 알 수 없는 이동 유형 {kind}')
        if any(not isinstance(v, (int, float)) or not isfinite(v) for v in (distance, height)):
            raise ValueError(f'{label}: 이동 값은 유한한 수여야 합니다.')
        if height < 0 or (kind != 'hop' and height != 0) or (kind == 'still' and distance != 0):
            raise ValueError(f'{label}: 이동 유형과 거리·높이가 일치하지 않습니다.')
        check_motion_bounds(animation)


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
        # 기본 회색 배경에서 파란 몸체·흰 장갑을 구분한다.
        pico2d.hide_lattice()
        sprite = load_sprite()
        validate_animations(ANIMATIONS, sprite.w, sprite.h)
        player = Player(started=monotonic())
        drawn = 0
        while frame_limit is None or drawn < frame_limit:
            if not handle_events():
                break
            player.update(monotonic())
            pico2d.clear_canvas()
            draw_frame(sprite, player.animation, player.frame_index, player.position)
            pico2d.update_canvas()
            pico2d.delay(0.01)
            drawn += 1
    except (OSError, RuntimeError, ValueError) as error:
        print(f'소닉 뷰어 오류: {error}', file=sys.stderr)
        return 1
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
