from tkinter import Tk, BOTH, Canvas
import time
import random

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

    def draw_line(self, line: Line, fill_color: str = "black"):
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
    def __init__(self, win: Window = None):
        """
        Cell constructor. Initialize cell with walls on all sides and no coordinates

        :param self: current Cell object
        :param win: Window object to draw the cell
        :type win: Window
        """
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__y1 = -1
        self.__x2 = -1
        self.__y2 = -1
        self.__win = win
        self.visited = False

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        """
        Draw a cell with the given coordinates (upper left corner and lower right corner)

        :param self: current Cell object
        :param x1: upper left corner x coordinate
        :type x1: int
        :param y1: upper left corner y coordinate
        :type y1: int
        :param x2: lower right corner x coordinate
        :type x2: int
        :param y2: lower right corner y coordinate
        :type y2: int
        """
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.__win is not None:
            line = Line(Point(x1, y1), Point(x1, y2))
            if self.has_left_wall:
                self.__win.draw_line(line, "black")
            else:
                self.__win.draw_line(line, "white")

            line = Line(Point(x1, y1), Point(x2, y1))
            if self.has_top_wall:
                self.__win.draw_line(line, "black")
            else:
                self.__win.draw_line(line, "white")

            line = Line(Point(x1, y2), Point(x2, y2))
            if self.has_bottom_wall:
                self.__win.draw_line(line, "black")
            else:
                self.__win.draw_line(line, "white")

            line = Line(Point(x2, y1), Point(x2, y2))
            if self.has_right_wall:
                self.__win.draw_line(line, "black")
            else:
                self.__win.draw_line(line, "white")

    def draw_move(self, to_cell: Cell, undo: bool = False):
        """
        Draw a line from the center of the current cell to the center of the destination cell

        :param self:Current Cell object
        :param to_cell: Destination Cell object
        :type to_cell: Cell
        :param undo: Use red color if undo is True, otherwise use gray color (backtrace)
        :type undo: bool
        """
        fill_color = "red"
        if undo:
            fill_color = "gray"
        center_x = (self.__x1 + self.__x2) // 2
        center_y = (self.__y1 + self.__y2) // 2
        to_center_x = (to_cell.__x1 + to_cell.__x2) // 2
        to_center_y = (to_cell.__y1 + to_cell.__y2) // 2
        line = Line(Point(center_x, center_y), Point(to_center_x, to_center_y))
        if self.__win is not None:
            self.__win.draw_line(line, fill_color)


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window = None,
        seed: int = None,
    ):
        """
        Maze constructor. Initialize a maze with the given dimensions and cell size

        :param self: current Maze object
        :param x1: x coordinate of the upper left corner of the maze
        :type x1: int
        :param y1: y coordinate of the upper left corner of the maze
        :type y1: int
        :param num_rows: number of rows in the maze
        :type num_rows: int
        :param num_cols: number of columns in the maze
        :type num_cols: int
        :param cell_size_x: width of each cell
        :type cell_size_x: int
        :param cell_size_y: height of each cell
        :type cell_size_y: int
        :param win: Window object to draw the maze
        :type win: Window
        :param seed: random seed for maze generation (used for testing)
        """
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        if seed is not None:
            random.seed(seed)
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        """
        Create a grid of cells for the maze and draw them

        :param self: current Maze object
        """
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i: int, j: int):
        """
        Draw a cell at the specified column and row indices

        :param self: current Maze object
        :param i: column index of the cell
        :type i: int
        :param j: row index of the cell
        :type j: int
        """
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        """
        Redraw the window and pause briefly to create animation effect

        :param self: current Maze object
        """
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.02)

    def __break_entrance_and_exit(self):
        """
        Remove the top wall of the entrance cell (top-left) and the bottom wall of the exit cell (bottom-right)

        :param self: current Maze object
        """
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i: int, j: int):
        """
        Recursively break walls to create a maze using Depth-First Search algorithm

        :param self: current Maze object
        :param i: column index of the current cell
        :type i: int
        :param j: row index of the current cell
        :type j: int
        """
        self.__cells[i][j].visited = True
        while True:
            to_visit = []
            # Check neighboring cells
            if i > 0 and not self.__cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j > 0 and not self.__cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            if to_visit==[]:
                self.__draw_cell(i,j)
                return
            # Pick a random cell to move to
            move = random.randint(0, len(to_visit) - 1)
            next_i, next_j = to_visit[move]
            # Break walls between current cell and chosen cell
            if next_i == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            if next_i == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            if next_j == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False
            if next_j == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            # Recursively visit the chosen cell
            self.__break_walls_r(next_i, next_j)
           

    def __reset_cells_visited(self):
        """
        Reset the visited status of all cells in the maze to False

        :param self: current Maze object
        """
        for col in self.__cells:
            for cell in col:
                cell.visited = False
                
    def _solve_r(self, i: int, j: int) -> bool:
        """
        Recursively solve the maze using Depth-First Search algorithm

        :param self: current Maze object
        :param i: column index of the current cell
        :type i: int
        :param j: row index of the current cell
        :type j: int
        :return: True if the exit is reached, False otherwise
        :rtype: bool
        """
        self.__animate()
        self.__cells[i][j].visited = True
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True  # Exit reached
        # Explore neighboring cells
        directions = [
            (0, -1, 'top', 'bottom'),    # Up
            (1, 0, 'right', 'left'),     # Right
            (0, 1, 'bottom', 'top'),     # Down
            (-1, 0, 'left', 'right')     # Left
        ]
        for di, dj, wall_from, wall_to in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.__num_cols and 0 <= nj < self.__num_rows:
                if not getattr(self.__cells[i][j], f'has_{wall_from}_wall') and not self.__cells[ni][nj].visited:
                    self.__cells[i][j].draw_move(self.__cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    else:
                        self.__cells[i][j].draw_move(self.__cells[ni][nj], undo=True)
        return False
    
    def solve(self) -> bool:
        """
        Solve the maze using Depth-First Search algorithm

        :param self: current Maze object
        :return: True if the exit is reached, False otherwise
        :rtype: bool
        """
        return self._solve_r(0, 0)
    
def main():
    win = Window(800, 600)

    maze = Maze(10, 10, 29, 39, 20, 20, win, seed=42)
    
    result = maze.solve()
    if result:
        print("Maze solved!")
    else:
        print("No solution found.")

    win.wait_for_close()


if __name__ == "__main__":
    main()
