import pygame
from pygame.locals import *
from math import sqrt

from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

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

use_texture = False


def render_tetrahedron():
    glEnable(GL_TEXTURE_2D) if use_texture else glDisable(GL_TEXTURE_2D)
    for surface in mesh:
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(0, len(surface)):
            vertex_index = surface[i]
            glColor3fv(colors[vertex_index % 4])
            # Obliczenie wektorów normalnych
            v0 = vertices[surface[i]]
            v1 = vertices[surface[i - 1]]
            v2 = vertices[surface[i - 2]]
            normal = (
                ((v1[1] - v0[1]) * (v2[2] - v0[2]) - (v1[2] - v0[2]) * (v2[1] - v0[1])),
                ((v1[2] - v0[2]) * (v2[0] - v0[0]) - (v1[0] - v0[0]) * (v2[2] - v0[2])),
                ((v1[0] - v0[0]) * (v2[1] - v0[1]) - (v1[1] - v0[1]) * (v2[0] - v0[0]))
            )
            glNormal3fv(normal)

            glTexCoord2f(vertices[vertex_index][0], vertices[vertex_index][1])
            glVertex3fv(vertices[vertex_index])
        glEnd()


def generate_tetrahedron_mesh(n):
    if n == 1:
        return

    generate_tetrahedron_mesh(n - 1)
    mesh.clear()
    number_of_tetrahedron_vertices = 4
    base_vertices = vertices.copy()
    max_first_vertex = 4 ** (n-1)  #potęgowanie

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
    # Materiał obiektu

    # Światło punktowe
    glLight(GL_LIGHT0, GL_POSITION, (0, 0, 1, 1))  # źródło światła punktowego
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.6, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)

    # Światło kierunkowe
    glLight(GL_LIGHT1, GL_POSITION, (0, 0, 100, 0.0))  # źródło światła kierunkowego
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.01, 0.01, 0.01, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1.0, 1.0, 1.0, 0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (1.0, 1.0, 1.0, 0))
    glEnable(GL_LIGHT1)
    #glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


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


def texture():
    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("D1_t.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
        image.tobytes("raw", "RGB", 0, -1)
    )


def main():
    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)  # właczna gładkie cieniowanie
    texture()
    generate_tetrahedron_mesh(4)

    #light()

    fovy = 45
    eye_x = 0
    eye_y = -1
    center_x = 0
    center_y = 0
    k_pressed = False
    w_pressed = False
    directional_light_use = False
    spot_ligh_use = False

    while True:
        camera_view(fovy, eye_x, eye_y, center_x, center_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    fovy -= 2

                elif event.key == pygame.K_x:
                    fovy += 2

                elif event.key == pygame.K_k:
                    k_pressed = True
                    w_pressed = False

                elif event.key == pygame.K_w:
                    w_pressed = True
                    k_pressed = False

                elif event.key == pygame.K_t:
                    global use_texture
                    use_texture = not use_texture  # Zmiana stanu tekstury

                elif event.key == pygame.K_d:
                    directional_light_use = not directional_light_use
                elif event.key == pygame.K_s:
                    spot_ligh_use = not spot_ligh_use

                #zmiana pozycji kamery
                if k_pressed:
                    if event.key == pygame.K_LEFT:
                        eye_x += 0.2

                    elif event.key == pygame.K_RIGHT:
                        eye_x -= 0.2

                    elif event.key == pygame.K_UP:
                        eye_y += 0.2

                    elif event.key == pygame.K_DOWN:
                        eye_y -= 0.2

                #zmiana pozycji widoku
                if w_pressed:
                    if event.key == pygame.K_LEFT:
                        center_x -= 0.2

                    elif event.key == pygame.K_RIGHT:
                        center_x += 0.2

                    elif event.key == pygame.K_UP:
                        center_y -= 0.2

                    elif event.key == pygame.K_DOWN:
                        center_y += 0.2

            camera_view(fovy, eye_x, eye_y, center_x, center_y)

        if spot_ligh_use:
            glEnable(GL_LIGHT0)
        else: glDisable(GL_LIGHT0)

        if directional_light_use:
            glEnable(GL_LIGHT1)
        else: glDisable(GL_LIGHT1)

        # obiekt
        glMatrixMode(GL_MODELVIEW)
        glRotatef(1, 0, 0, 1)       # obrót o 1 stopień względem wektora [0, 0, 1]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        render_tetrahedron()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()