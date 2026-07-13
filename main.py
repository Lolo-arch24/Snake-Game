import pygame
import random
import sys
import math

pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE 

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0,)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (0, 128, 0)
GRAY = (128, 128, 128)

class Food:
    def __init__(self, food_type='normal'):
        self.x = random.randint(0, GRID_WIDTH -1)
        self.y = random.randint(0, GRID_HEIGHT -1)
        self.type = food_type
        self.spawn_time = pygame.time.get_ticks()

        # Food type properties
        self.properties = {
            'normal': {'color': RED, 'points': 10, 'growth': 1, 'duration': None},
            'golden': {'color': YELLOW, 'points': 50, 'growth': 2, 'duration': 5000},
            'speed': {'color': BLUE, 'points': 25, 'growth': 1, 'duration': 3000},
            'shrink': {'color': PURPLE, 'points': 30, 'growth': -1, 'duration': None},
        }

    def should_disappear(self):
        if self.type == 'golden':
            return pygame.time.get_ticks() - self.spawn_time > self.properties[self.type]['duration']
        return False

    def draw(self, screen):
        color = self.properties[self.type]['color']
        rect = pygame.Rect(self.x * GRID_SIZE, GRID_SIZE, GRID_SIZE)

        if self.type == 'golden':
            # Pulsing golden food
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))
            golden_color = (255, int(255 * pulse), 0)
            pygame.draw.rect(screen, golden_color, rect) 
        elif self.type == 'speed':
            # Fishing blue food
            if (pygame.time.get_ticks() // 200) % 2:
                pygame.draw.rect(screen, color, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
        else: 
            pygame.draw.rect(screen, color, rect)

        # Add border
        pygame.draw.rect(screen, WHITE, rect, 1)

class Snake:
    def __init__(self):
        self.positions = [GRID_WIDTH // 2, GRID_HEIGHT // 2]
        self.direction = (0, -1)
        self.grow_pending = 0
        self.speed_boost_end = 0

    def move(self):
        head_x, head_y = self.position[0]
        new_x, = head_y + self.directions[0]
        new_y = head_y + self.direction[1]

        new_x = new_x % GRID_WIDTH 
        new_y = new_y % GRID_HEIGHT

        self.positions.insert(0, (new_x, new_y))

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()

    def change_direction(self, new_direction):
        # prevent moving directly backwards
        if (self.direction[0] * -1, self.direction[1]* -1) != new_direction:
            self.direction = new_direction 

    def grow(self, amount):
        if amount > 0:
            self.grow_pending += amount
        elif amount < 0 and len(self.positions) > 1:
            shrink_amount = min(abs(amount), len(self.positions) -1)
            for _ in range(shrink_amount):
                if len(self.positions) > 1:
                    self.positions.pop()
                    

    def check_collision(self):
        head = self.positions[0]
        #Check for collision
        return head in self.positions[1:]
    
    def has_speed_boost(self):
        return pygame.time.get_ticks() < self.speed_boost_end
    
    def apply_speed_boost(self, duration):
        self.speed_boost_end = pygame.time.get_ticks() + duration

    def draw(self, screen):
        if len(self.positions) == 0:
            return
        
        # Draw body segments with smooth curves
        for i in range(len(self.positions) -1, -1, -1):
            pos = self.positions[i]
            x, y = pos[0] * GRID_SIZE, pos[1] * GRID_SIZE
            center_x, center_y = x + GRID_SIZE // 2, y + GRID_SIZE // 2

            if 1 == 0:
                self.draw_head(screen, center_x, center_y)
            elif 1 == len(self.positions) - 1:
                self.draw_tail(screen, center_x, center_y, i)
            else: 
                self.draw_body_segment(screen, center_x, center_y, i)

    def draw_head
