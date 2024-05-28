import random
from time import sleep
from cells import Cell
class Maze():
    def __init__(self, x_offset, y_offset, num_rows, num_columns, cell_size_x, cell_size_y, win, seed=None):
        random.seed(seed)
        self._cells = []
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(0, self._num_rows): # i is y cords
            self._cells.append([])
            for j in range(0, self._num_columns):  # j is x cords
                x1 = self._x_offset + (j * self._cell_size_x)
                y1 = self._y_offset + (i * self._cell_size_y)
                self._cells[i].append(Cell(x1, x1 + self._cell_size_x, y1, y1 + self._cell_size_y, self._win))
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        # (i , j) = (y , x)
        self._cells[i][j].draw()

    def _animate(self, time):
        if self._win is None:
            return
        self._win.redraw()
        sleep(time)

    def _break_entrance_and_exit(self):
        if not self._cells:
            return
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_rows - 1][self._num_columns - 1].has_bottom_wall = False
        self._draw_cell(self._num_rows - 1, self._num_columns - 1)

    def _break_walls_r(self, i, j):
        if not self._cells:
            return
        self._cells[i][j]._visited = True
        current = self._cells[i][j]
        directions = [(0,1), (1,0), (0, -1), (-1, 0)] # right  down  left  up
        # (i , j) = (y , x)
        while directions:
            direction = directions.pop(random.randint(0, len(directions)-1)) # get random directoin
            h = i + direction[0]
            k = j + direction[1]
            if 0 <= h < self._num_rows and 0 <= k < self._num_columns: # is valid direction
                next = self._cells[h][k]
                if not next._visited: # not visited yet
                  match direction:
                      case (0,1): # right
                            current.has_right_wall = False
                            next.has_left_wall = False
                            self._cells[i][j].draw()
                            self._cells[h][k].draw()
                            self._break_walls_r(h, k)
                      case (1,0): # down
                            current.has_bottom_wall = False
                            next.has_top_wall = False
                            self._cells[i][j].draw()
                            self._cells[h][k].draw()
                            self._break_walls_r(h, k)
                      case (0,-1): # left
                            current.has_left_wall = False
                            next.has_right_wall = False
                            self._cells[i][j].draw()
                            self._cells[h][k].draw()
                            self._break_walls_r(h, k)
                      case (-1,0): # up
                            current.has_top_wall = False
                            next.has_bottom_wall = False
                            self._cells[i][j].draw()
                            self._cells[h][k].draw()
                            self._break_walls_r(h, k)

    def _reset_cells_visited(self):
        if not self._cells:
            return
        for col in self._cells:
            for cell in col:
                cell._visited = False

    def _solve_r(self, i, j):
        self._animate(0.02)
        current = self._cells[i][j]
        current._visited = True
        if i == (self._num_rows-1) and j == (self._num_columns-1):
            self._win.draw_circle(current.p1.x, current.p1.y, current.p4.x, current.p4.y)
            self._animate(.5)
            return True
        directions = [(0,1), (1,0), (0, -1), (-1, 0)] # right  down  left  up
        # (i , j) = (y , x)
        while directions:
            direction = directions.pop(0) # move in constant directions order
            h = i + direction[0]
            k = j + direction[1]
            valid_dir = False
            match direction:
                case (0,1): # right
                    if not current.has_right_wall:
                        valid_dir = True
                case (1,0): # down
                    if not current.has_bottom_wall:
                        valid_dir = True
                case (0,-1): # left
                    if not current.has_left_wall:
                        valid_dir = True
                case (-1,0): # up
                    if not current.has_top_wall:
                        valid_dir = True
            if valid_dir:
                if 0 <= h < self._num_rows and 0 <= k < self._num_columns: # is valid direction
                    next = self._cells[h][k]
                    if not next._visited:
                        current.draw_move(next)
                        if self._solve_r(h, k):
                            return True
                        else:
                            current.draw_move(next, True)
                            self._animate(0.3) # make backtracking slightly slower
        return False

    def _solve(self):
        self._win.draw_circle(self._x_offset, self._y_offset, self._x_offset + self._cell_size_x, self. _y_offset + self._cell_size_y)
        if self._solve_r(0, 0):
            print("End Reached")
        else:
            print("End Not Found")
