from tkinter import Tk, BOTH, Canvas, Button

class Window():
    def __init__(self, display_size=1000, solve_button_func=None, add_grid_size_button_func=None, remove_grid_size_button_func=None):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.solve_button = Button(text="SOLVE", width=15, height=3, bg="blue", fg="yellow", command=solve_button_func)
        self.add_grid_size_button = Button(text="+4 Grid Size", width=15, height=3, bg="blue", fg="yellow", command=add_grid_size_button_func)
        self.remove_grid_size_button = Button(text="-4 Grid Size", width=15, height=3, bg="blue", fg="yellow", command=remove_grid_size_button_func)
        self.canvas = Canvas(self.__root, bd=5, bg="white", cursor="circle", height=display_size, relief="flat", width=display_size)
        self.canvas.pack(fill=BOTH, expand=1)
        self.solve_button.pack(fill=BOTH, expand=1)
        self.add_grid_size_button.pack(fill=BOTH, expand=1)
        self.remove_grid_size_button.pack(fill=BOTH, expand=1)
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
    def __init__(self, p1, p2, canvas, capstyle="round", fill_color="black", width=6):
        self.p1 = p1
        self.p2 = p2
        self.line_id = canvas.create_line(
            p1.x, p1.y, p2.x, p2.y, capstyle=capstyle, fill=fill_color, width=width
        )

    def __repr__(self):
        return f"Line:({self.p1.x},{self.p1.y}),({self.p2.x},{self.p2.y})"

class Circle():
    def __init__(self, x1, y1, x2, y2, canvas, fill_color="blue"):
        self.circle_id = canvas.create_oval(x1, y1, x2, y2, fill=fill_color)