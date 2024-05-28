from time import sleep
from maze import Maze
from graphics import Window

def main():
    win_size = 800
    num_cells = 32
    grid_size = win_size // num_cells
    cell_size = win_size // grid_size
    offset = cell_size // 2
    window = Window(win_size + offset, win_size + offset)
    for n in range(1):
        maze = Maze(offset, offset,  grid_size , grid_size, cell_size, cell_size, window, seed=None)
        maze._solve()
        sleep(2)
        window.canvas.delete("all")

main()