from random import choice
from turtle import *
from freegames import floor, vector

# --- Estado del juego ---
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)

# Fantasmas más rápidos (antes era 5)
ghosts = [
    [vector(-180, 160),  vector(10, 0)],    
    [vector(-180, -160), vector(0, 10)],    
    [vector(100, 160),   vector(0, -10)],   
    [vector(100, -160),  vector(-10, 0)],   
]

# ✅ Nuevo tablero custom (más pasillos y zonas abiertas)
tiles = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,
    0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,0,
    0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,
    0,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,
    0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,
    0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,
    0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,
    0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,
    0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,
    0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,0,
    0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,
    0,1,0,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,
    0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,
    0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,
    0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,
    0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,
    0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

# ✅ --------------- TU lógica de IA VA AQUÍ SIN CAMBIOS ----------------
# (pegamos exactamente la IA inteligente que tú ya tienes)
# ----------------------------------------------------------------------

# Utilidades del juego
def square(x, y):
    path.up(); path.goto(x, y); path.down(); path.begin_fill()
    for _ in range(4): path.forward(20); path.left(90)
    path.end_fill()

def offset(point):
    x = (floor(point.x, 20) + 200)/20
    y = (180 - floor(point.y, 20))/20
    return int(x + y*20)

def valid(point):
    index = offset(point)
    if tiles[index] == 0: return False
    index = offset(point + vector(19,0))
    if tiles[index] == 0: return False
    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    bgcolor('black')
    path.color('blue')
    for index, tile in enumerate(tiles):
        if tile > 0:
            x = (index % 20)*20 - 200
            y = 180 - (index//20)*20
            square(x,y)
            if tile == 1:
                path.up(); path.goto(x+10, y+10)
                path.dot(2, 'white')

# -------------------- IA DE FANTASMAS QUE YA EXISTE --------------------
# (Tu misma IA que ya funcionaba — no la repito por espacio)
# Sólo pega aquí los métodos move_towards_pacman, move_to_intercept, etc.

# -------------------- Movimiento y controles ---------------------------
def move():
    writer.undo(); writer.write(state['score'])
    clear()

    if valid(pacman + aim): pacman.move(aim)
    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2; state['score'] += 1
        x = (index % 20)*20 - 200
        y = 180 - (index//20)*20
        square(x,y)

    up(); goto(pacman.x+10, pacman.y+10); dot(20,'yellow')

    for ghost in ghosts:
        point, course = ghost
        # IA fantasma se queda igual
        if ghosts.index(ghost) == 0: move_towards_pacman(ghost)
        elif ghosts.index(ghost) == 1: move_to_intercept(ghost)
        elif ghosts.index(ghost) == 2: move_random_smart(ghost)
        else: move_strategic(ghost)

        point.move(ghost[1])

        if abs(pacman - point) < 20: update(); return
        up(); goto(point.x+10, point.y+10); dot(20, 'red')

    update()
    ontimer(move, 80)  # un poquito más rápido aún

def change(x,y):
    if valid(pacman + vector(x,y)):
        aim.x, aim.y = x, y

setup(420,420,370,0)
hideturtle(); tracer(False)
writer.goto(160,160); writer.color('white'); writer.write(state['score'])
listen()

onkey(lambda: change(5,0), 'Right')
onkey(lambda: change(-5,0), 'Left')
onkey(lambda: change(0,5), 'Up')
onkey(lambda: change(0,-5), 'Down')

world()
move()
done()
