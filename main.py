import pygame
import numpy as np
import math
import Player
import Cube
import menu

def load_texture(path, factor):
    texture = pygame.image.load(path)
    txt = pygame.transform.scale(texture, (
        int(texture.get_width() * factor), int(texture.get_height() * factor)))
    return txt
def get_center(cube, camera):
    return sum(np.linalg.norm(np.array(i) - np.array(camera)) for i in cube.vertices) / len(cube.vertices)
def game(width, height, fps):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    status = True
    cubes = []
    SIZE = 10
    GROUND = SIZE * 6
    x, y, z = 0, GROUND, SIZE * 10
    side = load_texture('texture/leaves_oak.png', 0.5)
    top_bottom = load_texture('texture/tnt_b.png', 0.5)
    player = Player.Player(np.array([0, 0, 0]), 0, 0, 3)
    with_surface = 7
    lenght_surface = 7
    for i in range(with_surface):
        for j in range(lenght_surface):
            cubes.append(Cube.cube(screen, width, height, (y, x, z), SIZE, side, top_bottom))
            x += (SIZE * 2)
        y = GROUND
        x = 0
        z += (SIZE * 2)
    Menu = menu.Menu(screen, width, height)
    Menu.show()
    while status:
        sorted_cubes = sorted(cubes, key=lambda x_: (get_center(x_, player.pos)), reverse=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.jump_force == 0:
                        player.jump_force = 5
                elif event.key == pygame.K_c:
                    Menu.show()
            elif event.type == pygame.MOUSEMOTION:
                dx, dy = event.rel
                dx = -math.radians(dx)
                dy = math.radians(dy)
                for cube in sorted_cubes:
                    cube.rotate_cube(dx, dy)
                player.rotate_player(dx, dy)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    for cube in sorted_cubes[::-1]:
                        collide = cube.draw_cube(player.pos, mouse_pos)
                        if collide is not None:
                            if any(collide[i] != cube_.pos[i] for cube_ in cubes for i in range(3)):
                                cubes.append(
                                    Cube.cube(screen, width, height, collide, SIZE, side, top_bottom))
            if not Menu.status and player.jump_force == 0:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_z]:
                    player.move_forward()
                if keys[pygame.K_q]:
                    player.move_left()
                if keys[pygame.K_s]:
                    player.move_back()
                if keys[pygame.K_d]:
                    player.move_right()
        if not Menu.status:
            screen.fill((135, 206, 235))
            player.jump()
            for cube in sorted_cubes[-100:]:
                cube.draw_cube(player.pos, pygame.mouse.get_pos())
        pygame.display.set_caption(f'fps = {str(round(clock.get_fps()))}')
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == '__main__':
    game(800, 600, 60)