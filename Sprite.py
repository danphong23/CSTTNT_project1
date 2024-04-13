import pygame
import sys
import random
import pygame
import time
from Const import *
from Grid import *
from Cell import *

class Sprite:
    def __init__(self, image_paths, screen, location = (0, 0), destroy_animation_paths=None):
        self.images = []
        self.destroy_animation_images = []
        self.destroy_animation_paths = destroy_animation_paths
        self.screen = screen
        self.location = location
        self.current_image_index = 0
        self.destroy_image_id = 0
        self.is_destroyed = False
        self.destroy_animation_set = False

        # Load normal images
        for path in image_paths:
            image = pygame.image.load(path).convert_alpha()
            self.images.append(image)

    def update(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)

    def draw(self):
        if (not self.is_destroyed):
            self.screen.blit(self.images[self.current_image_index], self.location)
            self.update()

    def set_random_index(self):
        self.current_image_index = random.randint(0, len(self.images) - 1)

    def set_destroy_animation(self):
        if self.destroy_animation_paths:
            self.images = []
            for path in self.destroy_animation_paths:
                image = pygame.image.load(path).convert_alpha()
                self.images.append(image)


    def draw_destroy_animation(self):
        if self.destroy_animation_set == False:
            self.set_destroy_animation()
            self.current_image_index = 0
        self.set_destroy_animation_set = True
        if (not self.is_destroyed):
            if self.current_image_index < len(self.images):
                self.screen.blit(self.images[self.current_image_index], self.location)
                if self.current_image_index < len(self.images) - 1:
                    self.update()
                else:
                    self.is_destroyed = True

    
def pickup_sprite(space: Grid, sc: pygame.Surface):
    image_paths1 = [f"Strawberry\\normal{i:02d}.png" for i in range(0, 7)]
    image_paths2 = [f"Strawberry\\normal{i:02d}.png" for i in range(8, 20)]
    sprite_list = []

    for i in space.pickup_points:
        center_x = i.x + 25 // 7
        center_y = i.y + 25 // 4
        sprite = Sprite(image_paths1, sc, (center_x, center_y), image_paths2)
        sprite_list.append(sprite)

    return sprite_list