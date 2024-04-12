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

# test chức năng tìm đường đi
def Function_Search(g: Grid, sc: pygame.Surface):
    path = []
    # test ở đây, 
    # path = DFS(g, g.Start, g.Goal)
    # path = BFS(g, g.Start, g.Goal)
    # path = UCS(g, g.Start, g.Goal)
    # path = AStar(g, g.Start, g.Goal)
    path = find_path_with_pickup_points_using_matching(g, g.Start, g.Goal, g.pickup_points)

    # thực hiện vẽ đường đi ở đây
    draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
    # tính chi phí đường đi
    cost = calculate_cost(g, path)
    # vẽ chi phí lên màn hình
    show_cost(cost, sc)


def main_level_4(data):
    pygame.init()
    pygame.display.set_caption(f'project1')
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
    thread0.start()

    # Tìm đường đi khởi đầu
    path = []
    queue_request.put(1)

    while True:
        if not queue_response.empty():
            path = queue_response.get()
            break

    draw_path(space, sc, path, YELLOW)
    pygame.display.flip()
    clear_path(space, sc, path)
    pygame.display.flip()

    agent = Agent(space, sc, frame, path, queue_request, queue_response)
    
    # Xử lý sự kiện
    while True:
        agent.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main(data):
    pygame.init()
    pygame.display.set_caption(f'project1')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH,data.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(BLACK))
    pygame.display.flip()
    
    space = Grid(data)
    space.draw(sc)

    clock.tick(200)

    # Function_Search()
    # gọi đa nhiệm 
    thread0 = threading.Thread(target=Function_Search(space, sc))
    thread0.start()
    
    # Xử lý sự kiện
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# ===========================================================
if __name__=='__main__':
    # Đọc dữ liệu từ Input.txt
    data = InputData()
    # data.readInput("input.txt")
    data.readInput("input_level_4.txt")
    data.printData()

    # main(data)
    main_level_4(data)
    # nhớ sửa lại kích thước Cell trong Const trước khi test