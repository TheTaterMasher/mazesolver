from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, bg="white", height=height, width=width, )
        self.canvas.pack(fill=BOTH, expand=1)
        self.active = False
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.active = True

        while self.active:
            self.redraw()

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

    def draw_circle(self, x1, y1, x2, y2):
        self.canvas.create_oval(x1, y1, x2, y2)

    def close(self):
        self.active = False

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
