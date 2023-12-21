import math

class Player:
    def __init__(self, pos, angleX, angleY, speed):
        self.pos = pos
        self.speed = speed
        self.angleX = angleX
        self.angleY = angleY
        self.jump_force = 0
        self.gravity_pull = 0.2
        self.gravity = 0.8

    def move_forward(self):
        self.pos[1] -= self.speed * math.sin(self.angleX)
        self.pos[2] += self.speed * math.cos(self.angleX)
    def move_left(self):
        self.pos[1] -= self.speed * math.cos(self.angleX)
        self.pos[2] -= self.speed * math.sin(self.angleX)
    def move_back(self):
        self.pos[2] -= self.speed * math.cos(self.angleX)
        self.pos[1] += self.speed * math.sin(self.angleX)

    def move_right(self):
        self.pos[1] += self.speed * math.cos(self.angleX)
        self.pos[2] += self.speed * math.sin(self.angleX)

    def rotate_player(self, angleX, angleY):
        self.angleX += angleX
        self.angleY += angleY
    def jump(self):
        # Simulate player jumping
        self.jump_force = max(0, self.jump_force - self.gravity_pull)
        self.pos[0] = min(0, self.pos[0] - self.jump_force + self.gravity)
