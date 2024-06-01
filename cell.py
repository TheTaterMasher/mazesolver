class Cell():
    def __init__(self, x, y): # the cell's (x,y) cords are its top left corner
        self.x = x
        self.y = y
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.backtracked = False