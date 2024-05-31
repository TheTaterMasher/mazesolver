from random import randint
from time import sleep
from grid import Grid

def main():
    grid = Grid(32, 1200)
    grid.win.active = True
    grid.create_maze()
    grid.win.redraw()
    sleep(0.5)
    grid.solve()
    grid.win.wait_for_close()

main()