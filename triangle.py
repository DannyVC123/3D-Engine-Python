import pygame as pg
from math import *

class Triangle:
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