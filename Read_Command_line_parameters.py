import argparse

# định nghĩa một lớp Read_arg dùng để đọc tham số dòng lệnh.
class Read_arg:
    def __init__(self):
        """
        đọc tham số dòng lệnh
        """
        # tên chương trình
        # vd: Normal - BFS
        # vd: Find the shortest route through pickup points
        # vd: Moving Polygon - DFS
        # vd: 3D - Astar
        self.name = ''

        # mức độ:
        # normal = "n"
        # pickup_points = 'pk'
        # moving_polygon = "mp"
        # three_dimensional_space = "3d"
        self.level = ''

        # tên thuật toán: BFS, DFS, UCS, AStar
        self.algorithm = ''

        # Tạo trình phân tích cú pháp dòng lệnh
        parser = argparse.ArgumentParser(description='Wayfinding robots')

        # Thêm tùy chọn dòng lệnh
        parser.add_argument('--level', type=str, required=True, help='Level: : normal = n \n pickup_points = pk\n moving_polygon = mp\n three_dimensional_space = 3d',)
        parser.add_argument('--algor', type=str, help='algorithm: DFS, BFS, UCS, AStar', default='DFS')


        # Xử lý các đối số dòng lệnh
        args = parser.parse_args()
        
        # gán giá trị vào các biến
        self.init(args)


    

    def init(self, args):
        # gán các giá trị:
        self.level = args.level
        self.algorithm = args.algor

        # kiểm tra lỗi
        self.check_err()

        # đặt tên chương trình
        if self.level == Level.normal:
            self.name = f"normal - {self.algorithm}"
        elif self.level == Level.pickup_points:
            self.name = "Find the shortest route through pickup points"
        elif self.level == Level.moving_polygon:
            self.name = f"Moving polygon - {self.algorithm}"
        elif self.level == Level.three_dimensional_space:
            self.name = f"3D  - {self.algorithm}"
        
        
    # hàm kiểm tra lỗi các biến
    def check_err(self):
        try:
            self.check_level()
        except ValueError as e:
            raise NotImplementedError(e)
            

    def check_level(self):
        try:
            l = Level(self.level)
        except ValueError:
            raise ValueError("Invalid level please select: normal = n \n pickup_points = pk\n moving_polygon = mp\n three_dimensional_space = 3d")


class Level(enumerate):
    normal = "n"
    pickup_points = "pk"
    moving_polygon = "r"
    three_dimensional_space = "3d"
