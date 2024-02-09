import json
import threading
import time

class Pong:
    def __init__(self, Player1, id):
        self.leftBoxTop = 250
        self.rightBoxTop = 250
        self.player1 = Player1
        self.player2 = None
        self.id = id
        self.status = None

    def bar_moov(self, moov, playerMoov):
        
        if moov == 'ArrowUp' and self.leftBoxTop > 0 and self.player1 == playerMoov:
            self.leftBoxTop -= 30
        if moov == 'ArrowDown' and self.leftBoxTop < 430 and self.player1 == playerMoov:
            self.leftBoxTop += 30 
        if moov == 'ArrowUp' and self.rightBoxTop > 0 and self.player2 == playerMoov:
            self.rightBoxTop -= 30
        if moov == 'ArrowDown' and self.rightBoxTop < 430 and self.player2 == playerMoov:
           self.rightBoxTop += 30
        
        self.barSendToJs(moov, self.leftBoxTop, self.rightBoxTop)

    
    def game(self, game):

        if game == 'start':
            t = threading.Thread(target=self.ball, args=())
            t.start()
    
    def ball(self):
        scoreP1 = 0
        scoreP2 = 0

        ballPosX = 499
        ballPosY = 250
        
        hitLeft = 50
        hitRight = 930
        hitWall = 0
        while (scoreP1 < 5 and scoreP2 < 5):
            if ballPosX == 499 and ballPosY == 250:
                while ballPosX > hitLeft: #go left mid
                    ballPosX -= 15
                    self.ballSendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                    time.sleep(0.03)            
            if self.leftBoxTop - ballPosY < 30 and self.leftBoxTop - ballPosY > -90 and ballPosX <= hitLeft:
                if self.leftBoxTop - ballPosY > -20:
                    print('to right direction top')
                    hitWall = 0        
                    while ballPosX < hitRight:
                        if hitWall == 1:
                            ballPosY += 18
                        else:
                            ballPosY -= 10
                        if ballPosY <  0:
                            hitWall = 1
                        ballPosX += 18
                        self.ballSendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
                elif self.leftBoxTop - ballPosY < -50:
                    print('to right direction bot')
                    hitWall = 0
                    while ballPosX < hitRight:
                        if hitWall == 1:
                            ballPosY -= 10
                        else:
                            ballPosY += 10
                        if ballPosY > 460:
                            hitWall = 1
                        ballPosX += 18
                        self.ballSendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
                else:
                    print('to right direction mid')
                    while ballPosX < hitRight:
                        ballPosX += 18
                        self.ballSendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
            elif ballPosX < hitLeft :
                ballPosX = 499
                ballPosY = 250
                scoreP2 += 1
            
            if self.rightBoxTop - ballPosY < 30 and self.rightBoxTop - ballPosY > -90 and ballPosX >= hitRight:
                if self.rightBoxTop - ballPosY > -20:
                    print('to left direction top')
                    hitWall = 0        
                    while ballPosX > hitLeft:
                        if hitWall == 1:
                            ballPosY += 10
                        else:
                            ballPosY -= 10
                        if ballPosY <  0:
                            hitWall = 1
                        ballPosX -= 18
                        self.ballSendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
                elif self.rightBoxTop - ballPosY < -50:
                    print('to left direction bot')
                    hitWall = 0
                    while ballPosX > hitLeft:
                        if hitWall == 1:
                            ballPosY -= 10
                        else:
                            ballPosY += 10
                        if ballPosY > 460:
                            hitWall = 1
                        ballPosX -= 18
                        self.ballSendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
                else:
                    print('to right direction mid')
                    while ballPosX > hitLeft:
                        ballPosX -= 18
                        self.ballSendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
            elif ballPosX > hitRight:
                ballPosX = 499
                ballPosY = 250
                scoreP1 += 1
        self.ballSendToJs(499, 250, scoreP1, scoreP2)
        self.barSendToJs('ArrowUp', 250, 250)
        from .views import manager
        manager.endGame(self.id)

    def ballSendToJs(self, ballPosX, ballPosY, scoreP1, scoreP2):
        self.player1.send(text_data=json.dumps({
            'type':'game',
            'moov':'ball',
            'posX':ballPosX,
            'posY':ballPosY,
            'scoreP1':scoreP1,
            'scoreP2':scoreP2
        }))
        self.player2.send(text_data=json.dumps({
            'type':'game',
            'moov':'ball',
            'posX':ballPosX,
            'posY':ballPosY,
            'scoreP1':scoreP1,
            'scoreP2':scoreP2
        }))
    
    def barSendToJs(self, moov, leftBoxTop, rightBoxTop):
        self.player1.send(text_data=json.dumps({
            'type':'game',
            'moov':moov,
            'leftBoxTop': leftBoxTop,
            'rightBoxTop': rightBoxTop
        }))
        
        self.player2.send(text_data=json.dumps({
            'type':'game',
            'moov':moov,
            'leftBoxTop': leftBoxTop,
            'rightBoxTop': rightBoxTop
        }))

    def __del__(self):
        self.player1.close()
        self.player2.close()