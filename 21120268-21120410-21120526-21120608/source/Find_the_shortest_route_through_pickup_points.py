from Grid import *
from Cell import *
from PathFinder import *

def find_path_with_pickup_points_using_matching(g: Grid, start: Cell, goal: Cell, pickup_points):
    """
    Hàm thực hiện thuật toán ghép để tìm đường đi ngắn nhất từ điểm 
    đầu đến các điểm đón (không phân biệt thứ tự) và sau đó đến đích.

    Args:
        g: Lớp Grid đại diện cho bản đồ.
        start: Ô bắt đầu (Cell).
        goal: Ô kết thúc (Cell).
        pickup_points: Danh sách các điểm đón (Cell).

    Returns:
        Danh sách các ô trên đường đi ngắn nhất (bao gồm điểm đầu, điểm đón và điểm kết thúc).
    """

    # Liệt kê tất cả các hoán vị của các điểm đón
    permutations = find_permutations(pickup_points)

    # Tính toán độ dài đường đi cho mỗi hoán vị
    path_lengths = []
    paths = []
    for permutation in permutations:
        path = [start.id]
        for point in permutation:
            path += AStar(g, g.Grid_cells[path[-1]], point)
            path.append(point.id)
        path += AStar(g, g.Grid_cells[path[-1]], goal)
        path.append(goal.id)
        
        path_cost = calculate_cost(g, path)
        path_lengths.append(path_cost)
        paths.append(path)

    # Chọn hoán vị có đường đi ngắn nhất
    shortest_permutation_index = path_lengths.index(min(path_lengths))
    shortest_path = paths[shortest_permutation_index]
    return shortest_path


def find_permutations(pickup_points):
  """
  Hàm tìm kiếm tất cả các hoán vị của danh sách các điểm đón.

  Args:
      pickup_points: Danh sách các điểm đón (Cell).

  Returns:
      Danh sách chứa tất cả các hoán vị của pickup_points.
  """

  if len(pickup_points) == 0:
    return [[]]  # Trả về danh sách rỗng nếu không có điểm đón

  permutations = []
  for i in range(len(pickup_points)):
    current_point = pickup_points[i]
    remaining_points = pickup_points[:i] + pickup_points[i + 1:]

    # Tìm kiếm hoán vị của các điểm còn lại
    sub_permutations = find_permutations(remaining_points)

    # Thêm điểm hiện tại vào mỗi hoán vị con
    for sub_permutation in sub_permutations:
      permutations.append([current_point] + sub_permutation)

  return permutations