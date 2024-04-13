import pygame
from Const import *

# định nghĩa một lớp Cell dùng để mô phỏng một ô vuông trong một môi trường 2D.
class Cell:
    def __init__(self, x, y, size, id, passable = True):
        """
        Khởi tạo một ô vuông.

        Args:
            x: Tọa độ x của ô vuông trên màn hình.
            y: Tọa độ y của ô vuông trên màn hình.
            size: Độ dài cạnh của ô vuông.
            id: ID của ô vuông.
            passable: nếu đi qua được passable = True
        """
        # self.x = x
        # self.y = y
        # self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.id = id
        self.passable = passable
        self.color = WHITE

    def draw(self, screen):
        """
        Vẽ ô vuông lên màn hình.

        Args:
            screen: Màn hình pygame để vẽ.
        """
        # tô nền Cell
        pygame.draw.rect(screen, self.color, self.rect)
        # tô viền Cell
        pygame.draw.rect(screen, BLACK, self.rect, CELL_SPACING)


    def set_passable(self, passable):
        self.passable = passable

    def _set_color(self, color):
        self.color = color

    def set_color(self, color, screen, delay=0):
        """
        Đổi màu và cập nhật màu của ô vuông lên màn hình.

        Args:
            color: Màu mới của ô vuông.
            screen: Màn hình pygame để cập nhật.
            speed: Thời gian đổi màu (delay).
        """
        self.color = color
        self.draw(screen)
        if delay > 0:
            pygame.time.delay(delay)
        pygame.display.update()