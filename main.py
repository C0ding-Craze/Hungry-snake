import pygame
import sys
import random
from pygame.math import Vector2

pygame.init()
pygame.mixer.init()
Clock = pygame.time.Clock()

block_size = 40 # Each block/cell size in grid.
block_number = 22 # Total number of blocks/cells in grid.

# Screen adjustments.
screen_width = block_size * block_number
screen_height = block_size * block_number
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("HUNGRY SNAKE")
game_icon = pygame.image.load("Visuals/Icon.png")
pygame.display.set_icon(game_icon)

score_font = pygame.font.SysFont(None, 30) 
final_score_font = pygame.font.SysFont("Comic Sans MS", 120)

class BACKGROUND:

    def __init__(self):
        self.background_img = pygame.image.load("Visuals/Grass_background.png").convert()
        self.background = pygame.transform.scale(self.background_img, (screen_width, screen_height))

    def show_background(self):
        screen.blit(self.background, (0,0))

class SNAKE:
    
    def __init__(self):
        self.snake_body = [Vector2(5,6), Vector2(4,6), Vector2(3,6)]
        self.direction = Vector2(0,0)
        self.grow_snake = False

        self.head_up = pygame.image.load("Visuals/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Visuals/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("Visuals/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("Visuals/head_right.png").convert_alpha()
        
        self.tail_up = pygame.image.load("Visuals/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Visuals/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("Visuals/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("Visuals/tail_right.png").convert_alpha()
        
        self.curve_top_left = pygame.image.load("Visuals/curve_top_left.png").convert_alpha()
        self.curve_top_right = pygame.image.load("Visuals/curve_top_right.png").convert_alpha()
        self.curve_bottom_left = pygame.image.load("Visuals/curve_bottom_left.png").convert_alpha()
        self.curve_bottom_right = pygame.image.load("Visuals/curve_bottom_right.png").convert_alpha()

        self.body_horizontal = pygame.image.load("Visuals/body_horizontal.png").convert_alpha()
        self.body_vertical = pygame.image.load("Visuals/body_vertical.png").convert_alpha()
        
    def show_snake(self):
        self.update_head()
        self.update_tail()
        
        for index,block in enumerate(self.snake_body):
            block_x = block.x * block_size
            block_y = block.y * block_size
            block_rect = pygame.Rect(block_x , block_y, block_size, block_size)

            if index == 0:
                screen.blit(self.head, block_rect)

            elif index == len(self.snake_body) - 1:
                screen.blit(self.tail, block_rect)

            else:
                previous_block = self.snake_body[index + 1] - block
                next_block = self.snake_body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)

                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect) 
                
                else:
                    if ((previous_block.x == -1 and next_block.y == -1) 
                        or (previous_block.y == -1 and next_block.x == -1)):                        
                        screen.blit(self.curve_bottom_right, block_rect)

                    elif ((previous_block.y == 1 and next_block.x == -1) 
                        or (previous_block.x == -1 and next_block.y == 1)):                        
                        screen.blit(self.curve_top_right, block_rect)

                    elif ((previous_block.x == 1 and next_block.y == 1) 
                        or (previous_block.y == 1 and next_block.x == 1)):                        
                        screen.blit(self.curve_top_left, block_rect)
                
                    elif ((previous_block.x == 1 and next_block.y == -1) 
                        or (previous_block.y == -1 and next_block.x == 1)):                        
                        screen.blit(self.curve_bottom_left, block_rect)

    def update_head(self):
        head_relation = self.snake_body[1] - self.snake_body[0]

        if head_relation == Vector2(-1,0):
            self.head = self.head_right

        elif head_relation == Vector2(1,0):
            self.head = self.head_left

        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

        elif head_relation == Vector2(0,1):
            self.head = self.head_up

    def update_tail(self):
        tail_relation = self.snake_body[-2] - self.snake_body[-1]

        if tail_relation == Vector2(1,0):
            self.tail = self.tail_right

        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_left

        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_down

        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_up

    def move_snake(self):
        if self.grow_snake == True:
            snake_body_copy = self.snake_body[:]
            snake_body_copy.insert(0, self.snake_body[0] + self.direction)
            self.snake_body = snake_body_copy[:]
            self.grow_snake = False
        else:
            snake_body_copy = self.snake_body[:-1]
            snake_body_copy.insert(0, self.snake_body[0] + self.direction)
            self.snake_body = snake_body_copy[:]

    def add_block(self):
        self.grow_snake = True 

    def reset_snake(self):
        self.snake_body = [Vector2(5,6), Vector2(4,6), Vector2(3,6)]
        self.direction = Vector2(0,0)

class APPLE:

    def __init__(self):
        self.Apple_img = pygame.image.load("Visuals/Apple.png").convert_alpha()
        self.bite_sound = pygame.mixer.Sound("Sounds/Bite.mp3")
        self.spawn_randomizer()

    def show_apple(self):
        self.apple_rect = pygame.Rect(self.apple_pos.x, self.apple_pos.y, block_size, block_size)
        screen.blit(self.Apple_img, self.apple_rect)

    def spawn_randomizer(self):
        self.x = random.randint(0, block_number - 1)
        self.y = random.randint(0, block_number - 1)
        self.pos = Vector2(self.x, self.y) # position w.r.t grid used in MAIN class.
        self.apple_pos = Vector2(self.x * block_size, self.y * block_size)

    def play_sound(self):
        self.bite_sound.play()

class MAIN:

    def __init__(self):
        self.background = BACKGROUND()
        self.snake = SNAKE()
        self.apple = APPLE()

    def show_elements(self):
        self.background.show_background()
        self.snake.show_snake()
        self.apple.show_apple()
        self.show_score()

    def update_screen(self):        
        self.snake.move_snake()
        self.check_apple_collision()
        self.check_border_collision()
        self.check_snake_collision()

    def check_apple_collision(self):
        if self.apple.pos == self.snake.snake_body[0]:
            self.apple.play_sound()
            self.apple.spawn_randomizer()
            self.snake.add_block()

        for block in self.snake.snake_body[1:]:
            if block == self.apple.pos:
                self.apple.spawn_randomizer()

    def check_border_collision(self):
        if (
            self.snake.snake_body[0].x < 0
            or self.snake.snake_body[0].x >= block_number
            or self.snake.snake_body[0].y < 0
            or self.snake.snake_body[0].y >= block_number
        ):
            self.game_over() 

    def check_snake_collision(self):
        for body in self.snake.snake_body[1:]:
            if body == self.snake.snake_body[0]:
                self.game_over()        

    def game_over(self):
        self.snake.reset_snake()

    def show_score(self):
        score = str(len(self.snake.snake_body) - 3)
        score_surface = score_font.render(score, True, (0,0,0))
        score_x = int(block_size * block_number - 80)
        score_y = int(block_size * block_number - 70)
        score_rect = score_surface.get_rect(center=(score_x,score_y))
        apple_rect = self.apple.Apple_img.get_rect(midright=(score_rect.left, score_rect.centery - 3))
        screen.blit(score_surface, score_rect)
        screen.blit(self.apple.Apple_img, apple_rect)

# Custom event for updating screen after every 150 milliseconds.
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

if __name__=="__main__":

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SCREEN_UPDATE:
                main_game.update_screen()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)

                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)

                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
        
        main_game.show_elements()
        pygame.display.update()
        Clock.tick(60)
        