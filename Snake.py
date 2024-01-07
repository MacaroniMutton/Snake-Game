import pygame, sys
from pygame.math import Vector2
import random

class Food:
    def __init__(self):
        self.x = random.randint(0, CELL_NUMBER-1)
        self.y = random.randint(0, CELL_NUMBER-1)
        self.pos = Vector2(self.x*CELL_SIZE, self.y*CELL_SIZE)
        self.apple = pygame.image.load("Graphics/apple.png").convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (CELL_SIZE, CELL_SIZE))

    def draw_food(self):
        food_rect = pygame.Rect(int(self.pos.x), int(self.pos.y), CELL_SIZE, CELL_SIZE)
        screen.blit(self.apple, food_rect)
        # pygame.draw.rect(screen, "#FF0000", food_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(7*CELL_SIZE, 10*CELL_SIZE), Vector2(6*CELL_SIZE, 10*CELL_SIZE), Vector2(5*CELL_SIZE, 10*CELL_SIZE)]
        # self.body = []
        # for k in range(1, 18, 2):
        #     for i in range(14):
        #         self.body.append(Vector2((2+i)*CELL_SIZE, (k+1)*CELL_SIZE))
        #     for i in range(13, -1, -1):
        #         self.body.append(Vector2((2+i)*CELL_SIZE, (k+2)*CELL_SIZE))

        self.direction = RIGHT

        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()

        self.body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()
        self.body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha()

        self.body_bottomleft = pygame.image.load("Graphics/body_bottomleft.png").convert_alpha()
        self.body_bottomright = pygame.image.load("Graphics/body_bottomright.png").convert_alpha()
        self.body_topleft = pygame.image.load("Graphics/body_topleft.png").convert_alpha()
        self.body_topright = pygame.image.load("Graphics/body_topright.png").convert_alpha()

    def draw_snake(self):
        for index,square in enumerate(self.body):
            snake_rect = pygame.Rect(int(square.x), int(square.y), CELL_SIZE, CELL_SIZE)
            if index==0:
                if self.direction == RIGHT:
                    screen.blit(self.head_right, snake_rect)
                elif self.direction == LEFT:
                    screen.blit(self.head_left, snake_rect)
                elif self.direction == UP:
                    screen.blit(self.head_up, snake_rect)
                elif self.direction == DOWN:
                    screen.blit(self.head_down, snake_rect)
            elif index==len(self.body)-1:
                
                screen.blit(self.tail_graphic(), snake_rect)
            else:
                prev_square = self.body[index+1]
                next_square = self.body[index-1]
                if prev_square.y == square.y == next_square.y:
                    screen.blit(self.body_horizontal, snake_rect)
                elif prev_square.x == square.x == next_square.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif prev_square.y == square.y == next_square.y-CELL_SIZE and prev_square.x+CELL_SIZE == square.x == next_square.x:
                    screen.blit(self.body_bottomleft, snake_rect)
                elif prev_square.y-CELL_SIZE == square.y == next_square.y and prev_square.x == square.x == next_square.x+CELL_SIZE:
                    screen.blit(self.body_bottomleft, snake_rect)
                elif prev_square.y == square.y == next_square.y-CELL_SIZE and prev_square.x-CELL_SIZE == square.x == next_square.x:
                    screen.blit(self.body_bottomright, snake_rect)
                elif prev_square.y-CELL_SIZE == square.y == next_square.y and prev_square.x == square.x == next_square.x-CELL_SIZE:
                    screen.blit(self.body_bottomright, snake_rect)
                elif prev_square.y+CELL_SIZE == square.y == next_square.y and prev_square.x == square.x == next_square.x+CELL_SIZE:
                    screen.blit(self.body_topleft, snake_rect)
                elif prev_square.y == square.y == next_square.y+CELL_SIZE and prev_square.x+CELL_SIZE == square.x == next_square.x:
                    screen.blit(self.body_topleft, snake_rect)
                elif prev_square.y == square.y == next_square.y+CELL_SIZE and prev_square.x-CELL_SIZE == square.x == next_square.x:
                    screen.blit(self.body_topright, snake_rect)
                elif prev_square.y+CELL_SIZE == square.y == next_square.y and prev_square.x == square.x == next_square.x-CELL_SIZE:
                    screen.blit(self.body_topright, snake_rect)
                
    
    def tail_graphic(self):
        tail_relation = self.body[-1] - self.body[-2]
        if tail_relation == LEFT:
            return self.tail_left
        elif tail_relation == RIGHT:
            return self.tail_right
        elif tail_relation == DOWN:
            return self.tail_down
        elif tail_relation == UP:
            return self.tail_up

    def move_snake(self):
        new_body_part = self.body[0] + self.direction
        self.body.insert(0, new_body_part)

    def rmvLastBlock(self):
        self.body.pop()

class Main:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        while self.food.pos in self.snake.body:
            self.food = Food()
        self.score = 0
        self.crunch_sound = pygame.mixer.Sound('Graphics/appleCrunch.wav')
        self.over = False

    def draw_elements(self):
        if self.over:
            screen.fill((255, 255, 255))
            self.draw_winner()
        else:
            screen.fill((175, 215, 70))
            self.draw_grass()
            self.snake.draw_snake()
            self.food.draw_food()
            self.draw_score()

    def eat_food(self):
        if self.food.pos == self.snake.body[0]:
            self.score += 1
            self.crunch_sound.play()
            self.food = Food()
            while self.food.pos in self.snake.body:
                self.food = Food()
                if not self.check_empty_spaces():
                    self.game_over()
                    break
            return True
        else:
            return False
        
    def check_empty_spaces(self):
        for i in range(CELL_NUMBER):
                    for j in range(CELL_NUMBER):
                        if Vector2(i*CELL_SIZE, j*CELL_SIZE) not in self.snake.body:
                            return True
        return False
        
    def check_collisions(self):
        snake_head = self.snake.body[0]
        if snake_head.x<0 or snake_head.x+CELL_SIZE>CELL_NUMBER*CELL_SIZE:
            return True
        elif snake_head.y<0 or snake_head.y+CELL_SIZE>CELL_NUMBER*CELL_SIZE:
            return True
        elif snake_head in self.snake.body[1:]:
            return True
        
    def game_over(self):
        self.over = True

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                if col%2==row%2:
                    grass_rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = "Score : "+str(self.score)+" "
        score_surface = game_font.render(score_text, True, "#000000")
        score_x = CELL_NUMBER*CELL_SIZE / 2
        score_y = CELL_NUMBER*CELL_SIZE + SCOREBOARD_HEIGHT/2
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple = pygame.image.load("Graphics/apple.png").convert_alpha()
        apple = pygame.transform.scale(apple, (CELL_SIZE, CELL_SIZE))
        apple_rect = apple.get_rect(topleft = (score_rect.right, score_rect.top))
        frame = pygame.Rect(score_rect.left-4, score_rect.top-1, score_rect.width+apple_rect.width+6, score_rect.height+3)
        pygame.draw.rect(screen, "#000000", frame, 2)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)

    def draw_winner(self):
        #screen.fill((255, 255, 255))
        text = "You're the Snake Lord!"
        surf = game_font.render(text, True, "#000000")
        x = CELL_NUMBER*CELL_SIZE / 2
        y = CELL_NUMBER*CELL_SIZE / 2
        rect = surf.get_rect(center = (x, y))
        winner = pygame.image.load("Graphics/winner.png").convert_alpha()
        winner = pygame.transform.scale(winner, (5*CELL_SIZE, 5*CELL_SIZE))
        winner_rect = winner.get_rect(center = (x, y+175))
        screen.blit(surf, rect)
        screen.blit(winner, winner_rect)

pygame.init()

CELL_SIZE = 30
CELL_NUMBER = 14
SCOREBOARD_HEIGHT = 100
RIGHT = Vector2(1*CELL_SIZE, 0*CELL_SIZE)
LEFT = Vector2(-1*CELL_SIZE, 0*CELL_SIZE)
UP = Vector2(0*CELL_SIZE, -1*CELL_SIZE)
DOWN = Vector2(0*CELL_SIZE, 1*CELL_SIZE)
game_font = pygame.font.Font(None, 50)
winner_font = pygame.font.Font(None, 100)

pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((CELL_NUMBER*CELL_SIZE, CELL_NUMBER*CELL_SIZE+SCOREBOARD_HEIGHT))
clock = pygame.time.Clock()

main_game = Main()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        if event.type==SCREEN_UPDATE:
            if not main_game.check_collisions():
                main_game.snake.move_snake()
                if not main_game.eat_food():
                    main_game.snake.rmvLastBlock()
            # else:
            #     main_game.game_over()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w or event.key==pygame.K_UP:
                if main_game.snake.direction!=DOWN:
                    main_game.snake.direction = UP
            elif event.key==pygame.K_a or event.key==pygame.K_LEFT:
                if main_game.snake.direction!=RIGHT:
                    main_game.snake.direction = LEFT
            elif event.key==pygame.K_s or event.key==pygame.K_DOWN:
                if main_game.snake.direction!=UP:
                    main_game.snake.direction = DOWN
            elif event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                if main_game.snake.direction!=LEFT:
                    main_game.snake.direction = RIGHT
    
    
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
