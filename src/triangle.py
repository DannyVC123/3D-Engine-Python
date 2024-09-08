import pygame as pg
from math import *
import copy

from lin_alg import Lin_Alg

class Triangle:
    @staticmethod
    def triangulate(two_d_vertices, face):
        triangles = []
        
        vertices_left = face.copy()
        while len(vertices_left) > 3:
            num_vertices_left = len(vertices_left)
            selected_vertex = None
            for i in range(num_vertices_left):
                # print(i)
                curr_vertex = two_d_vertices[vertices_left[i]]

                left_ind = (i + 1) % num_vertices_left
                left_vertex = two_d_vertices[face[left_ind]]
                left_vector  = [(left_vertex[j]  - curr_vertex[j]) for j in range(2)]

                right_ind = (i - 1 + num_vertices_left) % num_vertices_left
                right_vertex = two_d_vertices[face[right_ind]]
                right_vector = [(right_vertex[j] - curr_vertex[j]) for j in range(2)]

                # print(left_ind, right_ind)

                cross_product = Lin_Alg.get_2d_determinant([left_vector, right_vector])
                # print(cross_product)
                if cross_product < 0:
                    continue
                
                valid_ear = True
                for j in range(num_vertices_left):
                    if j == i or j == left_ind or j == right_ind:
                        continue

                    test_vertex = two_d_vertices[vertices_left[j]]
                    test_vector = [test_vertex[k] - curr_vertex[k] for k in range(2)]
                    cross_product = Lin_Alg.get_2d_determinant([right_vector, test_vector])
                    right_test_cross = Lin_Alg.get_2d_determinant([test_vector, right_vector])
                    if cross_product > 0:
                        valid_ear = False
                
                if not valid_ear:
                    continue
                triangles.append([i, left_ind, right_ind])
                selected_vertex = i
                break
            vertices_left.remove(selected_vertex)
            
        triangles.append(vertices_left)
        return triangles
    
    @staticmethod
    def draw(window, two_d_vertices, color):
        pixel_array = pg.PixelArray(window)
        w, h, = window.get_size()
        
        ordered_vertices = sorted(two_d_vertices, key = lambda vertex: vertex[1])

        if ordered_vertices[0][1] == ordered_vertices[1][1]: # top
            Triangle.draw_flat_triangle(pixel_array, w, h, ordered_vertices[:2], ordered_vertices[2],  1, tuple(color))
        elif ordered_vertices[1][1] == ordered_vertices[2][1]: # bottom
            Triangle.draw_flat_triangle(pixel_array, w, h, ordered_vertices[1:], ordered_vertices[0], -1, tuple(color))
        else:
            triangle1, triangle2 = Triangle.split_triangle(ordered_vertices)
            Triangle.draw_flat_triangle(pixel_array, w, h, triangle1[:2], triangle1[2],  -1, tuple(color))
            Triangle.draw_flat_triangle(pixel_array, w, h, triangle2[:2], triangle2[2],  1, tuple(color))
        
        del pixel_array

    @staticmethod
    def draw_flat_triangle(pixel_array, w, h, flat_vertices, outlier_vertex, stride, color):
        ordered_flat_vertices = sorted(flat_vertices, key = lambda vertex: vertex[0])

        try:
            m_inv_left  = Triangle.get_slope_inv(ordered_flat_vertices[0], outlier_vertex)
            m_inv_right = Triangle.get_slope_inv(ordered_flat_vertices[1], outlier_vertex)
        except ZeroDivisionError:
            print('ERROR')
            print(flat_vertices, outlier_vertex)

        start_y, end_y = int(round(flat_vertices[0][1])), int(round(outlier_vertex[1]))
        for y in range(start_y, end_y, stride):
            start_x = m_inv_left  * (y - ordered_flat_vertices[0][1]) + ordered_flat_vertices[0][0]
            end_x   = m_inv_right * (y - ordered_flat_vertices[1][1]) + ordered_flat_vertices[1][0]
            start_x, end_x = int(ceil(start_x)), int(ceil(end_x))
            
            # pg.draw.line(window, color, [start_x, y], [end_x, y])
            # unberably slow
            for x in range(start_x, end_x + 1):
                if 0 <= x < w and 0 <= y < h:
                    pixel_array[x, y] = color
    
    @staticmethod
    def split_triangle(vertices):
        x_middle, y_middle = vertices[1]
        m_inv = Triangle.get_slope_inv(vertices[0], vertices[2])

        x_other = int(round(m_inv * (y_middle - vertices[0][1]) + vertices[0][0]))
        return (
            [vertices[1], [x_other, int(round(y_middle))], vertices[0]],
            [vertices[1], [x_other, int(round(y_middle))], vertices[2]]
        )

    @staticmethod
    def get_slope_inv(p0, p1):
        return (p1[0] - p0[0]) / (p1[1] - p0[1])