from math import *

from model import Model
from lin_alg import Lin_Alg

class Obj_Parser():
    @staticmethod
    def parse_obj(obj_filename, scale_factor = 1, color = None, has_vn = True, outward_vn = True):
        vertices = []
        vertex_normals = []

        faces = []
        vertex_normal_inds = []

        def simple_parse(line, start):
            vector_str = line[start:].strip()
            scaled_vector = [float(element) * scale_factor for element in vector_str.split()]
            return scaled_vector
        
        def parse_face(line):
            face_str = line[2:].strip()
            face_info = face_str.split()
            
            triples = [element.split("/") for element in face_info]
            face = [int(triple[0]) - 1 for triple in triples]
            if has_vn:
                vertex_normal_ind = int(triples[0][2]) - 1
                return (face, vertex_normal_ind)
            else:
                return face

        with open(obj_filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertex = simple_parse(line, 2)
                    vertices.append(vertex)
                elif line.startswith('vn '):
                    vertex_normal = simple_parse(line, 3)
                    if not outward_vn:
                        vertex_normal = [-element for element in vertex_normal]
                    vertex_normals.append(vertex_normal)
                elif line.startswith('f '):
                    if has_vn:
                        face, vertex_normal_ind = parse_face(line)
                        faces.append(face)
                        vertex_normal_inds.append(vertex_normal_ind)
                    else:
                        face = parse_face(line)
                        faces.append(face)
        
        vertices = Obj_Parser.adjust_vertices(vertices)
        unit_normals = Obj_Parser.get_unit_vectors(vertices, vertex_normals, faces, vertex_normal_inds)
        return Model(vertices, faces, unit_normals, color)

    @staticmethod
    def adjust_vertices(vertices):
        center = Obj_Parser.get_min_sphere(vertices)
        new_vertices = [[vertices[i][j] - center[j] for j in range(3)] for i in range(len(vertices))]
        return new_vertices
    
    @staticmethod
    def get_unit_vectors(vertices, vertex_normals, faces, vertex_normal_inds):
        unit_normals = []

        for i in range(len(faces)):
            vec1 = [vertices[faces[i][1]][j] - vertices[faces[i][0]][j] for j in range(3)]
            vec2 = [vertices[faces[i][2]][j] - vertices[faces[i][1]][j] for j in range(3)]

            normal = Lin_Alg.cross_product(vec1, vec2)
            unit_normal = Lin_Alg.get_unit_vector(normal)

            if vertex_normals != []:
                dot_product = Lin_Alg.dot_product(unit_normal, vertex_normals[vertex_normal_inds[i]])
                if dot_product < 0:
                    unit_normal = [-element for element in unit_normal]

            unit_normals.append(unit_normal)
        
        return unit_normals
    
    @staticmethod
    def get_min_sphere(vertices):
        min_x_ind = max_x_ind = min_y_ind = max_y_ind = min_z_ind = max_z_ind = 0
        for i in range(len(vertices)):
            if vertices[i][0] < vertices[min_x_ind][0]:
                min_x_ind = i
            if vertices[i][0] > vertices[max_x_ind][0]:
                max_x_ind = i
            if vertices[i][1] < vertices[min_y_ind][1]:
                min_y_ind = i
            if vertices[i][1] > vertices[max_y_ind][1]:
                max_y_ind = i
            if vertices[i][2] < vertices[min_z_ind][2]:
                min_z_ind = i
            if vertices[i][2] > vertices[max_z_ind][2]:
                max_z_ind = i
        
        vertex_pairs = [
            [vertices[min_x_ind], vertices[max_x_ind]],
            [vertices[min_y_ind], vertices[max_y_ind]],
            [vertices[min_z_ind], vertices[max_z_ind]]
        ]
        dx = Lin_Alg.get_length([vertex_pairs[0][1][i] - vertex_pairs[0][0][i] for i in range(3)])
        dy = Lin_Alg.get_length([vertex_pairs[1][1][i] - vertex_pairs[1][0][i] for i in range(3)])
        dz = Lin_Alg.get_length([vertex_pairs[2][1][i] - vertex_pairs[2][0][i] for i in range(3)])
        deltas = [dx, dy, dz]

        largest_pair = [pair for d, pair in sorted(zip(deltas, vertex_pairs), reverse = True)][0]
        center = [(largest_pair[0][i] + largest_pair[1][i]) / 2 for i in range(3)]

        dx = center[0] - largest_pair[0][0]
        dy = center[1] - largest_pair[0][1]
        dz = center[2] - largest_pair[0][2]
        radius_sq = dx ** 2 + dy ** 2 + dz ** 2
        radius = sqrt(radius_sq)

        for vertex in vertices:
            dx = vertex[0] - center[0]
            dy = vertex[1] - center[1]
            dz = vertex[2] - center[2]
            dist_sq = dx ** 2 + dy ** 2 + dz ** 2

            if dist_sq <= radius_sq:
                continue

            dist = sqrt(dist_sq)
            dist_unit_vector = Lin_Alg.get_unit_vector([dx, dy, dz], dist)
            diff = (dist - radius) / 2
            center = [center[i] + diff * dist_unit_vector[i] for i in range(3)]

            radius += diff
            radius_sq = radius ** 2
        
        return center
