import math
import pygame
from Const import *
from Polygon import *
from Grid import *
from Cell import *
import heapq

# tìm kiếm theo chiều rộng
def BFS(g: Grid, sc: pygame.Surface):
    """Thực hiện thuật toán BFS trên lưới g."""

    open_set = [g.Start.id]  # Danh sách các ô cần thăm dò
    closed_set = []  # Tập hợp các ô đã thăm dò (dùng set để kiểm tra nhanh hơn)
    father = [-1] * g.get_num_cells()  # Lưu vết đường đi

    while open_set:
        current_id = open_set.pop(0)  # Lấy ô đầu tiên trong danh sách
        current = g.Grid_cells[current_id]

        if g.is_goal(current):  # Nếu đã đến đích
            # tìm danh sách các cell trên đường đi
            path = find_path(father, g.Goal.id)
            draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
            # tính chi phí đường đi
            cost = calculate_cost(g, path)

            # vẽ chi phí lên màn hình
            show_cost(cost, sc)
            
            return

        closed_set.append(current_id)  # Đánh dấu ô đã thăm dò

        neighbors = g.get_neighbors(current)
        for neighbor in neighbors:  # Xem xét các ô lân cận
            neighbor_id = neighbor.id
            if neighbor_id not in open_set and neighbor_id not in closed_set:
                open_set.append(neighbor_id)  # Thêm ô lân cận chưa thăm dò vào danh sách
                father[neighbor_id] = current_id  # Lưu vết đường đi

    print("Không tìm được đường đi")  # Nếu không tìm ra đích

# Tìm kiếm theo chiều sâu
def DFS(g: Grid, sc: pygame.Surface):
    """Thực hiện thuật toán DFS trên lưới g."""

    open_stack = [g.Start.id]  # Stack chứa các ô cần thăm dò
    closed_set = []  # Tập hợp các ô đã thăm dò (dùng set để kiểm tra nhanh hơn)
    father = [-1] * g.get_num_cells()  # Lưu vết đường đi

    while open_stack:
        current_id = open_stack.pop()  # Lấy ô cuối cùng trong stack
        current = g.Grid_cells[current_id]

        if g.is_goal(current):  # Nếu đã đến đích
            # tìm danh sách các cell trên đường đi
            path = find_path(father, g.Goal.id)
            draw_path(g, sc, path, YELLOW)  # Vẽ đường đi
            # tính chi phí đường đi
            cost = calculate_cost(g, path)

            # vẽ chi phí lên màn hình
            show_cost(cost, sc)
            
            return

        closed_set.append(current_id)  # Đánh dấu ô đã thăm dò

        neighbors = g.get_neighbors(current)
        for neighbor in neighbors:  # Xem xét các ô lân cận
            neighbor_id = neighbor.id
            if neighbor_id not in open_stack and neighbor_id not in closed_set:
                open_stack.append(neighbor_id)  # Thêm ô lân cận chưa thăm dò vào stack
                father[neighbor_id] = current_id  # Lưu vết đường đi

    print("Không tìm được đường đi")  # Nếu không tìm ra đích


# Tìm kiếm đồng nhất (UCS - Uniform Cost Search) 
def UCS(g: Grid, sc: pygame.Surface):
    pass

# Tìm kiếm A* (A-Star) 
def AStar(g: Grid, sc: pygame.Surface):
    pass

# hàm tìm danh sách thứ tự đường đi từ đầu đến đích
def find_path(father, node_id):
    path = []
    # truy ngược đường đi
    current_id = node_id
    while current_id != -1:
        path.append(current_id)
        current_id = father[current_id]
    path.reverse()

    return path

# hàm vẽ đường đi từ đầu đến đích
def draw_path(g: Grid, sc: pygame.Surface, path, color):
    # Tìm đường đi từ ô kết thúc đến ô bắt đầu
    g.Start._set_color(GREEN)
    g.Start.draw(sc)
    g.Goal._set_color(BLUE)
    g.Goal.draw(sc)

    # Vẽ đường đi trên màn hình
    for i in path[1:len(path)-1]:
        cell:Cell = g.Grid_cells[i]
        cell.set_color(color, sc, 15)

# hàm trả về khoảng cách giữa 2 cell (chi phí heuristic)
def h(n: Cell, goal: Cell):
    return math.sqrt((n.rect.x - goal.rect.x)**2 + (n.rect.y - goal.rect.y)**2)

# hàm tìm chi phí đường đi từ đầu đến đích
def calculate_cost(g:Grid, path):
    """
    Tính chi phí của đường đi dựa trên danh sách ID các ô.

    Args:
        path: Danh sách ID các ô trên đường đi.
        grid: Lưới ô vuông.

    Returns:
        Chi phí của đường đi.
    """
    cost = 0.0
    for i in range(len(path) - 1):
        current_cell = g.Grid_cells[path[i]]
        next_cell = g.Grid_cells[path[i + 1]]

        # Đi thẳng
        if current_cell.rect.x == next_cell.rect.x or current_cell.rect.y == next_cell.rect.y:
            cost += 1.0
        # Đi chéo
        else:
            cost += 1.5

    return cost

# hàm hiển thị chi phí từ đầu đến đích
def show_cost(cost, sc: pygame.Surface):
    """
    Cập nhật chi phí đường đi lên màn hình.

    Args:
        sc: Màn hình pygame để vẽ.
        cost: Chi phí đường đi.
    """
    # Cài đặt font chữ
    font = pygame.font.SysFont("Arial", 20)

    # Tạo text hiển thị chi phí
    text = font.render(f"Cost: {cost:.2f}", True, BLACK)

    # Vẽ text lên màn hình
    sc.blit(text, (10, 10))

    # Cập nhật màn hình
    pygame.display.flip()