from ReadInput import InputData
from Const import *
from Polygon import *
from Grid import *
from Cell import *
import pygame
import threading
import sys
from PathFinder import *
from Frame import *
from queue import Queue
from Find_the_shortest_route_through_pickup_points import *
from Read_Command_line_parameters import *

# test chức năng tìm đường đi (algorithm = BFS, DFS, USC, AStar)
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
        path = AStar(g, g.Start, g.Goal)

    # thực hiện vẽ đường đi ở đây
    draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
    # tính chi phí đường đi
    cost = calculate_cost(g, path)

    # vẽ chi phí lên màn hình
    show_cost(cost, sc)
    
    

def main(data: InputData):
    pygame.init()
    pygame.display.set_caption(f'project1 - ')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH,data.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(BLACK))
    pygame.display.flip()
    
    space = Grid(data)
    space.draw(sc)

    clock.tick(200)

    # Function_Search()
    # gọi đa nhiệm 
    thread0 = threading.Thread(target=Function_Search_normal(space, sc, 'AStar'))
    thread0.start()
    
    # Xử lý sự kiện
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_level_4(data: InputData):
    pygame.init()
    pygame.display.set_caption(f'project1 - ')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH,data.SCREEN_HEIGHT))
    sc.fill(pygame.color.Color(BLACK))
    pygame.display.flip()

    space = Grid(data)
    space.draw(sc)

    frame = Frame(space, sc)

    # Queue gửi và nhận dữ liệu
    queue_request = Queue()
    queue_response = Queue()

    # Đa nhiệm tìm đường
    thread0 = threading.Thread(target=find_new_path, args=(queue_request, queue_response, space, sc))
    thread0.daemon = True
    thread0.start()

    path = []

    agent = Agent(space, sc, frame, path, queue_request, queue_response)
    
    # Xử lý sự kiện
    while True:
        agent.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# ===========================================================
if __name__=='__main__':
    # lấy tham số dòng lệnh
    # read_args = Read_arg()
    # Đọc dữ liệu từ Input.txt
    data = InputData()
    #data.readInput("input.txt")
    data.readInput("input_level_4.txt")
    data.printData()
    
    #main(data)
    main_level_4(data)