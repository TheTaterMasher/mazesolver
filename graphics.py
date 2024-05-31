from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, bd=5, bg="white", cursor="circle", height=height, relief="flat", width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.active = False
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.active = True

        while self.active:
            self.redraw()

    def close(self):
        self.active = False

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Line():
    def __init__(self, p1, p2, canvas, capstyle="round", fill_color="black", width=8):
        self.line_id = canvas.create_line(
            p1.x, p1.y, p2.x, p2.y, capstyle=capstyle, fill=fill_color, width=width
        )

class Circle():
    def __init__(self, x1, y1, x2, y2, canvas, fill_color="blue"):
        self.circle_id = canvas.create_oval(x1, y1, x2, y2, fill=fill_color)