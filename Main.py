from ReadInput import InputData
from Const import *
from Polygon import *
from Grid import *
from Cell import *
import pygame
import threading
import sys
from PathFinder import *

# test chức năng tìm đường đi
def Function_Search(g: Grid, sc: pygame.Surface):
    path = []
    # test ở đây, 
    # path = DFS(g, g.Start, g.Goal)
    # path = BFS(g, g.Start, g.Goal)
    # path = UCS(g, g.Start, g.Goal)
    path = AStar(g, g.Start, g.Goal)

    # thực hiện vẽ đường đi ở đây
    draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
    # tính chi phí đường đi
    cost = calculate_cost(g, path)

    # vẽ chi phí lên màn hình
    show_cost(cost, sc)
    
    

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
    data.readInput("input.txt")
    data.printData()

    main(data)