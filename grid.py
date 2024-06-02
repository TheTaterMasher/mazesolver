from random import randint, seed
from time import sleep
from cell import Cell
from graphics import Window, Point, Line, Circle
import csv
import os
from tkinter import BOTH

class Grid():
    def __init__(self, grid_size=4, display_size=1000):
        self.grid_size = grid_size
        self.display_size = display_size
        self.cell_size = display_size // (grid_size + 1)
        self.offset = self.cell_size // 2
        self.win = Window(display_size, self.reset_button_func, self.add_grid_size_button_func, self.remove_grid_size_button_func)
        self.is_solving = False
        self.points = []
        self.cells = []
        self.grid_lines = {}
        self.solve_lines = {}

        # create all points and cells
        for i in range(grid_size + 1): # i values are the y cords
            self.points.append([])
            if not i == grid_size:
                self.cells.append([])
            for j in range(grid_size + 1): # j values are the x cords
                self.points[i].append(Point(j,i))
                if not i == grid_size and not j == grid_size:
                    self.cells[i].append(Cell(j,i))

        # create all grid lines
        for i in range(grid_size + 1):
            for j in range(grid_size + 1):
                if j < grid_size:
                    p1 = Point((self.offset+(j*self.cell_size)), (self.offset+(i*self.cell_size)))
                    p2 = Point((self.offset+((j+1)*self.cell_size)), (self.offset+(i*self.cell_size)))
                    self.grid_lines[(self.points[i][j],self.points[i][j+1])] = Line(p1, p2, self.win.canvas)
                if i < grid_size:
                    p1 = Point((self.offset+(j*self.cell_size)), (self.offset+(i*self.cell_size)))
                    p2 = Point((self.offset+(j*self.cell_size)), (self.offset+((i+1)*self.cell_size)))
                    self.grid_lines[(self.points[i][j],self.points[i+1][j])] = Line(p1, p2, self.win.canvas)
        
        # create the stats file and the header
        if not os.path.exists("stats.csv"):
            with open("stats.csv", "w", newline="") as stats:
                writer = csv.writer(stats)
                field = ["Grid Size", "Solve Length", "Solve Efficiency", "Backtracked Cells", "Backtrack Efficiency"]
                writer.writerow(field)

    def reset_button_func(self):
        # prevent the button from working while a solve is in progress
        if self.is_solving:
            return
        # resets the grid and redraws a maze
        self.reset_grid()
        self.create_maze()
        sleep(0.5)
        # stats stroed in csv file after solve
        results = self.solve()
        with open("stats.csv", "a", newline="") as stats:
            writer = csv.writer(stats) 
            writer.writerow([f"{self.grid_size}", f"{results[0]}", f"{results[1]}", f"{results[2]}", f"{results[3]}"])

    def add_grid_size_button_func(self):
        # prevent the button from working while a solve is in progress
        if self.is_solving:
            return
        # cycle grid size from 4 to 32 by an increment of 4
        self.grid_size += 4
        if self.grid_size >32:
            self.grid_size = 4
        self.reset_grid()
        self.win.add_grid_size_button.pack(fill=BOTH, expand=1)
        self.win.redraw()
    
    def remove_grid_size_button_func(self):
        # prevent the button from working while a solve is in progress
        if self.is_solving:
            return
        # cycle grid size from 4 to 32 by an increment of 4
        self.grid_size -= 4
        if self.grid_size <4:
            self.grid_size = 32
        self.reset_grid()
        self.win.remove_grid_size_button.pack(fill=BOTH, expand=1)
        self.win.redraw()

    def reset_grid(self):
        # reset lines, points and cells
        self.points = []
        self.cells = []
        self.grid_lines = {}
        self.solve_lines = {}

        self.cell_size = self.display_size // (self.grid_size + 1)
        self.offset = self.cell_size // 2

        # reset canvas
        self.win.canvas.delete("all")

        # recreate all points and cells, this is necessary to do if the grid size changes
        for i in range(self.grid_size + 1): # i values are the y cords
            self.points.append([])
            if not i == self.grid_size:
                self.cells.append([])
            for j in range(self.grid_size + 1): # j values are the x cords
                self.points[i].append(Point(j,i))
                if not i == self.grid_size and not j == self.grid_size:
                    self.cells[i].append(Cell(j,i))

        # recreate all grid lines
        for i in range(self.grid_size + 1):
            for j in range(self.grid_size + 1):
                if j < self.grid_size:
                    p1 = Point((self.offset+(j*self.cell_size)), (self.offset+(i*self.cell_size)))
                    p2 = Point((self.offset+((j+1)*self.cell_size)), (self.offset+(i*self.cell_size)))
                    self.grid_lines[(self.points[i][j],self.points[i][j+1])] = Line(p1, p2, self.win.canvas)
                if i < self.grid_size:
                    p1 = Point((self.offset+(j*self.cell_size)), (self.offset+(i*self.cell_size)))
                    p2 = Point((self.offset+(j*self.cell_size)), (self.offset+((i+1)*self.cell_size)))
                    self.grid_lines[(self.points[i][j],self.points[i+1][j])] = Line(p1, p2, self.win.canvas)

    def create_maze(self):
        # break entrance wall
        self.win.canvas.delete(self.grid_lines[(self.points[0][0],self.points[0][1])].line_id)
        del self.grid_lines[(self.points[0][0],self.points[0][1])]
        self.cells[0][0].has_top_wall = False
        
        # break exit wall
        self.win.canvas.delete(self.grid_lines[(self.points[self.grid_size][self.grid_size-1],self.points[self.grid_size][self.grid_size])].line_id)
        del self.grid_lines[(self.points[self.grid_size][self.grid_size-1],self.points[self.grid_size][self.grid_size])]
        self.cells[self.grid_size-1][self.grid_size-1].has_bottom_wall = False

        self.break_walls_r(0,0)

        # reset cells visited state
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
                                self.win.canvas.delete(self.grid_lines[(self.points[i][j+1],self.points[i+1][j+1])].line_id) # break right wall
                                del self.grid_lines[(self.points[i][j+1],self.points[i+1][j+1])]
                                self.break_walls_r(h, k)
                        case (1,0): # down
                                current.has_bottom_wall = False
                                next.has_top_wall = False
                                self.win.canvas.delete(self.grid_lines[(self.points[i+1][j],self.points[i+1][j+1])].line_id) # break bottom wall
                                del self.grid_lines[(self.points[i+1][j],self.points[i+1][j+1])]
                                self.break_walls_r(h, k)
                        case (0,-1): # left
                                current.has_left_wall = False
                                next.has_right_wall = False
                                self.win.canvas.delete(self.grid_lines[(self.points[i][j],self.points[i+1][j])].line_id) # break left wall
                                del self.grid_lines[(self.points[i][j],self.points[i+1][j])]
                                self.break_walls_r(h, k)
                        case (-1,0): # up
                                current.has_top_wall = False
                                next.has_bottom_wall = False
                                self.win.canvas.delete(self.grid_lines[(self.points[i][j],self.points[i][j+1])].line_id) # break top wall
                                del self.grid_lines[(self.points[i][j],self.points[i][j+1])]
                                self.break_walls_r(h, k)
    
    def solve(self):
        self.is_solving = True
        self.current_cell = Circle(self.offset+(self.cell_size//4), self.offset+(self.cell_size//4), self.offset+self.cell_size-(self.cell_size//4), self.offset+self.cell_size-(self.cell_size//4), self.win.canvas)
        
        self.solve_r(0, 0)

        solve_cells_visited = 0
        solve_cells_backtracked = 0

        # reset cells walls and visited state
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.cells[i][j].visited:
                    solve_cells_visited += 1
                    if self.cells[i][j].backtracked:
                        solve_cells_backtracked += 1
                self.cells[i][j].has_left_wall = True
                self.cells[i][j].has_right_wall = True
                self.cells[i][j].has_top_wall = True
                self.cells[i][j].has_bottom_wall = True
                self.cells[i][j].visited = False
                self.cells[i][j].backtracked = False
        solve_eff = int((solve_cells_visited / (self.grid_size**2)) * 100)
        backtrack_eff = int((solve_cells_backtracked / solve_cells_visited) * 100)
        # print("----------------")
        # print(f"total cells: {self.grid_size**2}")
        # print("----------------")
        # print(f"cells in solve: {solve_cells_visited}")
        # print(f"solve eff: {solve_eff}%")
        # print("----------------")
        # print(f"cells backtracked: {solve_cells_backtracked}")
        # print(f"backtracking: {backtrack_eff}%")
        # print("----------------")
        self.is_solving = False
        return solve_cells_visited, solve_eff, solve_cells_backtracked, backtrack_eff

    def solve_r(self, i, j):
        # redraw circle at current cell
        self.win.canvas.delete(self.current_cell.circle_id)
        self.current_cell = Circle(self.offset+(j*self.cell_size)+(self.cell_size//4), self.offset+(i*self.cell_size)+(self.cell_size//4), self.offset+((j+1)*self.cell_size)-(self.cell_size//4), self.offset+((i+1)*self.cell_size)-(self.cell_size//4), self.win.canvas)
        
        self.win.redraw()
        sleep(0.05) # sleep to show the solve steps
        
        current = self.cells[i][j]
        current.visited = True
        
        # check if at exit cell
        if i == self.grid_size-1 and j == self.grid_size-1:
            return True

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
        self.cells[i][j].backtracked = True