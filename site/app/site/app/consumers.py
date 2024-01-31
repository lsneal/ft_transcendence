import json
import sys
import time 
import threading
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .classPong import Pong

class ChatConsumer(WebsocketConsumer):
    thisdict = {}

    def connect(self):
        #self.room_group_name = 'test'
        #
        #async_to_sync(self.channel_layer.group_add)(
        #    self.room_group_name,
        #    self.channel_name
        #)
        
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        moov = text_data_json['moov']
        game = text_data_json['game']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'game',
                'game':game,
            }
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'bar_moov',
                'moov':moov,
            }
        )

    def bar_moov(self, event):
        moov = event['moov']

        if moov == 'w' and self.thisdict[1].leftBoxTop > 0:
            self.thisdict[1].leftBoxTop -= 30
        if moov == 's' and self.thisdict[1].leftBoxTop < 430:
            self.thisdict[1].leftBoxTop += 30    
        if moov == 'ArrowUp' and self.thisdict[1].rightBoxTop > 0:
            self.thisdict[1].rightBoxTop -= 30
        if moov == 'ArrowDown' and self.thisdict[1].rightBoxTop < 430:
            self.thisdict[1].rightBoxTop += 30
        self.send(text_data=json.dumps({
            'type':'game',
            'moov':moov,
            'leftBoxTop': self.thisdict[1].leftBoxTop,
            'rightBoxTop': self.thisdict[1].rightBoxTop
        }))
    
    def game(self, event):
        game = event['game']

        if game == 'start':
            value = Pong()
            self.thisdict[1] = value
            t = threading.Thread(target=self.ball, args=())
            t.start()
        #if game == 'in progress':
            #print('LeftTopBox: ',  self.thisdict[1].getLeftTop(),file=sys.stderr)



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
                    ballPosX -= 18
                    self.sendToJs(ballPosX, ballPosY, scoreP1, scoreP2)
                    time.sleep(0.03)
            #print('ballPosX = ', ballPosX, 'hitLeft', hitLeft)
            
            if self.thisdict[1].leftBoxTop - ballPosY < 30 and self.thisdict[1].leftBoxTop - ballPosY > -90 and ballPosX <= hitLeft:
                print('HITEEEEEEEEEE left box',file=sys.stderr)
                if self.thisdict[1].leftBoxTop - ballPosY > -20:
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
                elif self.thisdict[1].leftBoxTop - ballPosY < -50:
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
            
            if self.thisdict[1].rightBoxTop - ballPosY < 30 and self.thisdict[1].rightBoxTop - ballPosY > -90 and ballPosX >= hitRight:
                print('HITEEEEEEEEEE right box',file=sys.stderr)
                if self.thisdict[1].rightBoxTop - ballPosY > -20:
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
                elif self.thisdict[1].rightBoxTop - ballPosY < -50:
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
        self.send(text_data=json.dumps({
            'type':'game',
            'moov':'ball',
            'posX':ballPosX,
            'posY':ballPosY,
            'scoreP1':scoreP1,
            'scoreP2':scoreP2
        }))

#
#
    #def connect(self):
    #    self.room_group_name = 'test'
    #    
    #    async_to_sync(self.channel_layer.group_add)(
    #        self.room_group_name,
    #        self.channel_name
    #    )
#
    #    self.accept()
    #    t = threading.Thread(target=self.ball, args=())
    #    t.start()
#
    #def receive(self, text_data):
    #    text_data_json = json.loads(text_data)
    #    moov = text_data_json['moov']
    #    
    #    async_to_sync(self.channel_layer.group_send)(
    #        self.room_group_name,
    #        {
    #            'type':'bar_moov',
    #            'moov':moov
    #        }
    #    )
#
    #def bar_moov(self, event):
    #    moov = event['moov']
#
    #    self.send(text_data=json.dumps({
    #        'type':'game',
    #        'moov':moov
    #    }))
    #    print('sleep: ', moov,file=sys.stderr)
#
#
#
#
#
#



#    def receive(self, text_data):
#        text_data_json = json.loads(text_data)
#        message = text_data_json['message']
#
#        async_to_sync(self.channel_layer.group_send)(
#            self.room_group_name,
#            {
#                'type':'chat_message',
#                'message':message
#            }
#        )
#    
#    def chat_message(self, event):
#        message = event['message']
#
#        self.send(text_data=json.dumps({
#            'type':'chat',
#            'message':message
#        }))