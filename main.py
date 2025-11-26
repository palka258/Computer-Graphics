from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

width, height = 800, 600
step = 10
rotate_speed = 5

# Объекты
objects = [
    {"type": "circle", "pos": [150, 300], "radius": 60, "angle": 0, "selected": False},
    {"type": "polygon", "pos": [400, 300], "sides": 9, "radius": 60, "angle": 0, "selected": False},
    {"type": "polygon", "pos": [650, 300], "sides": 10, "radius": 50, "angle": 0, "selected": False},
]

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

def draw_object(obj):
    glPushMatrix()
    glTranslatef(obj["pos"][0], obj["pos"][1], 0)
    glRotatef(obj["angle"], 0, 0, 1)
    glTranslatef(-obj["pos"][0], -obj["pos"][1], 0)

    # Цвет выделенного объекта
    if obj["selected"]:
        glColor3f(0.1, 0.8, 0.1)  # Зеленый
    else:
        glColor3f(0.2, 0.4, 0.8)  # Синий

    if obj["type"] == "circle":
        glBegin(GL_LINE_LOOP)
        segments = 50
        for i in range(segments):
            theta = 2.0 * math.pi * i / segments
            x = obj["radius"] * math.cos(theta) + obj["pos"][0]
            y = obj["radius"] * math.sin(theta) + obj["pos"][1]
            glVertex2f(x, y)
        glEnd()
    elif obj["type"] == "polygon":
        glBegin(GL_LINE_LOOP)
        for i in range(obj["sides"]):
            theta = 2.0 * math.pi * i / obj["sides"]
            x = obj["radius"] * math.cos(theta) + obj["pos"][0]
            y = obj["radius"] * math.sin(theta) + obj["pos"][1]
            glVertex2f(x, y)
        glEnd()
    glPopMatrix()

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    for obj in objects:
        draw_object(obj)
    glutSwapBuffers()

# Перемещение выбранного объекта
def keyboard(key, x, y):
    key = key.decode("utf-8")
    for obj in objects:
        if obj["selected"]:
            if key == "w":
                obj["pos"][1] += step
            elif key == "s":
                obj["pos"][1] -= step
            elif key == "a":
                obj["pos"][0] -= step
            elif key == "d":
                obj["pos"][0] += step
    glutPostRedisplay()

# Вращение выбранного объекта
def special_keys(key, x, y):
    for obj in objects:
        if obj["selected"]:
            if key == GLUT_KEY_LEFT:
                obj["angle"] += rotate_speed
            elif key == GLUT_KEY_RIGHT:
                obj["angle"] -= rotate_speed
    glutPostRedisplay()

# Выбор объекта мышью
def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Переводим координаты GLUT в OpenGL
        y = height - y
        for obj in objects:
            dx = x - obj["pos"][0]
            dy = y - obj["pos"][1]
            dist = math.sqrt(dx**2 + dy**2)
            if obj["type"] == "circle" and dist <= obj["radius"]:
                select_object(obj)
            elif obj["type"] == "polygon" and dist <= obj["radius"]:
                select_object(obj)

def select_object(obj):
    for o in objects:
        o["selected"] = False
    obj["selected"] = True
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"2D Objects with Selection")
    init()
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutMainLoop()

if __name__ == "__main__":
    main()
