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


def main(data: InputData, read_args: Read_arg):
    pygame.init()
    pygame.display.set_caption(f'project1 - {read_args.name}')
    
    if read_args.is_3D():
        sc = pygame.display.set_mode((data.SCREEN_WIDTH * 2, data.SCREEN_HEIGHT))
    else:
        sc = pygame.display.set_mode((data.SCREEN_WIDTH, data.SCREEN_HEIGHT))
        
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(BLACK))
    # sc.fill(pygame.color.Color(GREY))
    
    g = Grid(data)
    g.draw(sc)
    # g.draw_pickup_points(sc)

    pygame.display.flip()
    clock.tick(200)

    q = Queue()   
    # gọi đa nhiệm chạy mức độ chương trình
    thread0 = threading.Thread(target=Level_implementation(g, sc, read_args, q))
    thread0.daemon = True
    thread0.start()

    # gọi hàm sử dụng trạng thái hiển thị 2D hay 3D
    thread1 = threading.Thread(target=Change_space(g, sc, data, q, read_args.space))
    thread1.daemon = True
    thread1.start()
    
    # Xử lý sự kiện
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def main_level_4(data: InputData, read_args:Read_arg):
    pygame.init()
    pygame.display.set_caption(f'project1 - {read_args.name}')

    sc = pygame.display.set_mode((data.SCREEN_WIDTH, data.SCREEN_HEIGHT))

    # if read_args.is_3D():
    #     sc = pygame.display.set_mode((data.SCREEN_WIDTH * 2, data.SCREEN_HEIGHT))
    # else:
    #     sc = pygame.display.set_mode((data.SCREEN_WIDTH, data.SCREEN_HEIGHT))

    sc.fill(pygame.color.Color(BLACK))

    space = Grid(data)
    space.draw(sc)

    # gọi hàm sử dụng trạng thái hiển thị 2D hay 3D
    # Change_space(space, sc, read_args.space)
    pygame.display.flip()
    
    frame = Frame(space, sc)

    # Queue gửi và nhận dữ liệu
    queue_request = Queue()
    queue_response = Queue()

    # Đa nhiệm tìm đường
    thread0 = threading.Thread(target=find_new_path, args=(queue_request, queue_response, space, read_args.algorithm))
    thread0.daemon = True
    thread0.start()
    
    global path
    path = []

    agent = Agent(space, sc, frame, path, queue_request, queue_response)
    # player = Player(data, space)
    
    # Xử lý sự kiện
    while True:
        agent.update()
        # player.update()
        # player.draw(sc)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# ===========================================================
if __name__=='__main__':
    # lấy tham số dòng lệnh
    read_args = Read_arg()
    # Đọc dữ liệu từ Input.txt
    data = InputData()
    data.readInput("input.txt")
    # data.readInput("input_level_4.txt")
    data.printData()

    # main(data, read_args)
    if(read_args.level == Level.moving_polygon.value):
        main_level_4(data, read_args)
    else:
        main(data, read_args)