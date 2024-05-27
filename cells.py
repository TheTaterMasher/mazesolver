from graphics import Line, Point
class Cell():
    def __init__(self, x1, x2, y1, y2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._visited = False
        self._center = ((x1 + (abs(x2 - x1) // 2)), (y1 + (abs(y2 - y1) // 2)))
        self._win = win
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y1)
        self.p3 = Point(x1, y2)
        self.p4 = Point(x2, y2)
    
    def draw(self):
        left = Line(self.p1, self.p3)
        top = Line(self.p1, self.p2)
        right = Line(self.p2, self.p4)
        bottom = Line(self.p3, self.p4)
        if self.has_left_wall:
            self._win.draw_line(left)
        else:
            self._win.draw_line(left, "white")
        if self.has_top_wall:
            self._win.draw_line(top)
        else:
            self._win.draw_line(top, "white")
        if self.has_right_wall:
            self._win.draw_line(right)
        else:
            self._win.draw_line(right, "white")
        if self.has_bottom_wall:
            self._win.draw_line(bottom)
        else:
            self._win.draw_line(bottom, "white")

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        p1 = Point(self._center[0], self._center[1])
        p2 = Point(to_cell._center[0], to_cell._center[1])
        line = Line(p1, p2)
        self._win.draw_line(line, fill_color=color)