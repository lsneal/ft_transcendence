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
        self.scoreP1 = 0
        self.scoreP2 = 0

    def bar_moov(self, moov, playerMoov):
        
        if moov == 'ArrowUp' and self.leftBoxTop > 0 and self.player1 == playerMoov != self.player2:
            self.leftBoxTop -= 30
        if moov == 'ArrowDown' and self.leftBoxTop < 430 and self.player1 == playerMoov != self.player2:
            self.leftBoxTop += 30
        
        if moov == 'ArrowUp' and self.rightBoxTop > 0 and self.player2 == playerMoov:
            self.rightBoxTop -= 30
        if moov == 'ArrowDown' and self.rightBoxTop < 430 and self.player2 == playerMoov:
            self.rightBoxTop += 30
        
        if moov == 'w' and self.leftBoxTop > 0 and self.player1 == playerMoov == self.player2:
            self.leftBoxTop -= 30
        if moov == 's' and self.leftBoxTop < 430 and self.player1 == playerMoov == self.player2:
            self.leftBoxTop += 30

        self.barSendToJs(moov, self.leftBoxTop, self.rightBoxTop)

    
    def game(self, game, typeParty):
        t = threading.Thread(target=self.ball, args=(typeParty,))
        if game == 'start':
            t.start()

    
    def ball(self, typeParty):

        ballPosX = 499
        ballPosY = 250
        
        hitLeft = 50
        hitRight = 930
        hitWall = 0
        self.scoreP1 = 0
        self.scoreP2 = 0
        i = 0
        while i <= 4:
            self.player1.send(text_data=json.dumps({
                'type':'time',
                'time':i,
            }))
            if typeParty == 'game':
                self.player2.send(text_data=json.dumps({
                    'type':'time',
                    'time':i,
                }))
            time.sleep(0.5)
            i += 1
        while self.scoreP1 < 5 and self.scoreP2 < 5:
            if ballPosX == 499 and ballPosY == 250:
                while ballPosX > hitLeft:
                    ballPosX -= 15
                    self.ballSendToJs(ballPosX, ballPosY, typeParty)
                    time.sleep(0.03)            
            if self.leftBoxTop - ballPosY < 30 and self.leftBoxTop - ballPosY > -90 and ballPosX <= hitLeft:
                if self.leftBoxTop - ballPosY > -20:
                    hitWall = 0        
                    while ballPosX < hitRight:
                        if hitWall == 1:
                            ballPosY += 18
                        else:
                            ballPosY -= 10
                        if ballPosY <  0:
                            hitWall = 1
                        ballPosX += 18
                        self.ballSendToJs(ballPosX, ballPosY, typeParty)
                        time.sleep(0.03)
                elif self.leftBoxTop - ballPosY < -50:
                    hitWall = 0
                    while ballPosX < hitRight:
                        if hitWall == 1:
                            ballPosY -= 10
                        else:
                            ballPosY += 10
                        if ballPosY > 460:
                            hitWall = 1
                        ballPosX += 18
                        self.ballSendToJs(ballPosX, ballPosY, typeParty)
                        time.sleep(0.03)
                else:
                    while ballPosX < hitRight:
                        ballPosX += 18
                        self.ballSendToJs(ballPosX, ballPosY, typeParty)
                        time.sleep(0.03)
            elif ballPosX < hitLeft :
                ballPosX = 499
                ballPosY = 250
                self.scoreP2 += 1
            
            if self.rightBoxTop - ballPosY < 30 and self.rightBoxTop - ballPosY > -90 and ballPosX >= hitRight:
                if self.rightBoxTop - ballPosY > -20:
                    hitWall = 0        
                    while ballPosX > hitLeft:
                        if hitWall == 1:
                            ballPosY += 10
                        else:
                            ballPosY -= 10
                        if ballPosY <  0:
                            hitWall = 1
                        ballPosX -= 18
                        self.ballSendToJs(ballPosX, ballPosY, typeParty)
                        time.sleep(0.03)
                elif self.rightBoxTop - ballPosY < -50:
                    hitWall = 0
                    while ballPosX > hitLeft:
                        if hitWall == 1:
                            ballPosY -= 10
                        else:
                            ballPosY += 10
                        if ballPosY > 460:
                            hitWall = 1
                        ballPosX -= 18
                        self.ballSendToJs(ballPosX, ballPosY, typeParty)
                        time.sleep(0.03)
                else:
                    while ballPosX > hitLeft:
                        ballPosX -= 18
                        self.ballSendToJs(ballPosX, ballPosY, typeParty)
                        time.sleep(0.03)
            elif ballPosX > hitRight:
                ballPosX = 499
                ballPosY = 250
                self.scoreP1 += 1
        self.ballSendToJs(499, 250, typeParty)
        self.barSendToJs('ArrowUp', 250, 250)
        if typeParty == 'game':
            from .views import manager
            manager.endGame(self)
            return

    def ballSendToJs(self, ballPosX, ballPosY, typeParty):
        
        self.player1.send(text_data=json.dumps({
            'type':'game',
            'moov':'ball',
            'posX':ballPosX,
            'posY':ballPosY,
            'scoreP1':self.scoreP1,
            'scoreP2':self.scoreP2
        }))
        if typeParty == 'game':
            self.player2.send(text_data=json.dumps({
                'type':'game',
                'moov':'ball',
                'posX':ballPosX,
                'posY':ballPosY,
                'scoreP1':self.scoreP1,
                'scoreP2':self.scoreP2
            }))
        
        return
        
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
        return
