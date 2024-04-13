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
from Player import Player
from Sprite import *

def main(data: InputData, read_args: Read_arg):
    pygame.init()
    pygame.display.set_caption('project1 - ')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH * 2, data.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(GREY))
    
    sprite_list = []
    g = Grid(data)
    g.draw(sc)
    pygame.display.flip()

    clock.tick(200)

    # gọi hàm sử dụng trạng thái hiển thị 2D hay 3D
    Change_space(g, sc, read_args.space)

    q = Queue()
    result = None
    # gọi đa nhiệm chạy mức độ chương trình
    thread0 = threading.Thread(target=Level_implementation(g, sc, read_args, q))
    thread0.start()

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
        # Vẽ hoạt ảnh cho pick up cell
        for i in range(0, len(g.pickup_points)):
            g.pickup_points[i].draw(sc)
            sprite_list[i].draw()

        if result == None:
            if not q.empty():
                result = q.get_nowait()
                player.set_path(result)
                # Tạo text hiển thị chi phí
                #text = font.render(f"Cost: {result[1]:.2f}", True, BLACK)
        else:
            player.update()
            player.draw(sc)

        pygame.display.flip()

def main_level_4(data: InputData):
    pygame.init()
    pygame.display.set_caption('project1 - ')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH * 2, data.SCREEN_HEIGHT))
    sc.fill(pygame.color.Color(BLACK))

    space = Grid(data)
    space.draw(sc)
    pygame.display.flip()

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
    player = Player(data, space)
    
    # Xử lý sự kiện
    while True:
        agent.update()
        player.update()
        player.draw(sc)
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
    #data.readInput("input.txt")
    data.readInput("input_level_4.txt")
    data.printData()

    main(data, read_args)