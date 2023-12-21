import numpy as np
import pygame

class cube:
    def __init__(self, screen, width, height, pos, edge, side, top_bottom):
        self.screen = screen
        self.pos = pos
        self.edge = edge
        self.width = width
        self.height = height
        self.vertices = np.array([
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]) * self.edge + self.pos
        self.sides = {
            (0, 0, -edge): [(0, 1, 2, 3), side],
            (0, 0, edge): [(4, 5, 6, 7), side],
            (0, -edge, 0): [(0, 1, 5, 4), side],
            (0, edge, 0): [(3, 2, 6, 7), side],
            (-edge, 0, 0): [(0, 3, 7, 4), top_bottom],
            (edge, 0, 0): [(1, 2, 6, 5), top_bottom]
        }
        self.angleX = 0
        self.angleY = 0
        self.f = 3
        self.alpha = 100
        self.beta = 100
        self.Oi = height // 2
        self.Oj = width // 2
    @staticmethod
    def rotate_x(vertices, angle, camera):
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
        return np.dot((vertices - camera), rotation_matrix) + camera
    @staticmethod
    def rotate_y(vertices, angle, camera):
        rotation_matrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
        return np.dot((vertices - camera), rotation_matrix) + camera
    def is_axe_z_pos(self, vertices):
        for vertex in vertices:
            if vertex[2] <= self.f:
                return False
        return True
    @staticmethod
    def transform_points(points, f, camera):
        new_points = points - camera
        points_x = new_points[..., 0]
        points_y = new_points[..., 1]
        points_z = (new_points[..., 2] - f + 0.000001)
        return np.column_stack((points_x / points_z, points_y / points_z, np.ones(len(new_points))))
    @staticmethod
    # interpolation
    def lerp(p1, p2, f):
        return p1 + f * (p2 - p1)
    def lerp2d(self, p1, p2, f):
        return tuple(self.lerp(p1[i], p2[i], f) for i in range(2))
    def allwoed(self, vertices):
        for vertix in vertices:
            x, y= vertix
            if not (-50 <= x <= self.width + 50 and -200 <= y <= self.height + 50):
                return False
        return True
    def rotate_cube(self, dx, dy):
        self.angleX += dx
        self.angleY += dy
    def side_center(self, side, camera):
        vertices = self.sides[side][0]
        sum_distance = sum(np.linalg.norm(np.array(self.vertices[i]) - np.array(camera)) for i in vertices)
        return sum_distance / len(vertices)
    def project_3d_to_2d(self, points, camera):
        f = self.f
        K = np.array(
            [[0, f * self.beta, self.Oi],
             [f * self.alpha, 0, self.Oj]])
        transformed_points = self.transform_points(points, f, camera)
        projected_points = np.dot(K, transformed_points.T).T
        return projected_points
    def draw_cube(self, camera, mosepose):
        collide = None
        vertices = self.rotate_x(self.vertices, self.angleX, camera)
        vertices = self.rotate_y(vertices, self.angleY, camera)
        if self.is_axe_z_pos(vertices):
            projected_vertices = self.project_3d_to_2d(vertices, camera)
            sorted_sides = sorted(self.sides.items(), key=lambda x: self.side_center(x[0], camera), reverse=True)
            for side, (indices, texture) in sorted_sides[3:6]:
                vertices = [projected_vertices[i] for i in indices]
                if self.allwoed(vertices):
                    collide = self.texture_glue(self.screen, vertices, texture, mosepose)
                    if collide is not None:
                        collide = np.array([collide[0], collide[1], collide[2]]) + np.array(side)
        if collide is not None:
            return collide
        return None
    def texture_glue(self, surface, vertices, texture, mouse_pos):
        points = {}
        collided = False
        texture_size = texture.get_size()
        width, height = texture_size[0], texture_size[1]
        mouse_x, mouse_y = mouse_pos
        texture_data = pygame.surfarray.array3d(texture)

        for i in range(height + 1):
            parameter_height = i / height
            b = self.lerp2d(vertices[0], vertices[1], parameter_height)
            c = self.lerp2d(vertices[3], vertices[2], parameter_height)
            for d in range(width + 1):
                parameter_width = d / width
                a = self.lerp2d(c, b, parameter_width)
                points[d, i] = a
        for x in range(width):
            for y in range(height):
                color = texture_data[x, y]
                polygon_points = [points[a, b] for a, b in [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]]
                rect = pygame.draw.polygon(surface, color, polygon_points)
                if rect.collidepoint(mouse_x, mouse_y):
                    collided = True
        return self.pos if collided else None