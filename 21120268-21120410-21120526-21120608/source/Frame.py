from Const import *
from Cell import *
from Polygon import *
from Grid import *
from Find_the_shortest_route_through_pickup_points import *
import pygame
from queue import Queue
from PathFinder import *

class Frame: 
    def __init__(self, space: Grid, sc: pygame.Surface) -> None:
        self.space = space
        self.sc = sc
        self.time_out = 0
        self.previous_positon = space.Start
        self.cost = 0

    def update_new_frame(self):
        for polygon in self.space.Polygons.polygons:
            polygon.reset_polygon()
            polygon.reset_unsafe_points()
            points = []
            for point in polygon.points:
                x, y = point
                a, b = polygon.velocity
                if x + a < 0 or x + a >= self.space.width or y + b < 0 or y + b >= self.space.height:
                    polygon.velocity = [-a, -b]
                    if len(polygon.points) == 3:
                        if a == 0:
                            polygon.points = [polygon.points[1], polygon.points[2], polygon.points[0]]
                        else:
                            polygon.points = [polygon.points[2], polygon.points[0], polygon.points[1]]
                    else:
                        if a == 0:
                            polygon.points = [polygon.points[2], polygon.points[3], polygon.points[0], polygon.points[1]]
                        else:
                            polygon.points = [polygon.points[3], polygon.points[0], polygon.points[1], polygon.points[2]]
                        break
            for point in polygon.points:
                x, y = point
                a, b = polygon.velocity
                x += a
                y += b    
                point = (x, y)
                points.append(point)
            polygon.points = points
            polygon.init_edge(self.space.Grid_cells)
            polygon.set_passable_polygon(self.space.Grid_cells, False)
            polygon.update_unsafe_points()
        
        self.space.draw(self.sc)
        
    def update_agent(self, path):
        if path != []:
            if len(path) > 1:
                cell:Cell = self.space.Grid_cells[path[1]]
            else:
                cell:Cell = self.space.Grid_cells[path[0]] 
            self.previous_positon = cell
            if self.space.arrived_goal(cell):
                self.space.update_start(cell)
                show_cost(self.cost)
                self.space.draw(self.sc)
                return "arrived"
            self.space.arraived_pickup_point(cell)
            if cell.passable:
                self.cost += self.space.update_start(cell)
                show_cost(self.cost)
                path.pop(1)
                self.space.draw(self.sc)
                return True
            if cell.rect.x == self.previous_positon.rect.x:
                self.time_out += 1
            if self.time_out == 3:
                self.time_out = 0
                return "delay"
        return False
    


# Tìm đường đi mới
def find_new_path(queue_request: Queue, queue_response: Queue, g: Grid, algorithm: str):
    while True:
        # Đợi yêu cầu tìm đường
        _ = queue_request.get()

        path = []
        # path = AStar(g, g.Start, g.Goal)
        #path = find_path_with_pickup_points_using_matching(g, g.Start, g.Goal, space.pickup_points)
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

        # Tìm đường đi khởi đầu
        self.queue_request.put(1)

        while True:
            if not self.queue_response.empty():
                self.path = self.queue_response.get()
                break

        draw_path(self.space, self.sc, self.path, YELLOW)
        # pygame.display.flip()
        clear_path(self.space, self.sc, self.path)
        # pygame.display.flip()

    def update(self):
        if self.is_arrived is not True:
            # self.count += 1
            # if self.count % 2 == 0:
            self.frame.update_new_frame()
            # pygame.display.flip()
            if self.delay == 0:
                result = self.frame.update_agent(self.path)
                if result == False:
                    self.queue_request.put(1)
                    self.path = []
                if result == "delay":
                    self.delay = 5
            else:
                self.delay -= 1
            pygame.time.delay(100)
            if not self.queue_response.empty():
                self.path = self.queue_response.get()
                draw_path(self.space, self.sc, self.path, YELLOW)
                # pygame.display.flip()
                clear_path(self.space, self.sc, self.path)
                self.count = 0
            # pygame.display.flip()
