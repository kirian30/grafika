import pygame
from pygame.locals import *
from math import sqrt

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = [
    [-0.5, -sqrt(3)/6, 0],
    [0, sqrt(3)/3, 0],
    [0.5, -sqrt(3)/6, 0],
    [0, 0, -sqrt(6)/3]
]

mesh = [
    [0, 1, 2, 3, 0, 1]
]

colors = [
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [1, 1, 1]
]

def renderTetrahedron():
    for surface in mesh:
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(0, len(surface)):
            vertex_index = surface[i]
            glColor3fv(colors[vertex_index%4])
            glVertex3fv(vertices[vertex_index])
        glEnd()


def generateTetrahedronMesh(n):
    if n == 1:
        return

    generateTetrahedronMesh(n - 1)
    mesh.clear()
    number_of_tetrahedron_vertices = 4
    base_vertices = vertices.copy()
    max_first_vertex = 4 ** (n-1)

    # tworzenie listy wierzchołków po 4 wierzcholki dla kazdego nowego czworoscianu
    for first_vertex in range(0, max_first_vertex, 4):
        for i in range(number_of_tetrahedron_vertices):
            for j in range(number_of_tetrahedron_vertices):
                if i != j:
                    new_vertex = [(base_vertices[i + first_vertex][0] + base_vertices[j + first_vertex][0]) / 2,
                                  (base_vertices[i + first_vertex][1] + base_vertices[j + first_vertex][1]) / 2,
                                  (base_vertices[i + first_vertex][2] + base_vertices[j + first_vertex][2]) / 2]
                    vertices.insert(4 * i + j + 4 * first_vertex, new_vertex)

    # tworzenie siatek tych czworoscianow
    for i in range(0, max_first_vertex):
        mesh.append([4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3, 4 * i, 4 * i + 1])


def light():
    glLight(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 0)) # źródło światła left, top, front

    # Ustawienie koloru światła otoczenia
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 0.0, 0.0, 1.0))

    # Ustawienie koloru światła rozproszonego
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))

    # Ustawienie koloru światła wypukłego
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 1.0, 0.0, 1.0))
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


def camera_view(fovy, eye_x, eye_y, center_x, center_y):
    display = (1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, (display[0] / display[1]), 0.1, 50)
    gluLookAt(
        eye_x, eye_y, -2,  # położenie kamery
        center_x, center_y, 0,  # punkt, na który patrzy kamera
        0, 1, 0  # wektor wskazujący gdzie jest góra kamery
    )


def main():
    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)
    generateTetrahedronMesh(3)

    fovy = 45
    eye_x = 0
    eye_y = -1
    center_x = 0
    center_y = 0
    last_pressed_key = pygame.K_SPACE

    while True:
        camera_view(fovy, eye_x, eye_y, center_x, center_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    last_pressed_key = pygame.K_z
                    fovy -= 2

                elif event.key == pygame.K_x:
                    last_pressed_key = pygame.K_x
                    fovy += 2

                elif event.key == pygame.K_k:
                    last_pressed_key = pygame.K_k

                #zmiana pozycji kamery
                if last_pressed_key == pygame.K_k:
                    if event.key == pygame.K_LEFT:
                        last_pressed_key = pygame.K_LEFT
                        eye_x += 0.2

                    elif event.key == pygame.K_RIGHT:
                        last_pressed_key = pygame.K_RIGHT
                        eye_x -= 0.2

                    elif event.key == pygame.K_UP:
                        last_pressed_key = pygame.K_UP
                        eye_y += 0.2

                    elif event.key == pygame.K_DOWN:
                        last_pressed_key = pygame.K_DOWN
                        eye_y -= 0.2

                #zmiana punktu, na który patrzy kamera
                elif event.key == pygame.K_LEFT:
                    last_pressed_key = pygame.K_LEFT
                    center_x -= 0.2

                elif event.key == pygame.K_RIGHT:
                    last_pressed_key = pygame.K_RIGHT
                    center_x += 0.2

                elif event.key == pygame.K_UP:
                    last_pressed_key = pygame.K_UP
                    center_y -= 0.2

                elif event.key == pygame.K_DOWN:
                    last_pressed_key = pygame.K_DOWN
                    center_y += 0.2

            camera_view(fovy, eye_x, eye_y, center_x, center_y)

        # obiekt
        glMatrixMode(GL_MODELVIEW)
        glRotatef(1, 0, 0, 1)       # obrót o 1 stopień względem wektora [0, 0, 1]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        renderTetrahedron()
        #light()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()