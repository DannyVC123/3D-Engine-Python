from math import *
from collections import deque

from lin_alg import Lin_Alg

class Graph:
    def __init__(self, adjacancy_list = {}):
        self.adjacency_list = adjacancy_list
    
    def add_edge(self, node1, node2):
        if node1 in self.adjacency_list:
            self.adjacency_list[node1].append(node2)
        else:
            self.adjacency_list[node1] = [node2]
        
        if node2 in self.adjacency_list:
            self.adjacency_list[node2].append(node1)
        else:
            self.adjacency_list[node2] = [node1]
    
    def bfs(self, num_vertices):
        faces = []
        included_faces = set()

        for start in self.adjacency_list.keys():
            queue = deque()

            queue.append([start])
            while len(queue) > 0:
                curr_path = queue.popleft()
                last_visited = curr_path[-1]
                
                if len(curr_path) > 6:
                    continue

                for neighbor in self.adjacency_list[last_visited]:
                    if neighbor == start and len(curr_path) in num_vertices:
                        sorted_face = tuple(sorted(curr_path))
                        if sorted_face not in included_faces:
                            faces.append(curr_path)
                            included_faces.add(sorted_face)
                        continue
                    if neighbor not in curr_path:
                        new_path = curr_path.copy()
                        new_path.append(neighbor)
                        queue.append(new_path)
        
        return faces


class Soccer_Ball:
    @staticmethod
    def create_ball(edge_length):
        vertices = Soccer_Ball.get_vertices(edge_length)
        faces = Soccer_Ball.get_faces(vertices, edge_length)
        unit_normals = Soccer_Ball.get_unit_normals(vertices, faces)
        colors = [([0, 0, 0] if len(face) == 5 else [245, 245, 245]) for face in faces]
        return (vertices, faces, unit_normals, colors)
    
    @staticmethod
    def get_vertices(edge_length):
        coordinate1 = [
            0,
            1/2 * edge_length,
            (3 + 3 * sqrt(5)) / 4 * edge_length
        ]
        coordinate2 = [
            1/2 * edge_length,
            (5 + sqrt(5)) / 4 * edge_length,
            (1 + sqrt(5)) / 2 * edge_length
        ]
        coordinate3 = [
            (1 + sqrt(5)) / 4 * edge_length,
            edge_length,
            (2 + sqrt(5)) / 2 * edge_length
        ]
        
        vertices = []
        Soccer_Ball.generate_permutations(coordinate1, 4, vertices)
        Soccer_Ball.generate_permutations(coordinate2, 8, vertices)
        Soccer_Ball.generate_permutations(coordinate3, 8, vertices)
        
        '''
        print('[', end='')
        for v in vertices:
            print(f'({v[0]}, {v[1]}, {v[2]})', end=', ')
        print(']')
        '''
        return vertices
    
    @staticmethod
    def generate_permutations(coordinate, sign_combos, vertices):
        even_permutations = [
            [0, 1, 2],
            [2, 0, 1],
            [1, 2, 0]
        ]
        bin_length = int(log2(sign_combos))

        for permutation in even_permutations:
            vertex_perm = [coordinate[i] for i in permutation]
            
            for binary in range(sign_combos):
                binary_str = format(binary, f'0{bin_length}b')
                curr_axis = 0
                new_vertex = [0, 0, 0]

                for bit in binary_str:
                    sign = 1 if bit == '1' else -1

                    if vertex_perm[curr_axis] == 0:
                        curr_axis += 1
                    new_vertex[curr_axis] = vertex_perm[curr_axis] * sign
                    curr_axis += 1
                
                vertices.append(new_vertex)
    
    @staticmethod
    def get_faces(vertices, edge_length):
        graph = Graph()
        error = 0.001

        for i in range(len(vertices) - 1):
            for j in range(i + 1, len(vertices)):
                dx = vertices[j][0] - vertices[i][0]
                dy = vertices[j][1] - vertices[i][1]
                dz = vertices[j][2] - vertices[i][2]
                dist = sqrt(dx ** 2 + dy ** 2 + dz ** 2)

                if edge_length - error <= dist <= edge_length + error:
                    graph.add_edge(i, j)
        
        faces = graph.bfs([5, 6])
        return faces
    
    def get_unit_normals(vertices, faces):
        unit_normals = []

        for face in faces:
            vec1 = [vertices[face[1]][i] - vertices[face[0]][i] for i in range(3)]
            vec2 = [vertices[face[2]][i] - vertices[face[1]][i] for i in range(3)]

            normal = Lin_Alg.cross_product(vec1, vec2)
            unit_normal = Lin_Alg.get_unit_vector(normal)

            inward_vec = [-element for element in vertices[face[0]]]
            dot_product = Lin_Alg.dot_product(unit_normal, inward_vec)
            if dot_product > 0:
                unit_normal = [-element for element in unit_normal]

            unit_normals.append(unit_normal)
        
        return unit_normals

            
if __name__ == "__main__":
    vertices = Soccer_Ball.get_vertices()
    faces = Soccer_Ball.get_faces(vertices)