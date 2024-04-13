import argparse
from enum import Enum
from Grid import *
from Cell import *
from PathFinder import *
from Find_the_shortest_route_through_pickup_points import *
from Frame import *
from ReadInput import InputData
import threading

# python main.py --level n/pk/mp [--algor BFS/DFS/UCS/AStar] [--space 2D/3D]
# ex: python main.py --level n --algor BFS --space 3D
# ở trong ô vuông có thể nhập hoặc không
# nếu thuật toán không nhập mặc định là DFS
# nếu không gian không nhập thì mặc định là 2D

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
        self.name = ''

        # không gian hiển thị (2D, 3D)
        self.space = '2D'

        # mức độ:
        # normal = "n"
        # pickup_points = 'pk'
        # moving_polygon = "mp"
        self.level = ''

        # tên thuật toán: BFS, DFS, UCS, AStar
        self.algorithm = ''

        # Tạo trình phân tích cú pháp dòng lệnh
        parser = argparse.ArgumentParser(description='Wayfinding robots')

        # Thêm tùy chọn dòng lệnh
        parser.add_argument('--level', type=str, required=True, help=f'Level: : normal = {Level.normal.value} \n pickup_points = {Level.pickup_points.value}\n moving_polygon = {Level.moving_polygon.value}')
        parser.add_argument('--algor', type=str, help='algorithm: DFS, BFS, UCS, AStar', default='DFS')
        parser.add_argument('--space', type=str, help='space: 3D, 2D', default='2D')


        # Xử lý các đối số dòng lệnh
        args = parser.parse_args()
        
        # gán giá trị vào các biến
        self.init(args)


    

    def init(self, args):
        # gán các giá trị:
        self.level = args.level
        self.algorithm = args.algor
        self.space = args.space
        print(args)

        # kiểm tra lỗi
        self.check_err()

        # đặt tên chương trình
        self.name = self.get_name()
        
    
    # lấy tên chương trình:
    def get_name(self):
        if self.level == Level.normal.value:
            return f'normal - {self.algorithm}'
        elif self.level == Level.pickup_points.value:
            return 'Find the shortest route through pickup points'
        elif self.level == Level.moving_polygon.value:
            return f'Moving polygon - {self.algorithm}'
        
    # hàm kiểm tra lỗi các biến
    def check_err(self):
        try:
            self.check_level()
            self.check_algorithm()
        except ValueError as e:
            raise NotImplementedError(e)
            

    def check_level(self):
        try:
            l = Level(self.level)
        except ValueError:
            raise ValueError(f"Invalid level please select:\n normal = {Level.normal.value} \n pickup_points = {Level.pickup_points.value}\n moving_polygon = {Level.moving_polygon.value}")
    def check_algorithm(self):
        try:
            l = Algor(self.algorithm)
        except ValueError:
            raise ValueError(f"Invalid algorithm:\n {Algor._member_names_}")

    def check_space(self):
        try:
            l = Level(self.level)
        except ValueError:
            raise ValueError(f"Invalid level please select:\n normal = {Level.normal.value} \n pickup_points = {Level.pickup_points.value}\n moving_polygon = {Level.moving_polygon.value}")

class Level(Enum):
    normal = 'n'
    pickup_points = 'pk'
    moving_polygon = 'mp'
    
class Algor(Enum):
    DFS = 'DFS'
    BFS = 'BFS'
    UCS = 'UCS'
    AStar = 'AStar'

# chạy Mức độ
def Level_implementation(g: Grid, sc: pygame.surface, read_args:Read_arg):
    if read_args.level == Level.normal.value:
        Function_Search_normal(g, sc, read_args.algorithm)
    elif read_args.level == Level.pickup_points.value:
        Function_Search_Pickup_points(g, sc)


# đổi không gian hiển thị (space = 2D / 3D)
def Change_space(g: Grid, sc: pygame.surface, space:str):
    if space == '2D':
        # TODO
        pass
    elif space == '3D':
        # TODO
        pass

# chức năng tìm đường đi (algorithm = BFS, DFS, USC, AStar)
def Function_Search_normal(g: Grid, sc: pygame.Surface, algorithm: str):
    # path = find_path_with_pickup_points_using_matching(g, g.Start, g.Goal, g.pickup_points)
    path = []
    if(algorithm == 'DFS'):
        path = DFS(g, g.Start, g.Goal)
    elif(algorithm == 'BFS'):
        path = BFS(g, g.Start, g.Goal)
    elif(algorithm == 'UCS'):
        path = UCS(g, g.Start, g.Goal)
    elif(algorithm == 'AStar'):
        path = AStar(g, g.Start, g.Goal)
    else:
        path = DFS(g, g.Start, g.Goal)

    # thực hiện vẽ đường đi ở đây
    draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
    # tính chi phí đường đi
    cost = calculate_cost(g, path)

    # vẽ chi phí lên màn hình
    show_cost(cost, sc)

# Chức năng tìm đường đi ngắn nhất đi qua tất cả điểm đón
def Function_Search_Pickup_points(g: Grid, sc: pygame.Surface):
    if g.pickup_points == [] or len(g.pickup_points) <=0:
        raise NotImplementedError(f"Can't search for pickup points")
    # vẽ các điểm đón lên màn hình
    g.draw_pickup_points(sc)
    
    # thực hiện tìm đường đi
    path = find_path_with_pickup_points_using_matching(g, g.Start, g.Goal, g.pickup_points)
    # thực hiện vẽ đường đi
    draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
    # tính chi phí đường đi
    cost = calculate_cost(g, path)

    # vẽ chi phí lên màn hình
    show_cost(cost, sc)

