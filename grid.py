from random import randint
from time import sleep
from graphics import Window, Point, Line, Circle
class Grid():
    def __init__(self, grid_size, display_size):
        self.grid_size = grid_size
        self.display_size = display_size
        self.cell_size = display_size // (grid_size + 1)
        self.offset = self.cell_size // 2
        self.win = Window(display_size, display_size)
        self.points = []
        self.cells = []
        self.lines = {}
        self.solve_lines = {}

        for i in range(grid_size + 1): # i values are the y cords
            self.points.append([])
            if not i == grid_size:
                self.cells.append([])
            for j in range(grid_size + 1): # j values are the x cords
                self.points[i].append(Point(j,i))
                if not i == grid_size and not j == grid_size:
                    self.cells[i].append(Cell(j,i))

        for i in range(grid_size + 1):
            for j in range(grid_size + 1):
                if j < grid_size:
                    p1 = Point((self.offset+(j*self.cell_size)), (self.offset+(i*self.cell_size)))
                    p2 = Point((self.offset+((j+1)*self.cell_size)), (self.offset+(i*self.cell_size)))
                    self.lines[(self.points[i][j],self.points[i][j+1])] = Line(p1, p2, self.win.canvas)
                if i < grid_size:
                    p1 = Point((self.offset+(j*self.cell_size)), (self.offset+(i*self.cell_size)))
                    p2 = Point((self.offset+(j*self.cell_size)), (self.offset+((i+1)*self.cell_size)))
                    self.lines[(self.points[i][j],self.points[i+1][j])] = Line(p1, p2, self.win.canvas)
    
    def create_maze(self):
        self.win.canvas.delete(self.lines[(self.points[0][0],self.points[0][1])].line_id) # break entrance wall
        del self.lines[(self.points[0][0],self.points[0][1])]
        self.cells[0][0].has_top_wall = False

        self.win.canvas.delete(self.lines[(self.points[self.grid_size][self.grid_size-1],self.points[self.grid_size][self.grid_size])].line_id) # break exit wall
        del self.lines[(self.points[self.grid_size][self.grid_size-1],self.points[self.grid_size][self.grid_size])]
        self.cells[self.grid_size-1][self.grid_size-1].has_bottom_wall = False

        self.break_walls_r(0,0)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.cells[i][j].visited = False

    def break_walls_r(self, i, j):
        sleep(0.01)
        self.win.redraw()
        current = self.cells[i][j]
        current.visited = True
        directions = [(0,1), (1,0), (0, -1), (-1, 0)] # right  down  left  up
        # [i][j] = (y,x)
        while directions:
            direction = directions.pop(randint(0, len(directions)-1)) # get random directoin
            h = i + direction[0]
            k = j + direction[1]
            if 0 <= h < self.grid_size and 0 <= k < self.grid_size: # is valid direction
                next = self.cells[h][k]
                if not next.visited: # next not visited yet
                    match direction:
                        case (0,1): # right
                                current.has_right_wall = False
                                next.has_left_wall = False
                                self.win.canvas.delete(self.lines[(self.points[i][j+1],self.points[i+1][j+1])].line_id) # break right wall
                                del self.lines[(self.points[i][j+1],self.points[i+1][j+1])]
                                self.break_walls_r(h, k)
                        case (1,0): # down
                                current.has_bottom_wall = False
                                next.has_top_wall = False
                                self.win.canvas.delete(self.lines[(self.points[i+1][j],self.points[i+1][j+1])].line_id) # break bottom wall
                                del self.lines[(self.points[i+1][j],self.points[i+1][j+1])]
                                self.break_walls_r(h, k)
                        case (0,-1): # left
                                current.has_left_wall = False
                                next.has_right_wall = False
                                self.win.canvas.delete(self.lines[(self.points[i][j],self.points[i+1][j])].line_id) # break left wall
                                del self.lines[(self.points[i][j],self.points[i+1][j])]
                                self.break_walls_r(h, k)
                        case (-1,0): # up
                                current.has_top_wall = False
                                next.has_bottom_wall = False
                                self.win.canvas.delete(self.lines[(self.points[i][j],self.points[i][j+1])].line_id) # break top wall
                                del self.lines[(self.points[i][j],self.points[i][j+1])]
                                self.break_walls_r(h, k)
    
    def solve_r(self, i, j):
        # redraw circle at current cell
        self.win.canvas.delete(self.current_cell.circle_id)
        self.current_cell = Circle(self.offset+(j*self.cell_size)+(self.cell_size//4), self.offset+(i*self.cell_size)+(self.cell_size//4), self.offset+((j+1)*self.cell_size)-(self.cell_size//4), self.offset+((i+1)*self.cell_size)-(self.cell_size//4), self.win.canvas)
        
        self.win.redraw()
        sleep(0.05) # sleep to show the solve steps

        if i == self.grid_size-1 and j == self.grid_size-1: # check if at exit cell
            return True
        
        current = self.cells[i][j]
        current.visited = True

        # [i][j] = (y,x)
        directions = [(0,1), (1,0), (0, -1), (-1, 0)] # right  down  left  up

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
                if 0 <= h < self.grid_size and 0 <= k < self.grid_size: # is valid direction
                    next = self.cells[h][k]
                    if not next.visited: # next not visited yet
                        # draw line from current cell to next cell
                        p1 = Point((self.cell_size+(j*self.cell_size)), (self.cell_size+(i*self.cell_size)))
                        p2 = Point((self.cell_size+(k*self.cell_size)), (self.cell_size+(h*self.cell_size)))
                        self.solve_lines[(self.points[i][j],self.points[h][k])] = Line(p1, p2, self.win.canvas, capstyle="round", fill_color="blue", width=6)
                        if self.solve_r(h,k):
                            return True
                        else:
                            # redraw line in new color to indicate backtracking
                            self.win.canvas.delete(self.solve_lines[(self.points[i][j],self.points[h][k])].line_id)
                            self.solve_lines[(self.points[i][j],self.points[h][k])] = Line(p1, p2, self.win.canvas, capstyle="round", fill_color="red", width=6)
                            # redraw circle at current cell
                            self.win.canvas.delete(self.current_cell.circle_id)
                            self.current_cell = Circle(self.offset+(j*self.cell_size)+(self.cell_size//4), self.offset+(i*self.cell_size)+(self.cell_size//4), self.offset+((j+1)*self.cell_size)-(self.cell_size//4), self.offset+((i+1)*self.cell_size)-(self.cell_size//4), self.win.canvas)
                            self.win.redraw()
                            sleep(.2) # sleep to make backtracking slightly slower

    def solve(self):
        self.current_cell = Circle(self.offset+(self.cell_size//4), self.offset+(self.cell_size//4), self.offset+self.cell_size-(self.cell_size//4), self.offset+self.cell_size-(self.cell_size//4), self.win.canvas)
        if self.solve_r(0, 0):
            print("End Reached")
        else:
            print("End Not Found")

class Cell():
    def __init__(self, x, y): # the cell's (x,y) cords are its top left corner
        self.x = x
        self.y = y
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False