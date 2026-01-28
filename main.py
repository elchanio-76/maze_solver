from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str ="black"):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, win: Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1
        self.__win = win

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__win.draw_line(line)
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__win.draw_line(line)
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__win.draw_line(line)
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__win.draw_line(line)
    
    def draw_move(self, to_cell: Cell, undo: bool = False):
        fill_color = "red"
        if undo:
            fill_color = "gray"
        center_x = (self.__x1 + self.__x2) // 2
        center_y = (self.__y1 + self.__y2) // 2
        to_center_x = (to_cell.__x1 + to_cell.__x2) // 2
        to_center_y = (to_cell.__y1 + to_cell.__y2) // 2
        line = Line(Point(center_x, center_y), Point(to_center_x, to_center_y))
        self.__win.draw_line(line, fill_color)
      

def main():
    win = Window(800, 600)
    cell1 = Cell(win)
    cell1.draw(10, 10, 100, 100)
    cell2 = Cell(win)
    cell2.has_left_wall = False
    cell2.draw(100, 10, 200, 100)
    cell3 = Cell(win)
    cell3.has_top_wall = False
    cell3.draw(200, 10, 300, 100)
    cell4 = Cell(win)
    cell4.has_right_wall = False
    cell4.draw(300, 10, 400, 100)
    cell1.draw_move(cell2)
    cell2.draw_move(cell3, True)
    cell3.draw_move(cell4)
    win.wait_for_close()
        
if __name__ == "__main__":
    main()
    