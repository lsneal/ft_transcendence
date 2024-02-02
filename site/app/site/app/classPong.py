#from .views import manager
import json
import threading
import sys
import time
#from channels.generic.websocket import WebsocketConsumer
#from asgiref.sync import async_to_sync

class Pong:
    def __init__(self, Player1, id):
        self.leftBoxTop = 250
        self.rightBoxTop = 250
        self.player1 = Player1
        self.player2 = None
        self.id = id

    def bar_moov(self, moov):
        
        if moov == 'w' and self.leftBoxTop > 0:
            self.leftBoxTop -= 30
        if moov == 's' and self.leftBoxTop < 430:
            self.leftBoxTop += 30    
        if moov == 'ArrowUp' and self.rightBoxTop > 0:
            self.rightBoxTop -= 30
        if moov == 'ArrowDown' and self.rightBoxTop < 430:
           self.rightBoxTop += 30
        
        self.player1.send(text_data=json.dumps({
            'type':'game',
            'moov':moov,
            'leftBoxTop': self.leftBoxTop,
            'rightBoxTop': self.rightBoxTop
        }))
        self.player2.send(text_data=json.dumps({
            'type':'game',
            'moov':moov,
            'leftBoxTop': self.leftBoxTop,
            'rightBoxTop': self.rightBoxTop
        }))
    
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
        print("ball start moov")
        while (scoreP1 < 5 and scoreP2 < 5):
            if ballPosX == 499 and ballPosY == 250:
                while ballPosX > hitLeft: #go left mid
                    ballPosX -= 15
                    self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                    time.sleep(0.03)            
            if self.leftBoxTop - ballPosY < 30 and self.leftBoxTop - ballPosY > -90 and ballPosX <= hitLeft:
                print('HITEEEEEEEEEE left box',file=sys.stderr)
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
                        self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
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
                        self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
                else:
                    print('to right direction mid')
                    while ballPosX < hitRight:
                        ballPosX += 18
                        self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
            elif ballPosX < hitLeft :
                ballPosX = 499
                ballPosY = 250
                scoreP2 += 1
            
            if self.rightBoxTop - ballPosY < 30 and self.rightBoxTop - ballPosY > -90 and ballPosX >= hitRight:
                print('HITEEEEEEEEEE right box',file=sys.stderr)
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
                        self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
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
                        self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
                else:
                    print('to right direction mid')
                    while ballPosX > hitLeft:
                        ballPosX -= 18
                        self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                        time.sleep(0.03)
            elif ballPosX > hitRight:
                ballPosX = 499
                ballPosY = 250
                scoreP1 += 1
            
    def sendToJs(self, ballPosX, ballPosY, scoreP1, scoreP2):
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