from time import sleep
from maze import Maze
from graphics import Window

def main():
    offset = 40
    grid_size = 9
    cell_size = 80
    window = Window(800, 800)
    for n in range(10):
        maze = Maze(offset, offset,  grid_size , grid_size, cell_size, cell_size, window, seed=None)
        maze._solve()
        sleep(1)
        window.canvas.delete("all")
    
main()