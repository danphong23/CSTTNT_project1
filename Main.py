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

# test chức năng tìm đường đi
def Function_Search(g: Grid, sc: pygame.Surface):
    path = []
    # test ở đây, 
    # path = DFS(g, sc)
    # path = BFS(g, sc)
    # path = UCS(g, sc)
    path = AStar(g, sc)

    # thực hiện vẽ đường đi ở đây
    draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
    # tính chi phí đường đi
    cost = calculate_cost(g, path)

    # vẽ chi phí lên màn hình
    show_cost(cost, sc)


# Tìm đường đi mới
def find_path(queue_request, queue_response, space, sc):
    while True:
        # Đợi yêu cầu tìm đường
        _ = queue_request.get()

        path = []
        path = AStar(space, sc)

        # Trả về đường đi
        queue_response.put(path)

class Agent:
    def __init__(self, space: Grid, sc: pygame.Surface, frame: Frame, path, queue_request: Queue, queue_response: Queue):
        self.count = 0
        self.delay = 0
        self.is_arrived = False
        self.space = space
        self.sc = sc
        self.frame = frame
        self.path = path
        self.queue_request = queue_request
        self.queue_response = queue_response

    def update(self):
        if self.is_arrived is not True:
            self.frame.update_new_frame()
            pygame.display.flip()
            if self.delay == 0:
                result = self.frame.update_agent(self.path)
                if result == False:
                    self.queue_request.put(1)
                    self.path = []
                if result == "delay":
                    self.delay = 5
            else:
                self.delay -= 1
            pygame.time.delay(200)
            if not self.queue_response.empty():
                self.path = self.queue_response.get()
                draw_path(self.space, self.sc, self.path, YELLOW)
                pygame.display.flip()
                clear_path(self.space, self.sc, self.path)
            pygame.display.flip()

def main(data):
    pygame.init()
    pygame.display.set_caption(f'project1')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH,data.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(GREY))
    pygame.display.flip()
    
    space = Grid(data)
    space.draw(sc)

    frame = Frame(space, sc)

    #clock.tick(200)

    # Function_Search()
    # gọi đa nhiệm 
    #thread0 = threading.Thread(target=Function_Search(space, sc))
    #thread0.start()

    # Queue gửi và nhận dữ liệu
    queue_request = Queue()
    queue_response = Queue()

    # Đa nhiệm tìm đường
    thread0 = threading.Thread(target=find_path, args=(queue_request, queue_response, space, sc))
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

# ===========================================================
if __name__=='__main__':
    # Đọc dữ liệu từ Input.txt
    data = InputData()
    data.readInput("input.txt")
    data.printData()

    main(data)