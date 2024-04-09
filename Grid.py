import pygame
from Const import *
from Cell import Cell
from ReadInput import InputData
from Polygon import *


class Grid:
    def __init__(self, input: InputData) -> None:
        """
        Khởi tạo một lưới ô vuông.

        Args:
            input: Đối tượng Input chứa thông tin về bản đồ.
        """
        self.width = input.Num_Cols
        self.height = input.Num_Rows
        self.cell_size = input.Num_Cols*input.Num_Rows
        self.Grid_cells = []  # Danh sách các ô vuông
        self.Start = None  # Ô bắt đầu (S)
        self.Goal = None  # Ô kết thúc (G)
        pickup_points = [] # danh sách các điểm đón
        # self.Polygons = []  # Danh sách các đa giác

        # Tạo danh sách các ô vuông
        for i in range(self.height):
            for j in range(self.width):
                # j*(A+A1)+BOUND, i*(A+A1)+BOUND, A, i*COLS+j, is_brick
                x = j * (CELL_SIZE + CELL_SPACING) + FRAME_THICKNESS
                y = (self.height -1 - i) * (CELL_SIZE + CELL_SPACING) + FRAME_THICKNESS
                id = j + i * self.width 
                cell = Cell(x, y, CELL_SIZE, id)
                self.Grid_cells.append(cell)

        # Xác định ô bắt đầu và kết thúc
        self.Start:Cell = self.Grid_cells[input.Start[0] + input.Start[1] * self.width]
        self.Start._set_color(GREEN)
        self.Goal:Cell = self.Grid_cells[input.Goal[0] + input.Goal[1] * self.width]
        self.Goal._set_color(BLUE)

        # Xác Định các điểm đón nếu có
        for p in input.Pickup_Points:
            x = p[0]
            y = p[1]
            id = x + y * self.width
            cell:Cell = self.Grid_cells[id]
            cell._set_color(PURPLE)
            pickup_points.append(cell)

        # Tạo danh sách các đa giác
        self.Polygons = List_Polygon(input.Polygons, self.Grid_cells, self.width)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Vẽ các ô lưới, đa giác, điểm bắt đầu, điểm kết thúc, các điểm đón lên màn hình.

        Args:
            screen: Màn hình pygame để vẽ.
        """
        for cell in self.Grid_cells:
            cell.draw(screen)

        pygame.display.flip()
    # Các hàm khác...

    def get_num_cells(self) -> int:
        """
        Lấy số lượng các ô trong lưới.

        Returns:
            Số lượng các ô trong lưới.
        """
        return len(self.Grid_cells)

    def is_goal(self, cell: Cell) -> bool:
        """
        Kiểm tra ô đó có phải là điểm kết thúc không.

        Args:
            cell: Ô cần kiểm tra.

        Returns:
            True nếu ô là điểm kết thúc, False nếu không.
        """
        return cell.id == self.Goal.id

    def get_neighbors(self, cell: Cell):
        """
        Lấy các ô hàng xóm có thể đi được của 1 ô bất kỳ.
        """
        x = cell.id % self.width
        y = cell.id // self.width

        directions = [(0,1), (0,-1), (1,0), (-1,0), (-1,1), (-1,-1), (1,1), (1,-1)]
        # directions = [(0,1), (0,-1), (-1,0), (1,0)]
        
        neighbors = []
        for (dx, dy) in directions:
            # Tính toán tọa độ Cell lân cận
            next_x = x + dx
            next_y = y + dy
            id_cell = next_x + next_y*self.width if 0 <= next_y < self.height and 0 <= next_x < self.width else None
            if id_cell is not None and self.Grid_cells[id_cell].passable:
                neighbors.append(self.Grid_cells[id_cell])

        return neighbors