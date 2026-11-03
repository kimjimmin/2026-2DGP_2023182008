from math import pi
from pico2d import (
    SDL_KEYDOWN,
    SDL_KEYUP,
    SDLK_LEFT,
    SDLK_RIGHT,
    get_time,
    load_image,
)


class Idle:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.animation_time = get_time()
        boy.last_input_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        now = get_time()
        if now - boy.last_input_time >= 5.0:
            boy.change_state(Sleep)
            return

        if now - boy.animation_time >= 0.12:
            boy.frame = (boy.frame + 1) % 8
            boy.animation_time = now

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_draw(
                boy.frame * 100, 300, 100, 100, boy.x, boy.y
            )
        else:
            boy.image.clip_draw(
                boy.frame * 100, 200, 100, 100, boy.x, boy.y
            )


class Run:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.animation_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 4
        boy.x = max(50, min(750, boy.x))

        now = get_time()
        if now - boy.animation_time >= 0.08:
            boy.frame = (boy.frame + 1) % 8
            boy.animation_time = now

    @staticmethod
    def draw(boy):
        flip = '' if boy.face_dir == 1 else 'h'
        boy.run_image.clip_composite_draw(
            boy.frame * 100, 0, 100, 100,
            0, flip,
            boy.x, boy.y, 100, 100
        )


class Sleep:
    @staticmethod
    def enter(boy):
        boy.frame = 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        sprite_y = 300 if boy.face_dir == 1 else 200
        boy.image.clip_composite_draw(
            0, sprite_y, 100, 100,
            pi / 2, '',
            boy.x, boy.y - 20, 100, 100
        )


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.left_pressed = False
        self.right_pressed = False
        self.image = load_image('animation_sheet.png')
        self.run_image = load_image('run_animation.png')
        self.state = Idle
        self.last_input_time = get_time()
        self.animation_time = get_time()
        self.state.enter(self)

    def change_state(self, next_state):
        self.state.exit(self)
        self.state = next_state
        self.state.enter(self)

    def handle_event(self, event):
        self.last_input_time = get_time()

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.left_pressed = True
            elif event.key == SDLK_RIGHT:
                self.right_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.left_pressed = False
            elif event.key == SDLK_RIGHT:
                self.right_pressed = False

        self.dir = int(self.right_pressed) - int(self.left_pressed)

        if self.dir != 0:
            self.face_dir = 1 if self.dir > 0 else -1
            if self.state is not Run:
                self.change_state(Run)
        elif self.state is Run:
            self.change_state(Idle)
        elif self.state is Sleep:
            self.change_state(Idle)

    def update(self):
        self.state.do(self)

    def draw(self):
        self.state.draw(self)
