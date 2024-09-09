import pygame as pg
from math import *
import copy
from random import *

from lin_alg import Lin_Alg
from triangle import Triangle

class Model:
    X, Y, Z = 0, 1, 2

    light_direc = [0, 0, -1]
    # light_direc = Lin_Alg.get_unit_vector([-1, -1, -1])
    intensities = [1, 1, 1]

    def __init__(self, vertices, faces, unit_normals, colors = None):
        self.vertices = vertices
        self.rotated_vertices = copy.deepcopy(vertices)

        self.faces = faces
        self.unit_normals = unit_normals
        self.rotated_unit_normals = copy.deepcopy(unit_normals)

        if colors is None:
            self.colors = []
            for _ in range(len(faces)):
                color = [randint(0, 255) for _ in range(3)]
                self.colors.append(color)
        elif isinstance(colors[0], int):
            self.colors = []
            self.colors = [colors.copy() for _ in range(len(faces))]
        else:
            self.colors = colors
        self.shaded_colors = copy.deepcopy(self.colors)
    
    # Rotation
    def simple_rotate(self, axis, theta):
        theta *= pi / 180

        axes = [Model.X, Model.Y, Model.Z]
        axes.remove(axis)
        rot_mat = Lin_Alg.get_2d_rotation_matrix(theta)

        def rotate(vector):
            new_vector = []
            for element in vector:
                new_element = [0, 0, 0]
                two_d_element = element.copy()
                new_element[axis] = two_d_element.pop(axis)

                rotation_product = Lin_Alg.vector_matrix_multiplication(two_d_element, rot_mat)
                for i in range(len(axes)):
                    new_element[axes[i]] = rotation_product[i]
                new_vector.append(new_element)
            return new_vector

        self.rotated_vertices = rotate(self.rotated_vertices)
        self.rotated_unit_normals = rotate(self.rotated_unit_normals)
    
    def complex_rotate(self, x0, y0, x1, y1):
        dx, dy = x1 - x0, y1 - y0
        length = hypot(dx, dy)
        if length == 0:
            return
        theta = length * 0.01 * pi / 180

        two_d_unit_vector = Lin_Alg.get_unit_vector([dx, dy])
        normal_vector = Lin_Alg.get_normal_vector(two_d_unit_vector)
        rot_mat = Lin_Alg.get_unit_vector_3d_rotation_matrix(normal_vector, theta)

        def rotate(vector):
            new_elements = []
            for element in vector:
                new_element = Lin_Alg.vector_matrix_multiplication(element, rot_mat)
                new_elements.append(new_element)
            return new_elements
        
        self.rotated_vertices = rotate(self.rotated_vertices)
        self.rotated_unit_normals = rotate(self.rotated_unit_normals)
        
        new_angles = self.get_angles()
        return new_angles
    
    def get_angles(self):
        def get_angle(a0, b0, a1, b1):
            A = [
                [ b0, a0],
                [-a0, b0]
            ]
            inverse = Lin_Alg.get_2d_inverse(A)
            sin_cos_vec = Lin_Alg.vector_matrix_multiplication([a1, b1], inverse)
            
            theta = atan2(sin_cos_vec[0], sin_cos_vec[1])
            return (round(degrees(theta)) + 360) % 360
        
        x0, y0, z0 = self.vertices[0]
        x1, y1, z1 = self.rotated_vertices[0]

        alpha = get_angle(x0, y0, x1, y1)
        beta = get_angle(x0, z0, x1, z1)
        gamma = get_angle(y0, z0, y1, z1)

        return [gamma, beta, alpha]
    
    # Lighting
    def apply_lighting(self):
        def calc_intensity(light_direc, intensities, unit_normal):
            sin_theta = -Lin_Alg.dot_product(light_direc, unit_normal)
            light_amount = max(0, sin_theta)
            intensity = [light_amount * intensity for intensity in intensities]
            return intensity

        shaded_colors = []
        for i in range(len(self.faces)):
            intensity = calc_intensity(
                Model.light_direc,
                Model.intensities,
                self.rotated_unit_normals[i]
            )

            shaded_color = [
                max(min(round((intensity[j] + 0.2) * self.colors[i][j]), 255), 0)
                for j in range(3)
            ]
            shaded_colors.append(shaded_color)
        
        return shaded_colors
    
    # Drawing
    def project(self, focal_length, w, h):
        two_d_vertices = []
        for vertex in self.rotated_vertices:
            aspect_ratio = focal_length / (focal_length + -vertex[Model.Z])

            new_x = vertex[Model.X] * aspect_ratio + w / 2
            new_y = h - (vertex[Model.Y] * aspect_ratio + h / 2)
            coordinate = [new_x, new_y]
            two_d_vertices.append(coordinate)
        
        return two_d_vertices
    
    def draw_order(self):
        avg_z = []
        for face in self.faces:
            avg = sum(self.rotated_vertices[vertex][2] for vertex in face) / len(face)
            avg_z.append(avg)
        
        indices = list(range(len(self.faces)))
        ordered_face_inds = [i for z, i in sorted(zip(avg_z, indices))]
        return ordered_face_inds
    
    def draw(self, window, focal_length):
        w, h = window.get_size()
        window.fill((255, 255, 255))

        two_d_vertices = self.project(focal_length, w, h)
        self.shaded_colors = self.apply_lighting()

        for i in range(len(self.faces)):
            view_vector = self.rotated_vertices[self.faces[i][0]].copy()
            view_vector[Model.Z] -= focal_length
            if Lin_Alg.dot_product(view_vector, self.rotated_unit_normals[i]) >= 0:
                continue
            
            triangles = Triangle.triangulate(two_d_vertices, self.faces[i])
            for triangle in triangles:
                coordinates = [two_d_vertices[j] for j in triangle]
                pg.draw.polygon(window, self.colors[i], coordinates)
                # Triangle.draw(window, coordinates, self.colors[i])
                pg.draw.polygon(window, 'black', coordinates, width = 1)
        
        '''
        for edge in self.edges:
            x0, y0 = two_d_vertices[edge[0]]
            x1, y1 = two_d_vertices[edge[1]]
            canvas.create_line(x0, y0, x1, y1, width = 5)
        '''