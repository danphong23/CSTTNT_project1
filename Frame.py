from Const import *
from Cell import *
from Polygon import *
from Grid import *

class Frame: 
    def __init__(self, space: Grid, sc: pygame.Surface) -> None:
        self.space = space
        self.sc = sc
        self.time_out = 0
        self.previous_positon = space.Start

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
        if path is not []:
            if len(path) > 1:
                cell:Cell = self.space.Grid_cells[path[1]]
            else:
                cell:Cell = self.space.Grid_cells[path[0]] 
            self.previous_positon = cell
            if self.space.arrived_goal(cell):
                self.space.update_start(cell)
                self.space.draw(self.sc)
                return "arrived"
            self.space.arraived_pickup_point(cell)
            if cell.passable:
                self.space.update_start(cell)
                path.pop(1)
                self.space.draw(self.sc)
                return True
            if cell.rect.x == self.previous_positon.rect.x:
                self.time_out += 1
            if self.time_out == 3:
                self.time_out = 0
                return "delay"
        return False