from math import *
from random import *

from lin_alg import Lin_Alg
from model import Model
from soccer_ball import Soccer_Ball

class Model_Lib:
    @staticmethod
    def cube():
        # https://commons.wikimedia.org/wiki/File:Labeled_cube_graph.png
        vertices = [
            [-200,  200,  200], # 0
            [-200,  200, -200], # 1
            [ 200,  200, -200], # 2
            [ 200,  200,  200], # 3
            [-200, -200,  200], # 4
            [-200, -200, -200], # 5
            [ 200, -200, -200], # 6
            [ 200, -200,  200], # 7
        ]
        
        faces = [
            [1, 0, 3, 2], # top
            [4, 5, 6, 7], # bottom
            [0, 4, 7, 3], # front
            [2, 6, 5, 1], # back
            [1, 5, 4, 0], # left
            [3, 7, 6, 2]  # right
        ]
        '''
        faces = [
            [1,0,2], # top
            [2,0,3],
            [4,5,7], # bottom
            [7,5,6],
            [0,4,3], # front
            [3,4,7],
            [2,6,1], # back
            [1,6,5],
            [1,5,0], # left
            [0,5,4],
            [3,7,2], # right
            [2,7,6]
        ]
        '''
        unit_normals = []
        for face in faces:
            vec1 = [vertices[face[1]][i] - vertices[face[0]][i] for i in range(3)]
            vec2 = [vertices[face[2]][i] - vertices[face[1]][i] for i in range(3)]

            normal = Lin_Alg.cross_product(vec1, vec2)
            unit_normal = Lin_Alg.get_unit_vector(normal)
            print(unit_normal)

            unit_normals.append(unit_normal)

        return Model(vertices, faces, unit_normals)
    
    @staticmethod
    def n_gon_pyramid(n, radius = 200, colors = None):
        if n < 3:
            raise ValueError('n must be at least 3')
        
        y = -radius
        vertices = [
            [0, radius, 0], # point
            [radius, y, 0], # first base point
        ]
        faces = []

        slice_angle = 2 * pi / n
        base = [1]
        for i in range(1, n):
            theta = i * slice_angle
            x = radius * cos(theta)
            z = radius * sin(theta)
            vertices.append([x, y, z])

            faces.append([i, i + 1, 0]) # side
            base.append(i + 1)
        
        faces.append([n, 1, 0]) # last side
        faces.append(base)

        return Model(vertices, faces, colors)

    @staticmethod
    def cone():
        n = 72

        side_color = [randint(0, 255) for _ in range(3)]
        base_color = [randint(0, 255) for _ in range(3)]
        
        colors = [side_color] * n
        colors.append(base_color)
        
        cone = Model_Lib.n_gon_pyramid(n, colors = colors)
        return cone

    @staticmethod
    def soccer_ball(edge_length = 100):
        vertices, faces, unit_normals, colors = Soccer_Ball.create_ball(edge_length)
        return Model(vertices, faces, unit_normals, colors)