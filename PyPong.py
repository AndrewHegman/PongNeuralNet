import pygame
import random
import copy

ScreenWidth = 1024
ScreenHeight = 768
HorizontalBuffer = 5
VerticalBuffer = 5
PaddleWidth = 10
PaddleHeight = 100
BallWidth = 10
BallHeight = 10
BallSpeed = 3
random.seed()


class PongObject:

    def __init__(self, x, y, width, length, auto):
        self.StartingPosition = [x, y]
        self.Rect = pygame.Rect(x, y, width, length)
        self.Auto = auto
        self.Center = [y + (length / 2), x + (width / 2)]
        self.Change = 0
        self.MovingUp = False
        self.MovingDown = False
        self.GamesWon = 0
        self.TestVar = 0
        
    def draw_object(self, gamescreen):
        pygame.draw.rect(gamescreen, (255, 255, 255), self.Rect)
        
    def updateposition(self, change_y):
        self.Change += change_y
        
        if change_y < 0:
            self.MovingUp = True
            self.MovingDown = False
        elif change_y > 0:
            self.MovingUp = False
            self.MovingDown = True
        else:
            self.MovingUp = False
            self.MovingDown = False

        self.Rect.y += int(self.Change)
        if self.Rect.bottom > (ScreenHeight - VerticalBuffer) or self.Rect.top < VerticalBuffer:
            self.Rect.y -= int(self.Change)
            self.MovingUp = False
            self.MovingDown = False

        if abs(int(self.Change)) >= 1:
            self.Change = 0

    def set_position(self, x, y):
        self.Rect.x = x
        self.Rect.y = y
        self.Center[0] = self.Rect.x = (self.Rect.width / 2)
        self.Center[1] = self.Rect.y = (self.Rect.height / 2)

    def reset(self, won_game):
        self.Rect.x = self.StartingPosition[0]
        self.Rect.y = self.StartingPosition[1]
        self.Change = 0
        self.MovingUp = False
        self.MovingDown = False
        if won_game:
            self.GamesWon += 1


class PongBall:
    def __init__(self, x, y, width, length, max_speed):
        self.StartingPosition = [x, y]
        self.Rect = pygame.Rect(x, y, width, length)

        self.max_speed = [max_speed[0], max_speed[1]]      #Pixels/Sec
        self.Change = [0, 0]
        self.Speed = self.get_random_speed()   #Pixels/sec

        self.StartingSpeed = copy.deepcopy(self.Speed)

        self.HitHorizontalEdge = False
        self.HitVerticalEdge = False

        self.HitPaddle1 = False
        self.HitPaddle2 = False
        self.SpedUpByPaddle = False

        self.Player1Won = False
        self.Player2Won = False

    def draw_object(self, gamescreen):
        pygame.draw.rect(gamescreen, (255, 255, 255), self.Rect)

    def updateposition(self, paddle1, paddle2):
        self.check_for_collision(paddle1, paddle2)

        self.Change[0] += self.Speed[0]
        self.Change[1] += self.Speed[1]

        if self.HitHorizontalEdge and abs(self.Change[1]) >= 1:
            self.HitHorizontalEdge = False
        if self.HitVerticalEdge and abs(self.Change[0]) >= 1:
            self.HitVerticalEdge = False

        self.Rect.x += int(self.Change[0])
        self.Rect.y += int(self.Change[1])

        if abs(int(self.Change[0])) >= 1:
            self.Change[0] = 0
        if abs(int(self.Change[1])) >= 1:
            self.Change[1] = 0

        if self.Rect.x >= ScreenWidth - self.Rect.width:
            self.Player1Won = True
        elif self.Rect.x <= 0:
            self.Player2Won = True

        if (self.Rect.y >= ScreenHeight - self.Rect.height or self.Rect.y <= 0) and not self.HitHorizontalEdge:
            self.Speed[1] = -self.Speed[1]
            self.Change[1] = 0
            self.HitHorizontalEdge = True
            if abs(self.Speed[0]) > abs(self.StartingSpeed[0]):
                self.Speed[1] -= self.Speed[1] * 0.1

    def check_for_collision(self, paddle1, paddle2):
        if not self.HitPaddle1 and self.Rect.colliderect(paddle1.Rect):
            self.Speed[0] = -self.Speed[0]
            self.HitPaddle1 = True
            if paddle1.MovingUp and not self.SpedUpByPaddle:
                self.Speed[1] = abs(self.Speed[1]) * -1.5
            elif paddle1.MovingDown and not self.SpedUpByPaddle:
                self.Speed[1] = abs(self.Speed[1]) * 1.5

        elif self.HitPaddle1 and not self.Rect.colliderect(paddle1.Rect):
            self.HitPaddle1 = False

        if not self.HitPaddle2 and self.Rect.colliderect(paddle2.Rect):
            self.Speed[0] = -self.Speed[0]
            self.HitPaddle2 = True
            if paddle2.MovingUp and not self.SpedUpByPaddle:
                self.Speed[1] = abs(self.Speed[1] * 1.5)

            elif paddle2.MovingDown and not self.SpedUpByPaddle:
                self.Speed[1] = -1 * abs(self.Speed[1] * 1.5)

        elif self.HitPaddle2 and not self.Rect.colliderect(paddle2.Rect):
            self.HitPaddle2 = False

    def get_random_speed(self):
        speed = [0, 0]
        while abs(speed[0]) + abs(speed[1]) != 0.6 and not abs(speed[0]) < abs(speed[1]):
            speed = [random.choice([i/10 for i in range(-5, 6) if i != 0.0]), 
                     random.choice([i/10 for i in range(-5, 6) if i != 0.0])]
        return speed
    
    def reset(self):
        self.Rect.x = self.StartingPosition[0]
        self.Rect.y = self.StartingPosition[1]

        self.Change = [0, 0]
        self.Speed = self.get_random_speed()
        self.StartingSpeed = copy.deepcopy(self.Speed)

        self.HitHorizontalEdge = False
        self.HitVerticalEdge = False

        self.HitPaddle1 = False
        self.HitPaddle2 = False
        self.SpedUpByPaddle = False

        self.Player1Won = False
        self.Player2Won = False

screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
Player1 = PongObject(HorizontalBuffer, VerticalBuffer, PaddleWidth, PaddleHeight, False)
Player2 = PongObject(ScreenWidth - PaddleWidth - HorizontalBuffer, VerticalBuffer, PaddleWidth, PaddleHeight, False)
Ball = PongBall(ScreenWidth / 2, ScreenHeight / 2, BallWidth, BallHeight, (-0.75, 0.75))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    if not Player1.Auto:
        if pygame.key.get_pressed()[pygame.K_UP]:
            if Player1.Rect.y >= VerticalBuffer:
                Player1.updateposition(-0.25)

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if Player1.Rect.y <= ScreenHeight - VerticalBuffer - Player1.Rect.height:
                Player1.updateposition(0.25)
    else:
        if Ball.Rect.y > Player1.Rect.centery:
            Player1.updateposition(0.25)
        elif Ball.Rect.y < Player1.Rect.centery:
            Player1.updateposition(-0.25)

    if not Player2.Auto:
        pass
    else:
        if Ball.Rect.y > Player2.Rect.centery:
            Player2.updateposition(0.25)
        elif Ball.Rect.y < Player2.Rect.centery:
            Player2.updateposition(-0.25)

    screen.fill((0, 0, 0))
    Ball.updateposition(Player1, Player2)

    if Ball.Player1Won:
        print("Player 1 won!")
        Player1.reset(True)
        Player2.reset(False)
        Ball.reset()
        input()
    elif Ball.Player2Won:
        print("Player 2 won!")
        Player1.reset(True)
        Player2.reset(False)
        Ball.reset()
        input()
    else:
        Player1.draw_object(screen)
        Player2.draw_object(screen)
        Ball.draw_object(screen)
    
    pygame.display.flip()
