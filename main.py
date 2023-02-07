'''from lib2to3.pygram import python_grammar_no_print_statement
from tkinter import LEFT'''
import pygame
pygame.init()

Width, Hieght = 700, 500
Win = pygame.display.set_mode((Width, Hieght))
pygame.display.set_caption("PONG") 

FPS = 60 # 60 Frames per second

White = (250 ,250, 250)
Black = (0, 0, 0)
Blue = (0,255,255)

Paddle_Width , Paddle_Hieght = 20, 100
Ball_radius = 7

Score_font = pygame.font.SysFont("comicans", 50)
Winning_score = 10

class Paddle:
    Color = White
    Vel = 4

    def __init__(self, x, y, width, hieght):
        self.x = self.orignal_x = x
        self.y = self.orignal_y = y
        self.width = width 
        self.hieght = hieght
    
    def draw(self,win):
        pygame.draw.rect(win, self.Color, (self.x, self.y, self.width, self.hieght))

    def move(self,up=True):
        if up:
            self.y -= self.Vel
        else:
            self.y += self.Vel
    
    def reset(self):
        self.x = self.orignal_x
        self.y = self.orignal_y

class Ball:
    Max_Vel = 5
    Color = Blue

    def __init__(self, x, y, radius):
        self.x = self.orignal_x = x
        self.y = self.orignal_y = y
        self.radius = radius
        self.x_vel = self.Max_Vel
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.Color,(self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.orignal_x
        self.y = self.orignal_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(Black)

    left_score_text = Score_font.render(f"{left_score}", 1, White)
    right_score_text = Score_font.render(f"{right_score}", 1, White)
    win.blit(left_score_text, (Width//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (Width * (3/4) -right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)
    
    for i in range(10, Hieght, Hieght//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, White, (Width//2 - 5, i, 10, Hieght//20))
    ball.draw(win)

    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= Hieght:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.hieght:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.hieght / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.hieght / 2) / ball.Max_Vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.hieght:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.hieght / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.hieght / 2) / ball.Max_Vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.Vel >=0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.Vel + left_paddle.hieght <= Hieght:
        left_paddle.move(up=False)
    
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.Vel >=0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.Vel + right_paddle.hieght <= Hieght:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, Hieght//2 - Paddle_Hieght//2, Paddle_Width, Paddle_Hieght)

    right_paddle = Paddle(Width - 10 - Paddle_Width, Hieght//2 - Paddle_Hieght//2, Paddle_Width, Paddle_Hieght)

    ball = Ball(Width//2, Hieght//2, Ball_radius)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(Win,[left_paddle,right_paddle],ball, left_score, right_score)   


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > Width:
            left_score += 1
            ball.reset()
        
        won = False

        if left_score >= Winning_score:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= Winning_score:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = Score_font.render(win_text, 1, White)
            Win.blit(text, (Width//2 - text.get_width()//2, Hieght//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__':
    main()


