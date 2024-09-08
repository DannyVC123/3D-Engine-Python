from math import *

from lin_alg import Lin_Alg

class Polygon:
    @staticmethod
    def triangulate(vertices, face):
        triangles = []
        
        vertices_left = face.copy()
        while len(vertices_left) > 3:
            num_vertices_left = len(vertices_left)
            for i in range(num_vertices_left):
                curr_vertex = vertices[vertices_left[i]]

                left_ind = (i - 1 + num_vertices_left) % num_vertices_left
                left_vertex = vertices[face[left_ind]]
                left_vector  = [(left_vertex[j]  - curr_vertex[j]) for j in range(2)]

                right_ind = (i + 1) % num_vertices_left
                right_vertex = vertices[face[right_ind]]
                right_vector = [(right_vertex[j] - curr_vertex[j]) for j in range(2)]

                cross_product = Lin_Alg.get_2d_determinant([right_vector, left_vector])
                if cross_product < 0:
                    continue
                
                valid_ear = True
                for j in range(num_vertices_left):
                    if j == i or j == left_ind or j == right_ind:
                        continue

                    test_vertex = vertices[vertices_left[j]]
                    test_vector = [test_vertex[k] - curr_vertex[k] for k in range(2)]
                    cross_product = Lin_Alg.get_2d_determinant([left_vector, test_vector])
                    if cross_product > 0:
                        valid_ear = False
                
                if not valid_ear:
                    continue
                triangles.append([i, left_ind, right_ind])
                vertices_left.remove(i)
                break
        
        triangles.append(vertices_left)
        return triangles

vertices = [
    [-1,1],
    [-1,-1],
    [1,-1],
    [1,1]
]
face = [0,1,2,3]
print(Polygon.triangulate(vertices, face))

