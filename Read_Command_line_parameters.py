import argparse
from enum import Enum
from Grid import *
from Cell import *
from PathFinder import *
from Find_the_shortest_route_through_pickup_points import *
from queue import Queue
from Player import Player
import sys

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

        # kiểm tra lỗi
        self.check_err()

        # đặt tên chương trình
        self.name = self.get_name()
        
    
    # lấy tên chương trình:
    def get_name(self):
        if self.level == Level.normal.value:
            return f'normal - {self.algorithm} - {self.space}'
        elif self.level == Level.pickup_points.value:
            return f'Find the shortest route through pickup points - {self.space}'
        elif self.level == Level.moving_polygon.value:
            return f'Moving polygon - {self.algorithm} - {self.space}'
        
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
            raise ValueError(f"Invalid level please select:\n normal = {Level.normal.value} \n pickup_points = {Level.pickup_points.value}\n moving_polygon = {Level.moving_polygon.value}")

    def check_space(self):
        try:
            l = Level(self.level)
        except ValueError:
            raise ValueError(f"Invalid level please select:\n normal = {Level.normal.value} \n pickup_points = {Level.pickup_points.value}\n moving_polygon = {Level.moving_polygon.value}")

    def is_3D(self):
        return self.space == '3D'

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
def Level_implementation(g: Grid, sc: pygame.surface, read_args:Read_arg, q: Queue):
    if read_args.level == Level.normal.value:
        q.put(Function_Search_normal(g, sc, read_args.algorithm))
    elif read_args.level == Level.pickup_points.value:
        q.put(Function_Search_Pickup_points(g, sc))
    # elif read_args.level == Level.moving_polygon.value:
    #     Function_Search_moving_polygon(g, sc, read_args.algorithm)

# đổi không gian hiển thị (space = 2D / 3D)
def Change_space(g:Grid, sc:pygame.surface, data:InputData, q:Queue, space:str='2D'):
    if space == '2D':
        # TODO
        pass
    elif space == '3D':
        result = None
        player = Player(data, g)
        # Xử lý sự kiện
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            sc.fill(pygame.color.Color((133, 251, 253)))
            pygame.draw.rect(sc, BLACK, (data.SCREEN_WIDTH, 0, data.SCREEN_WIDTH, data.SCREEN_HEIGHT // 2))
            g.draw(sc)

            if result == None:
                if not q.empty():
                    result = q.get_nowait()
                    player.set_path(result)
                    # Tạo text hiển thị chi phí
                    #text = font.render(f"Cost: {result[1]:.2f}", True, BLACK)
                else:
                    break
            else:
                player.update()
                player.draw(sc)

            pygame.display.flip()

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
    show_cost(cost)
    return path

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
    show_cost(cost)
    return path

# # Chức năng tìm đường đi (algorithm = BFS, DFS, USC, AStar), với các đa giác di chuyển
# def Function_Search_moving_polygon(g: Grid, sc: pygame.Surface, algorithm: str):
#     # TODO
#     pass
#Cảnh báo: Không nên chạy 3D cho thuật toán Moving Polygon!!!