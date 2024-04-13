import pygame
from Const import *
from Cell import Cell
from Polygon import *
import math
import random

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
        self.velocity = [0, random.choice([-1, 1])] # vận tốc di chuyển của đa giác
        self.inside_points_ids = [] # id các cell nằm trong đa giác
        self.grid_cell = Grid_cell # danh sách các cell trên lưới
        self.unsafe_points = [] # id các cell không an toàn
        self.poly_width = 0 # chiều rộng của đa giác

        # chứa tất cả các điểm thuộc đa giác
        # self.points_in_polygon = []

        # khởi tạo các đỉnh
        self.init_edge(Grid_cell)

        # đặt các cell trong đa giác là không đi qua được 
        self.set_passable_polygon(Grid_cell, False)

        self.calculate_width()

    # hàm khởi tạo các cạnh của đa giác
    def init_edge(self, Grid_cell):
        # đặt các điểm trên đa giác là không đi qua được và đổi màu
        for point in self.points:
            x, y = point
            Grid_cell[x + y*self.width].set_passable(False)
            Grid_cell[x + y*self.width]._set_color(RED)
            self.inside_points_ids.append(x + y*self.width)


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
                self.inside_points_ids.append(id)
                

        # lấy đường thẳng nối điểm cuối với điểm đầu
        A = self.points[-1] # điểm cuối danh sách
        B = self.points[0]
        points_in_line = self.points_in_line(A, B)
        for id in points_in_line:
            Grid_cell[id].set_passable(False)
            Grid_cell[id]._set_color(self.color)
            self.inside_points_ids.append(id)


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
    def set_passable_polygon(self, Grid_cell, value):
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

            if Grid_cell[x + y * self.width].passable is not value:
                queue.append((x, y))
                break

        # Lặp lại cho đến khi không còn điểm nào trong danh sách cần kiểm tra
        while len(queue) > 0:
            # Lấy điểm đầu tiên trong danh sách cần kiểm tra
            point = queue.pop(0)
            if Grid_cell[point[0] + point[1] * self.width].passable is not value:
                continue

            # Đánh dấu điểm đã được thăm
            Grid_cell[point[0] + point[1] * self.width].set_passable(value)
            self.inside_points_ids.append(point[0] + point[1] * self.width)
            #Grid_cell[point[0] + point[1] * self.width]._set_color(BLACK)

            # Kiểm tra các điểm lân cận
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x = point[0] + dx
                y = point[1] + dy

                # Kiểm tra điểm lân cận có nằm trong đa giác hay không
                if 0 <= x < self.width and 0 <= y < self.height and Grid_cell[x + y * self.width].passable is not value:
                    # Thêm điểm lân cận vào danh sách cần kiểm tra
                    queue.append((x, y))

    def reset_polygon(self):
        for id in self.inside_points_ids:
            self.grid_cell[id].set_passable(True)
            self.grid_cell[id]._set_color(WHITE)
        
        for point in self.points:
            x, y = point
            self.grid_cell[x + y*self.width].set_passable(True)
            self.grid_cell[x + y*self.width]._set_color(WHITE)

        self.set_passable_polygon(self.grid_cell, True)
        self.inside_points_ids = []
        

    def update_unsafe_points(self):
        a, b = self.velocity
        # for vertical only
        width = self.poly_width
        if a == 0:
            if b == 1:
                self.move_up(width)
                if self.is_near_top() > 0:
                    self.move_down(self.is_near_top())
            
            if b == -1:
                self.move_down(width)
                if self.is_near_bottom() > 0:
                    self.move_up(self.is_near_bottom())
        
    
    def reset_unsafe_points(self):
        for id in self.unsafe_points:
            self.grid_cell[id].set_passable(True)
            self.grid_cell[id]._set_color(WHITE)
        self.unsafe_points = []
                

    def calculate_width(self):
        points = self.inside_points_ids
        cells = []
        for point in points:
            x = point % self.width
            y = point // self.width
            cells.append((x, y))
        # find the lowest x-coordinate and highest x-coordinate to calculate the width
        min_x = min(cells, key=lambda x: x[0])[0]
        max_x = max(cells, key=lambda x: x[0])[0]
        self.poly_width = max_x - min_x + 2

    def get_two_highest_points(self):
        points = self.inside_points_ids
        cells = []
        for point in points:
            x = point % self.width
            y = point // self.width
            cells.append((x, y))
        # find the cell with the highest y-coordinate with the lowest x-coordinate
        highest_point = max(cells, key=lambda x: (x[1], -x[0]))
        # find the cell with the highest y-coordinate with the highest x-coordinate
        highest_point2 = max(cells, key=lambda x: (x[1], x[0]))
        
        if highest_point[0] == highest_point2[0]:
            for point in self.points:
                if not point[0] == highest_point[0]:
                    return highest_point, point
        if highest_point[0] < highest_point2[0]:
            return highest_point, highest_point2
        return highest_point2, highest_point
    
    def get_two_lowest_points(self):
        points = self.inside_points_ids
        cells = []
        for point in points:
            x = point % self.width
            y = point // self.width
            cells.append((x, y))
        # find the cell with the lowest y-coordinate with the lowest x-coordinate
        lowest_point = min(cells, key=lambda x: (x[1], -x[0]))
        # find the cell with the lowest y-coordinate with the highest x-coordinate
        lowest_point2 = min(cells, key=lambda x: (x[1], x[0]))
        if lowest_point[0] == lowest_point2[0]:
            for point in self.points:
                if not point[0] == lowest_point2[0]:
                    return point, lowest_point2
        if lowest_point[0] < lowest_point2[0]:
            return lowest_point, lowest_point2
        return lowest_point2, lowest_point
    
    def move_up(self, width):
        us_width = width
        first_point, second_point = self.get_two_highest_points()
        top_first_point = first_point
        top_second_point = second_point
        if top_first_point[1] > top_second_point[1]:
            us_width = 2
        for i in range(1, us_width):
            if first_point[1] + i < self.height:
                top_first_point = (top_first_point[0], top_first_point[1] + 1)
                self.unsafe_points.append(first_point[0] + (first_point[1] + i) * self.width)
            lines = self.points_in_line(top_first_point, top_second_point)
            self.unsafe_points.extend(lines)
        for id in self.unsafe_points:
            self.grid_cell[id].set_passable(False)
            #self.grid_cell[id]._set_color(ORANGE)

    def move_down(self, width):
        us_width = width
        first_point, second_point = self.get_two_lowest_points()
        bottom_first_point = first_point
        bottom_second_point = second_point
        if bottom_first_point[1] < bottom_second_point[1]:
            us_width = 2
        for i in range(1, us_width):
            if first_point[1] - i >= 0:
                bottom_first_point = (bottom_first_point[0], bottom_first_point[1] - 1)
                self.unsafe_points.append(first_point[0] + (first_point[1] - i) * self.width)
        lines = self.points_in_line(bottom_first_point, bottom_second_point)
        self.unsafe_points.extend(lines)

        for id in self.unsafe_points:
            self.grid_cell[id].set_passable(False)
            #self.grid_cell[id]._set_color(ORANGE)

    def is_near_top(self):
        height = 0 
        for point in self.points:
            if point[1] + self.poly_width >= self.height:
                if point[1] + self.poly_width - self.height > height:
                    height = point[1] + self.poly_width - self.height
        if height == 0:
            return 0
        return height

    def is_near_bottom(self):
        height = 0
        for point in self.points:
            if point[1] - self.poly_width < 0:
                if self.poly_width - point[1] > height:
                    height = self.poly_width - point[1]
        if height == 0:
            return 0
        return height

class List_Polygon:
    def __init__(self, list_points, Grid_cell, width):
        self.polygons = []
        for i in range(len(list_points)):
            p = Polygon(list_points[i], Grid_cell, width)
            self.polygons.append(p)
