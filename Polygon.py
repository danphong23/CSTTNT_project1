import pygame
from Const import *
from Cell import Cell
from Polygon import *
import math

# ***********************************************************************************************************
# MỨC 4: khi thực hiện di chuyển đa giác thì chỉ cần di chuyển các đỉnh đa giác sau đó vẽ lại đa giác
# Lưu ý: khi các đa giác di chuyển thì phải đặt lại thuộc tính passable của các cell thuộc đa giác trước
#        khi di chuyển là True sau đó mới di chuyển và đặt các thuộc tính passable của các cell 
#        thuộc đa giác sau khi di chuyển là False
# *** có thể viết 1 hàm thực hiện việc di chuyển đa giác sau đó thực hiện gọi đa 
#       nhiệm để không ảnh hưởng đến chương trình
# *** vấn đề là có sự ảnh hưởng của tốc độ di chuyển (delay) của nhân vật tìm đường, tốc độ di chuyển của các đa giác
# *** di chuyển đa giác tới lui thì dễ nhưng thuật toán chạy đúng thì khó
# ***********************************************************************************************************

# ta chỉ xét đa giác lồi
class Polygon:
    def __init__(self, points, Grid_cell, width):
        """
        Khởi tạo một đa giác.

        Args:
            points: Danh sách các điểm tọa độ (ô vuông) theo chiều kim đồng hồ.
            Grid_cell: Danh sách các ô vuông trên lưới.
        """
        self.points = points
        self.color = GREY
        self.width = width # số cột
        self.height = len(Grid_cell)//width

        # chứa tất cả các điểm thuộc đa giác
        # self.points_in_polygon = []

        # khởi tạo các đỉnh
        self.init_edge(Grid_cell)

        # đặt các cell trong đa giác là không đi qua được 
        self.set_passable_polygon(Grid_cell)

    # hàm khởi tạo các cạnh của đa giác
    def init_edge(self, Grid_cell):
        # đặt các điểm trên đa giác là không đi qua được và đổi màu
        for point in self.points:
            x, y = point
            Grid_cell[x + y*self.width].set_passable(False)
            Grid_cell[x + y*self.width]._set_color(RED)


        # lấy các đường thẳng nối các điểm
        for i in range(len(self.points) - 1):
            A = self.points[i]
            B = self.points[i + 1]
            # Sử dụng hàm points_in_line để lấy danh sách các điểm trên đường thẳng nối A và B
            points_in_line = self.points_in_line(A, B)
            # Tô màu các Cell tương ứng với các điểm trên đường thẳng
            for id in points_in_line:
                Grid_cell[id].set_passable(False)
                Grid_cell[id]._set_color(self.color)

        # lấy đường thẳng nối điểm cuối với điểm đầu
        A = self.points[-1] # điểm cuối danh sách
        B = self.points[0]
        points_in_line = self.points_in_line(A, B)
        for id in points_in_line:
            Grid_cell[id].set_passable(False)
            Grid_cell[id]._set_color(self.color)


                
    # hàm xác định danh sách các id Cell nằm trên đưởng thẳng nối 2 điểm A, B
    def points_in_line(self, A, B):
        """
        Hàm trả về danh sách các điểm nằm trên đường thẳng đi qua hai điểm A và B.

        Tham số:
            A: Tuple (x1, y1) đại diện cho điểm đầu tiên.
            B: Tuple (x2, y2) đại diện cho điểm thứ hai.

        Trả về:
            Danh sách các điểm nằm trên đường thẳng.
        """

        # Xác định trường hợp đặc biệt

        if A[0] == B[0]:  # Đường thẳng thẳng đứng
            return [(A[0] + y* self.width) for y in range(min(A[1] + 1, B[1] + 1), max(A[1], B[1]))]
        elif A[1] == B[1]:  # Đường thẳng nằm ngang
            return [(x + A[1] * self.width) for x in range(min(A[0] + 1, B[0] + 1), max(A[0], B[0]))]

        # Tính hệ số a và b của phương trình y = ax + b

        a = (B[1] - A[1]) / (B[0] - A[0])
        b = A[1] - a * A[0]

        # Tính các điểm trên đường thẳng

        x1 = min(A[0], B[0])
        x2 = max(A[0], B[0])
        lines = []
        for i in range(x1 + 1, x2):
            y = a * i + b
            # y = math.floor(y)
            y = round(y)
            lines.append(i + y * self.width)
        y1 = min(A[1], B[1])
        y2 = max(A[1], B[1])
        for y in range(y1 + 1, y2):
            x = (y - b) / a
            x = round(x)
            lines.append(x + y * self.width)

        return lines

    #  thuật toán Flood Fill 
    def set_passable_polygon(self, Grid_cell):
        """
        Set passable các cell nằm trong đa giác là False.

        Tham số:
            polygon: Danh sách các điểm tọa độ (ô vuông) theo chiều kim đồng hồ.
            Grid_cell: Danh sách các ô vuông trên lưới.
            width: Số cột của lưới.

        """
        # Khởi tạo danh sách các điểm cần kiểm tra
        queue = []

        # Tìm điểm seed nằm trong đa giác
        p1 = self.points_in_line(self.points[1], self.points[2])
        x1 = p1[len(p1)//2] % self.width
        y1 = p1[len(p1)//2] // self.width
        seeds = self.points_in_line(self.points[0], (x1,y1))
        
        for seed in seeds:
            x = seed % self.width
            y = seed // self.width

            if Grid_cell[x + y * self.width].passable:
                queue.append((x, y))
                break

        # Lặp lại cho đến khi không còn điểm nào trong danh sách cần kiểm tra
        while len(queue) > 0:
            # Lấy điểm đầu tiên trong danh sách cần kiểm tra
            point = queue.pop(0)
            if not Grid_cell[point[0] + point[1] * self.width].passable:
                continue

            # Đánh dấu điểm đã được thăm
            Grid_cell[point[0] + point[1] * self.width].set_passable(False)
            # Grid_cell[point[0] + point[1] * self.width]._set_color(BLACK)

            # Kiểm tra các điểm lân cận
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x = point[0] + dx
                y = point[1] + dy

                # Kiểm tra điểm lân cận có nằm trong đa giác hay không
                if 0 <= x < self.width and 0 <= y < self.height and Grid_cell[x + y * self.width].passable:
                    # Thêm điểm lân cận vào danh sách cần kiểm tra
                    queue.append((x, y))

class List_Polygon:
    def __init__(self, list_points, Grid_cell, width):
        self.polygons = []
        for i in range(len(list_points)):
            p = Polygon(list_points[i], Grid_cell, width)
            self.polygons.append(p)
