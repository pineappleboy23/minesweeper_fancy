import pygame as pg
import random
import math

pg.init()

clock = pg.time.Clock()


barrier_size = 2
block_size = 35
grid_w = 28
grid_h = 20


sw = 1001
sh = 705
screen_color = (48, 141, 240)

# pg.display.set_caption("Minesweeper")
win = pg.display.set_mode((sw, sh))
win.fill(screen_color)



class Grid(object):
    def __init__(self):
        self.grid = []
        self.get_grid()
        # self.bomb_count = 30
        self.grid_positions_to_update = []


    def get_grid(self):
        for i in range(grid_h):
            temp_array = []
            for ii in range(grid_w):
                temp_array.append(Box((ii, i), self.get_random()))
            self.grid.append(temp_array)


    def get_random(self):
        if random.random() > .85:
            return True
        return False



    def update_grid(self, mouse_key):
        for i in self.grid:
            for ii in i:
                grid_clone = self.grid
                for pp in ii.update_state(grid_clone, mouse_key):
                    self.grid_positions_to_update.append(pp)

        while len(self.grid_positions_to_update) > 0:
            self.grid_positions_to_update = self.clear_blank_space()

    def clear_blank_space(self):
        temp_grid_positions_to_update = []
        for i in self.grid:
            for ii in i:
                for iii in self.grid_positions_to_update:
                    if iii == ii.a_pos:
                        temp_grid = self.grid
                        for iiii in ii.update_number(temp_grid, "clear"): # I know too many i's but it was fun
                            add_it = True
                            for iiiii in self.grid_positions_to_update:
                                if iiii == iiiii:
                                    add_it = False
                            if add_it:
                                temp_grid_positions_to_update.append(iiii)
                        ii.hidden = False

        return temp_grid_positions_to_update



    def bomb_check(self):
        for i in self.grid:
            for ii in i:
                if ii.bomb and not ii.hidden:
                    return True


    def draw(self, win):
        for i in self.grid:
            for ii in i:
                ii.draw(win)


class Box(object):
    def __init__(self, pos, bomb):
        self.hidden = True
        self.number = 0
        self.bomb = bomb
        self.flag = False

        self.array_x, self.array_y = pos
        self.a_pos = pos
        self.x = barrier_size * self.array_x + block_size * (self.array_x - 1)
        self.y = barrier_size * self.array_y + block_size * (self.array_y - 1)
        self.w = block_size
        self.h = block_size


    def update_state(self, grid_in, mouse_button):
        if mouse_button == 1 and self.collision_detect() and not self.flag:
            self.hidden = False
            # left pressed = uncover
        if mouse_button == 3 and self.collision_detect():
            if self.hidden:
                if self.flag:
                    self.flag = False
                else:
                    self.flag = True
            # right pressed = flag
        if not self.hidden:
            return self.update_number(grid_in, "state")
        else:
            return []


    def collision_detect(self):
        if self.x < pg.mouse.get_pos()[0] and self.y < pg.mouse.get_pos()[1]:
            if self.x + self.w > pg.mouse.get_pos()[0] and self.y + self.h > pg.mouse.get_pos()[1]:
                return True
        return False

    def update_number(self, grid_in, from_state_or_clear):
        bomb_count = 0
        pos_to_update = []
        for i in grid_in:
            for ii in i:
                if self.check_3x3(ii):
                    pos_to_update.append(ii.a_pos)
                    if ii.bomb:
                        bomb_count += 1

        self.number = bomb_count


        if (bomb_count == 0 and from_state_or_clear == "state"):
            return pos_to_update
        elif from_state_or_clear == "clear" and self.hidden and bomb_count == 0:
            return pos_to_update
        else:
            return []

    def check_3x3(self, box_in):
        if self.array_x - box_in.array_x > -2 and self.array_x - box_in.array_x < 2:
            if self.array_y - box_in.array_y > -2 and self.array_y - box_in.array_y < 2:
                return True
        return False





    def draw(self, win):
        if self.hidden:
            pg.draw.rect(win, (150, 150, 150), (self.x, self.y, self.w, self.h))
        if not self.hidden:
            pg.draw.rect(win, (120, 120, 120), (self.x, self.y, self.w, self.h))
            if self.number > 0:
                font_name = pg.font.get_default_font()
                font = pg.font.Font(font_name, 38)
                t_surf = font.render(str(self.number), True, (22, 174, 75))
                t_rec = t_surf.get_rect()
                t_rec.center = (self.x + 18,self.y + 20)
                win.blit(t_surf, t_rec)
            else:
                pass
        if self.bomb:
            pg.draw.rect(win, (0, 50, 150), (self.x + 5, self.y + 5, self.w - 10, self.h - 10))
        if self.flag:
            pg.draw.rect(win, (252, 87, 66), (self.x + 8, self.y + 8, self.w - 16, self.h - 16))


def redraw_game_window():
    win.fill(screen_color)

    size_z = 35
    edge_z = 2
    pg.draw.rect(win, (130, 130, 130), (edge_z, edge_z, size_z, size_z))
    pg.draw.rect(win, (150, 150, 150), (2 * edge_z + size_z, edge_z, size_z, size_z))
    pg.draw.rect(win, (150, 150, 150), (edge_z, edge_z * 2 + size_z, size_z, size_z))
    pg.draw.rect(win, (150, 150, 150), (edge_z * 2 + size_z, edge_z * 2 + size_z, size_z, size_z))

    grid.draw(win)



    pg.display.update()



grid = Grid()


running = True
while running:

    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONUP:
            print(event)
            if event.button == 1:
                print("1")
                grid.update_grid(1)
            if event.button == 3:
                print("3")
                grid.update_grid(3)


    # check if bomb clicked
    if grid.bomb_check():
        grid = Grid()



    redraw_game_window()
