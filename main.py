from time import sleep
from maze import Maze
from graphics import Window

def main():
    offset = 20
    grid_size = 27
    cell_size = 40
    window = Window(1200, 1200)
    for n in range(1):
        maze = Maze(offset, offset,  grid_size , grid_size, cell_size, cell_size, window, seed=None)
        maze._solve()
        sleep(1)
        window.canvas.delete("all")
    
main()