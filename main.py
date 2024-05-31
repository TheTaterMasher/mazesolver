from random import randint
from time import sleep
from grid import Grid

def main():
    grid = Grid(9, 1000)
    grid.win.wait_for_close()

main() 