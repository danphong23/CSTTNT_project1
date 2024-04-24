from Const import *
class InputData:
    def __init__(self):
        self.Num_Cols = 0  # số cột (kích thước ngang)
        self.Num_Rows = 0  # số hàng (kích thước dọc)
        self.Num_Hight = 0  # kích thước cao (nếu có)
        self.Start = (0, 0)  # tọa độ điểm bắt đầu (x1, y1)
        self.Goal = (0, 0)  # tọa độ điểm kết thúc (x2, y2)
        self.Pickup_Points = []  # danh sách tọa độ các điểm đón ([(x1,y1), (x2,y2),…]) (nếu có)
        self.Polygons = []  # danh sách các danh sách các tọa độ điểm của đa giác 
                            # [[(x1,y1), (x2, y2), (x3, y3),...], [(x1,y1), (x2, y2), (x3, y3),...],... ]
        self.SCREEN_WIDTH = (self.Num_Cols * 25) + 2 * 25   # Chiều rộng của màn hình
        self.SCREEN_HEIGHT = (self.Num_Rows * 25) + 2 * 25 # Chiều cao của màn hình
        self.CELL_SIZE = 25


    def readInput(self, filename: str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            dimensions = list(map(int, lines[0].strip().split(',')))
            self.Num_Cols, self.Num_Rows = dimensions[:2]
            
            # tính toán độ dài của Cell và kích thước màn hình
            self.calculate_screen_dimensions()

            if len(dimensions) > 2:
                self.Num_Hight = dimensions[2]
            coordinates = list(map(int, lines[1].strip().split(',')))
            self.Start = tuple(coordinates[:2])
            self.Goal = tuple(coordinates[2:4])
            if len(coordinates) > 4:
                self.Pickup_Points = [tuple(coordinates[i:i+2]) for i in range(4, len(coordinates), 2)]
            
            num_polygons = int(lines[2].strip())
            polygon_lines = lines[3:3 + num_polygons]
            self.Polygons = []
            for polygon_line in polygon_lines:
                polygon_coords = list(map(int, polygon_line.strip().split(',')))
                # Chuyển đổi từng tọa độ thành tuple và tạo danh sách
                polygon_as_tuples = [(coord[0], coord[1]) for coord in zip(*[iter(polygon_coords)] * 2)]
                self.Polygons.append(polygon_as_tuples)

    def printData(self):
        print(f"Kích thước ngang: {self.Num_Cols}")
        print(f"Kích thước dọc: {self.Num_Rows}")
        print(f"kích thước ngang màn hình: {self.SCREEN_WIDTH}")
        print(f"kích thước dọc màn hình: {self.SCREEN_HEIGHT}")
        if self.Num_Hight != 0:
            print(f"Kích thước cao: {self.Num_Hight}")
        print(f"Điểm bắt đầu: {self.Start}")
        print(f"Điểm kết thúc: {self.Goal}")
        if self.Pickup_Points:
            print(f"Các điểm đón: {self.Pickup_Points}")
        print("Các đa giác:")
        for i, polygon in enumerate(self.Polygons, 1):
            print(f"Đa giác {i}: {polygon}")


    def calculate_screen_dimensions(self):
        """
        Tính toán kích thước màn hình phù hợp (SCREEN_WIDTH, SCREEN_HEIGHT)
        """
        # Tính toán kích thước màn hình ban đầu
        self.SCREEN_WIDTH = (self.Num_Cols * self.CELL_SIZE) + 2 * self.CELL_SIZE
        self.SCREEN_HEIGHT = (self.Num_Rows * self.CELL_SIZE) + 2 * self.CELL_SIZE

        # Kiểm tra xem chiều rộng màn hình có vượt quá kích thước tối đa hay không
        if self.SCREEN_WIDTH > SCREEN_WIDTH_MAX:
            # Tính toán lại kích thước ô vuông (CELL_SIZE)
            new_cell_size = SCREEN_WIDTH_MAX // (self.Num_Cols + 2 * self.CELL_SIZE / self.CELL_SIZE)
            # Cập nhật kích thước ô vuông
            self.CELL_SIZE = new_cell_size

            # Tính toán lại kích thước màn hình với kích thước ô vuông mới
            self.SCREEN_WIDTH = (self.Num_Cols * new_cell_size) + 2 * self.CELL_SIZE
            self.SCREEN_HEIGHT = (self.Num_Rows * new_cell_size) + 2 * self.CELL_SIZE

        # Kiểm tra xem chiều cao màn hình có vượt quá kích thước tối đa hay không
        if self.SCREEN_HEIGHT > SCREEN_HEIGHT_MAX:
            # Tính toán lại kích thước ô vuông (CELL_SIZE)
            new_cell_size = SCREEN_HEIGHT_MAX // (self.Num_Rows + 2 * self.CELL_SIZE / self.CELL_SIZE)
            # Cập nhật kích thước ô vuông
            self.CELL_SIZE = new_cell_size

            # Tính toán lại kích thước màn hình với kích thước ô vuông mới
            self.SCREEN_WIDTH = (self.Num_Cols * new_cell_size) + 2 * self.CELL_SIZE
            self.SCREEN_HEIGHT = (self.Num_Rows * new_cell_size) + 2 * self.CELL_SIZE