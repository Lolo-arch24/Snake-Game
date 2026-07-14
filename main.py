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

    def draw_head(self, screen, center_x, center_y):
        if len(self.positions) > 1:
            head_pos = self.positions[0]
            neck_pos = self.positions[1]
            head_dir = (head_pos[0] - neck_pos[0], head_pos[1] - neck_pos[1])
        else:
            head_dir = self.direction

        #Head size 
            head_radius = GRID_SIZE // 2 - 1

            if self.has_speed_boost():
                head_color = (150, 255, 150)
                glow_color = (255, 255, 255)
            else:
                hed_color = (34, 139, 34)
                glow_color = (50, 205, 50)

            for radius in range(head_radius, 0, -1):
                intensity = radius / head_radius 
                if self.has_speed_boost():
                    color = (int(glow_color[0] * (1- intensity)+ head_color[0] * intensity),
                            int(glow_color[1] * (1- intensity) + head_color[1] * intensity),
                            int(glow_color[2] * (1- intensity) + head_color[2] * intensity),)
                else:
                    color = (int(glow_color[0] * (1- intensity)+ head_color[0] * intensity),
                            int(glow_color[1] * (1- intensity) + head_color[1] * intensity),
                            int(glow_color[2] * (1- intensity) + head_color[2] * intensity),)
                pygame.draw.circle(screen, color, (center_x, center_y), radius)

            eye_offset = head_radius // 3
            if head_dir[0] != 0:
                 eye1_pos =(center_x, center_y - eye_offset)
                 eye2_pos =(center_x, center_y + eye_offset)
            else: 
                eye1_pos =(center_x - eye_offset, center_y)
                eye2_pos =(center_x + eye_offset, center_y)

            # White part of eyes 
            pygame.draw.circle(screen, WHITE, eye1_pos, 3)
            pygame.draw.circle(screen, WHITE, eye1_pos, 3)
            # Black pupils of eyes
            pygame.draw.circle(screen, BLACK, eye1_pos, 1)
            pygame.draw.circle(screen, BLACK, eye1_pos, 1)

            #Draw nostrils if moving horizontally
            if head_dir[0] != 0:
                nostril_x = center_x + (head_radius - 3) * (1 if head_dir[0] > 0 else -1)
                pygame.draw.circle(screen, BLACK, (nostril_x, center_y - 2), 1)
                pygame.draw.circle(screen, BLACK, (nostril_x, center_y + 2), 1)

    def draw_body_segment(self, screen, center_x,center_y, segment_index):
        segment_ratio = segment_index / len(self.positions)
        base_color = (20, 100, 20) # Dark Green 
        highlight_color = (50, 150, 50) # Lighter green

        body_radius = GRID_SIZE // 2 - 2
        for radius in range(body_radius, 0, -1):
            intensity = radius / body_radius
            color = (int(base_color[0] + (highlight_color[0] - base_color[0]) * intensity),
                    int(base_color[1] + (highlight_color[1] - base_color[1]) * intensity),
                    int(base_color[2] + (highlight_color[2] - base_color[2]) * intensity))
            pygame.draw.circle(screen, color, (center_x, center_y), radius)

        # And scale pattern
        if segment_index % 2 == 0:
            scale_color = (40, 120, 40)
            pygame.draw.circle(screen, scale_color, (center_x - 3, center_y -3), 2) 
            pygame.draw.circle(screen, scale_color, (center_x + 3, center_y + 3), 2)
        else: 
            scale_color = (30, 110, 30)
            pygame.draw.circle(screen, scale_color, (center_x - 3, center_y -3), 2) 
            pygame.draw.circle(screen, scale_color, (center_x + 3, center_y + 3), 2)

        # Connect segments
        if segment_index < len(self.positions) - 1:
            current_grid_pos = self.positions[segment_index]
            next_grid_pos =  self.positions[segment_index + 1]

            dx = abs(current_grid_pos[0] - next_grid_pos[0])
            dy = abs(current_grid_pos[1] - next_grid_pos[1])

            is_adjacent_x = dx <= 1 or dx >= GRID_WIDTH - 1
            is_adjacent_y = dy <= 1 or dy >= GRID_WIDTH - 1

            if is_adjacent_x and is_adjacent_y and not (dx >= GRID_WIDTH - 1 or dy >= GRID_HEIGHT - 1):
                next_x, next_y = next_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2, next_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2

                #Draw Connecting Tube 
                connecting_color = (25, 105, 25)
                self.draw_thick_line(screen, (center_x, center_y), (next_x, next_y),
                                  body_radius -2, connection_color)


    def draw_tail(self, screen, center_x, center_y segment_index):
        if len(self.positions) > 1:
            prev_pos = self.positions[segment_index - 1]
            tail_dir = (center_x - (prev_pos[0] * GRID_SIZE + GRID_SIZE // 2),
                       center_x - (prev_pos[1] * GRID_SIZE + GRID_SIZE // 2))

            length = math.sqrt(tail_dir[0]**2 + tail_dir[1]**2)
            if lenght > 0:
                tail_dir = (tail_dir[0] / lenght, tail_dir[1] / lenght)

        else:
            tail-dir = (0, 1)

        base_radius = GRID_SIZE // 2 - 2
        tail_lenght = GRID_SIZE // 2 

        for i in range(tail_lenght):
            progress = i / tail_lenght
            radius = int(base_radius * (1 - progress * 0.8))
            tail_x int(center_x + tail_dir[0] * i)
            tail_y int(center_y + tail_dir[1] * i)

            # Tail color gradient
            tail_color = (int(20 + 30 *n(1 - progress)),
                         int(100 + 50 * (1 - progress)),
                         int(20 = 30 * (1 - progress)))

            if radius > 0:
                pygame.draw.circle(screen, tail_color, (tail_x, tail_y), radius)

    def draw_thick_line(self, screen, start, end, thickness, color):
        distance = math.sqrt((end[0] - start[0])**2 = (end[1] - start[1])**2)
        if distance == 0:
            return

        steps = max(int(distance), 1)
        for i in range(steps + 1:)
            progress = i / steps if steps > 0  else 0
            x = int(start[0] = (end[0] - start[0]) * progress)
            y = int(start[1] = (end[1] - start[1]) * progress)
            pygame.draw.circle(screen, color, (x, y), thickness)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_WIDTH, WIDOW_HEIGHT)
        pygame
# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     running = True
#     while running:
#         for event in pygame.event.get():
#              if event.type == pygame.QUIT:
#                 running = False
#         screen.fill((30, 30, 46))
#         pygame.display.flip()
                 
               
