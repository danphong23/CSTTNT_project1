from Grid import Grid
from ReadInput import InputData
import pygame, math

FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS

def get_cell_position(grid: Grid, col: int, row: int) -> tuple[float, float]:
    return ((col + 1) * grid.CELL_SIZE + grid.CELL_SIZE / 2, (grid.height - row) * grid.CELL_SIZE + grid.CELL_SIZE / 2)

def get_cell(grid: Grid, x: float, y: float) -> int:
    col = x // grid.CELL_SIZE - 1
    row = grid.height - y // grid.CELL_SIZE
    if col < 0 or col >= grid.width or row < 0 or row >= grid.height:
        return -1
    return int(row * grid.width + col)

class Player:
    def __init__(self, data: InputData, grid: Grid) -> None:
        (self.x, self.y) = get_cell_position(grid, data.Start[0], data.Start[1])
        self.angle: int = 0 # phải là độ để tính toán cho chính xác
        self.grid: Grid = grid
        self.data: InputData = data

        self.angle_delta: int = 0
        self.angle_times: int = 0

        self.position_delta: tuple[float, float] = (0, 0)
        self.position_times: int = 0

        self.dest_cell: int = 0

        self.path: list[int] = []

    def set_path(self, path: list[int]):
        self.path = path

    def angle_rad(self) -> float:
        return math.radians(self.angle)
    
    def update(self):
        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_LEFT]: self.angle -= 5
        # if keys[pygame.K_RIGHT]: self.angle += 5
        # if keys[pygame.K_UP]:
        #     self.x += math.cos(self.angle_rad()) * 5
        #     self.y += math.sin(self.angle_rad()) * 5
        # if keys[pygame.K_DOWN]:
        #     self.x -= math.cos(self.angle_rad()) * 5
        #     self.y -= math.sin(self.angle_rad()) * 5
        def wrap(x, a, b) -> int:
            return (x - a) % (b - a) + a # ép số x vào trong phạm vi [a, b] nhất định
        
        if self.angle_times != 0 and self.angle_delta != 0: # không có angle_delta không có nghĩa là không tốn thời gian xoay
            self.angle = (self.angle + self.angle_delta) % 360 # có thể vượt quá 360 độ và khiến xoay nhiều lần
            
            self.angle_times -= 1
        elif self.position_times != 0:
            self.x += self.position_delta[0]
            self.y += self.position_delta[1] # curse you

            self.position_times -= 1
        elif self.dest_cell < len(self.path) - 1:
            self.dest_cell += 1

            (row, col) = divmod(get_cell(self.grid, self.x, self.y), self.grid.width) # lấy hàng và cột (tương ứng phần nguyên và phần dư)
            
            cell = divmod(self.grid.Grid_cells[self.path[self.dest_cell]].id, self.grid.width)
            cell = (cell[1], cell[0]) # đảo ngược lại, từ (hàng, cột) thành (cột, hàng)

            self.angle_times = 45 # vì di chuyển 8 hướng, và mỗi góc như thế đều là bội của 45 độ
            
            dest_angle = math.degrees(math.atan2(-(cell[1] - row), cell[0] - col)) # meth
            self.angle_delta = wrap(int((dest_angle - self.angle) / self.angle_times), -4, 4) # giới hạn để xoay tối đa 180 độ

            position_dest = get_cell_position(self.grid, cell[0], cell[1])

            self.position_times = 10 
            self.position_delta = ((position_dest[0] - self.x) / self.position_times, (position_dest[1] - self.y) / self.position_times)
            
    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 8)
        pygame.draw.line(surface, (0, 255, 0), (self.x, self.y), (self.x + math.cos(self.angle_rad()) * 50, self.y + math.sin(self.angle_rad()) * 50) , 3)
        pygame.draw.line(surface, (0, 255, 0), (self.x, self.y), (self.x + math.cos(self.angle_rad() - HALF_FOV) * 50, self.y + math.sin(self.angle_rad() - HALF_FOV) * 50), 3)
        pygame.draw.line(surface, (0, 255, 0), (self.x, self.y), (self.x + math.cos(self.angle_rad() + HALF_FOV) * 50, self.y + math.sin(self.angle_rad() + HALF_FOV) * 50), 3)
        self.cast_rays(surface)

    def cast_rays(self, surface: pygame.Surface):
        start_angle = self.angle_rad() - HALF_FOV
        MAX_DEPTH = int(self.data.Num_Cols * self.grid.CELL_SIZE)
        SCALE = (self.data.SCREEN_WIDTH) / CASTED_RAYS

        for ray in range(CASTED_RAYS):
            for depth in range(MAX_DEPTH):
                target_x = self.x + math.cos(start_angle) * depth
                target_y = self.y + math.sin(start_angle) * depth

                square = get_cell(self.grid, target_x, target_y)
                
                if square == -1 or not self.grid.Grid_cells[square].passable:
                    pygame.draw.line(surface, (255, 255, 0), (self.x, self.y), (target_x - math.copysign(2, math.cos(start_angle)), target_y - math.copysign(2, math.sin(start_angle))))
                    
                    depth *= math.cos(self.angle_rad() - start_angle)
                    
                    intensity = 512 / (1 + depth * depth * 0.0001)  # Adjust 128 to change the intensity
                    # Create the custom color using the base (128, 128, 64) and the calculated intensity
                    
                    color = (min(26 + intensity, 255), min(44 + intensity, 193), min(66 + intensity, 162))
                    wall_height = 21000 / (depth + 0.0001)
                    # wall_height = self.data.Num_Hight
                    
                    pygame.draw.rect(surface, color, (self.data.SCREEN_WIDTH + ray * (SCALE) -1, (self.data.SCREEN_HEIGHT / 2) - wall_height / 2, SCALE + 1, wall_height)) # trừ 1 do có kẽ hở
                    
                    break
        
            start_angle += STEP_ANGLE