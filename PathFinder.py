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
    start_id = g.Start.id # lấy id của ô bắt đầu
    goal_id = g.Goal.id # lấy id của ô kết thúc

    # Tạo một map để lưu trữ các ô theo id
    cell_dict = {cell.id: cell for cell in g.Grid_cells}
    start_cell = cell_dict[start_id]
    goal_cell = cell_dict[goal_id]

    # Khởi tạo open set với hàng đợi ưu tiên
    open_set = []
    heapq.heappush(open_set, (0, start_id))

    # Lưu vết đường đi
    came_from = [-1] * g.get_num_cells()

    # Khởi tạo giá trị g_score và f_score cho mỗi ô
    g_score = {cell_id: float("inf") for cell_id in cell_dict}
    g_score[start_id] = 0
    f_score = {cell_id: float("inf") for cell_id in cell_dict}
    f_score[start_id] = h(start_cell, goal_cell)

    # Khởi tạo danh sách các ô đã thăm dò
    closed_set = set()

    while open_set:
        # Lấy ô có f_score nhỏ nhất trong open set
        _, current_id = heapq.heappop(open_set)
        current_cell = cell_dict[current_id]

        # Nếu ô hiện tại là đích
        if current_id == goal_id:
            path = find_path(came_from, goal_id)
            draw_path(g, sc, path, YELLOW)
            cost = calculate_cost(g, path)
            show_cost(cost, sc)
            return

        # Thêm ô hiện tại vào tập đã thăm dò
        closed_set.add(current_id)

        # Xem xét các ô lân cận
        for neighbor in g.get_neighbors(current_cell):
            neighbor_id = neighbor.id
            if neighbor_id in closed_set:
                continue

            if current_cell.rect.x == neighbor.rect.x or current_cell.rect.y == neighbor.rect.y:
                cost = CELL_SIZE + CELL_SPACING
            else:
                cost = math.sqrt(2) * (CELL_SIZE + CELL_SPACING)
            # Tính giá trị g_score mới
            tentative_g_score = g_score[current_id] + cost

            # Nếu ô lân cận có giá trị g_score mới tốt hơn hoặc chưa thăm dò
            is_opened = any(id == neighbor_id for _, id in open_set)
            if tentative_g_score < g_score[neighbor_id] or not is_opened:
                # Cập nhật thông tin của ô lân cận
                came_from[neighbor_id] = current_id
                g_score[neighbor_id] = tentative_g_score
                f_score[neighbor_id] = g_score[neighbor_id] + h(cell_dict[neighbor_id], goal_cell)
                # Thêm ô lân cận vào open set
                if not is_opened:
                    heapq.heappush(open_set, (f_score[neighbor_id], neighbor_id))
                else: 
                    index = next((i for i, (_, id) in enumerate(open_set) if id == neighbor_id), None)
                    if index is not None:
                        open_set[index] = (f_score[neighbor_id], neighbor_id)
                        heapq.heapify(open_set)

    # Nếu không tìm được đường đi
    print("Không tìm được đường đi")

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
    n_center_x = n.rect.x + CELL_SIZE / 2
    n_center_y = n.rect.y + CELL_SIZE / 2
    goal_center_x = goal.rect.x + CELL_SIZE / 2
    goal_center_y = goal.rect.y + CELL_SIZE / 2
    return math.sqrt((n_center_x - goal_center_x)**2 + (n_center_y - goal_center_y)**2)

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