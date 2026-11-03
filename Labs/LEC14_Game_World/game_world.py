
# 계층 구조를 가지는 게임 월드
world = [[],[],[]] # layers for game objects



#게임 월드에 객체를 담는 함수
def add_object(o, depth=0): #depth 0읜 배경, 1은 캐릭터
    world[depth].append(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return


def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

