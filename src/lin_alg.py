from math import *

class Lin_Alg:
    # Rotation
    @staticmethod
    def get_2d_rotation_matrix(theta):
        s_t, c_t = sin(theta), cos(theta)
        return [
            [c_t, -s_t],
            [s_t,  c_t]
        ]
    
    @staticmethod
    def get_simple_3d_rotation_matrix(alpha, beta, gamma):
        s_a, c_a = sin(alpha), cos(alpha)
        s_b, c_b = sin(beta),  cos(beta)
        s_g, c_g = sin(gamma), cos(gamma)

        return [
            [c_a * c_b,    c_a * s_b * s_g - s_a * c_g,    c_a * s_b * c_g + s_a * s_g],
            [s_a * c_b,    s_a * s_b * s_g + c_a * c_g,    s_a * s_b * c_g - c_a * s_g],
            [-s_b,         c_b * s_g,                      c_b * c_g]
        ]

    @staticmethod
    def get_unit_vector_3d_rotation_matrix(two_d_unit_vector, theta):
        u_x, u_y = two_d_unit_vector

        c_t, s_t = cos(theta), sin(theta)
        one_minus_c_t = 1 - c_t

        return [
            [u_x ** 2 * one_minus_c_t + c_t,    u_x * u_y * one_minus_c_t,         u_y * s_t],
            [u_x * u_y * one_minus_c_t,         u_y ** 2 * one_minus_c_t + c_t,    -u_x * s_t],
            [-u_y * s_t,                        u_x * s_t,                         c_t]
        ]
    
    #3D
    @staticmethod
    def get_length(vector):
        squared_sum = sum(num ** 2 for num in vector)
        length = sqrt(squared_sum)
        return length

    @staticmethod
    def get_unit_vector(vector, length = None):
        if length == None:
            length = Lin_Alg.get_length(vector)
        return [num / length for num in vector]
    
    @staticmethod
    def dot_product(vec1, vec2):
        if len(vec1) != len(vec2):
            raise ValueError('number of elements in vec1 and vec2 must match')
        return sum(vec1[i] * vec2[i] for i in range(len(vec1)))
    
    @staticmethod
    def cross_product(vec1, vec2):
        if len(vec1) != len(vec2):
            raise ValueError('number of elements in vec1 and vec2 must match')
        
        def determinant(vec1, vec2, direc):
            cols = [0, 1, 2]
            cols.remove(direc)
            a, b = [vec1[cols[i]] for i in range(len(cols))]
            c, d = [vec2[cols[i]] for i in range(len(cols))]
            return a * d - b * c
        
        product = [0, 0, 0]
        product[0] = determinant(vec1, vec2, 0)
        product[1] = -determinant(vec1, vec2, 1)
        product[2] = determinant(vec1, vec2, 2)
        return product

    @staticmethod
    def vector_matrix_multiplication(vector, matrix):
        if len(vector) != len(matrix):
            raise ValueError('number of columns in vector must equal number of rows in matrix')
        
        product = [0] * len(vector)
        for c in range(len(matrix[0])):
            product[c] = sum(vector[i] * matrix[c][i] for i in range(len(vector)))
        return product
    
    # 2D
    @staticmethod
    def get_normal_vector(unit_vector):
        return [-unit_vector[1], unit_vector[0]]
    
    @staticmethod
    def get_inverse(matrix):
        a, b = matrix[0]
        c, d = matrix[1]

        coefficient = 1 / (a * d - b * c)
        inverse = [
            [coefficient *  d, coefficient * -b],
            [coefficient * -c, coefficient *  a]
        ]
        return inverse