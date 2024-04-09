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
    # test ở đây, 
    # DFS(g, sc)
    #BFS(g, sc)
    UCS(g, sc)
    # AStar(g, sc)
    

def main(data):
    pygame.init()
    pygame.display.set_caption(f'project1')
    sc = pygame.display.set_mode((data.SCREEN_WIDTH,data.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(GREY))
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