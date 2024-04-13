from ReadInput import InputData
from Const import *
from Polygon import *
from Grid import *
from Cell import *
import pygame
import threading
import sys
from PathFinder import *
from Find_the_shortest_route_through_pickup_points import *
from Read_Command_line_parameters import *


def main(data: InputData, read_args:Read_arg):
    pygame.init()
    print(read_args.name)
    pygame.display.set_caption(f'project1 - {read_args.name}')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH, data.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(BLACK))
    pygame.display.flip()
    
    g = Grid(data)
    g.draw(sc)

    clock.tick(200)

    # gọi hàm sử dụng trạng thái hiển thị 2D hay 3D
    Change_space(g, sc, read_args.space)

    # gọi đa nhiệm chạy mức độ chương trình
    thread0 = threading.Thread(target=Level_implementation(g, sc, read_args))
    thread0.start()
    
    # Xử lý sự kiện
    while True:
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
    data.printData()

    main(data, read_args)