from collections import namedtuple

direction = namedtuple("direction","x y")
class Bullet():

    def __init__(self,x,y,direction=-1,velocity=4,parent=None):
        self.x = x
        self.y = y
        self.type="bullet"
        self.parent = parent
        self.state ="first"
        self.direction = direction
        self.velocity = velocity
    def move(self,direction):
        self.x = (self.x + direction.x)%80
        self.y = (self.y + direction.y)
    def render(self):
        if(self.state=="first"):
            #animate the bullet
            #      []
            self.move(direction(0,self.velocity*self.direction))
            if(self.y<=0 or self.y>39):
                self.y = 0
                self.state = "destroyed"
                return ["'"]
            if self.direction ==1:
                return ["[]"]
            else:
                return ["8"]
        elif(self.state=="destroyed"):
            #bullet destroyed
            #     {}
            return ["{}"]

class Enemy():
    def __init__(self,x,y,game=None,skin="cat"):
        self.x = x
        self.y = y
        self.type = "enemy"
        self.state ="left"
        self.skin="cat"
        self.lifepoints = 3
        self.game = game
    def move(self,direction):
        self.x = (self.x + direction.x)%80
        self.y = (self.y + direction.y)%40
    def damage(self):
        self.lifepoints -= 1
        if self.lifepoints ==0:
            self.state = "destroyed"
            return True
        else:
            return False
    def shoot(self,direction,velocity):
        self.game.objects.append(Bullet(self.x,self.y,direction,velocity,parent=self))
    def render(self):
        if self.skin =="cat":
            if(self.state=="left"):
                #animate first move
                #      A___ A
                #      |=  =| 
                #     ~  [] ~
                self.move(direction(-1,0))
                self.state = "right"
                return [" A___ A",\
                        " |=  =|",\
                        "~  [] ~"] 
            elif(self.state=="right"):
                #animate second move
                #       A___ A
                #      ~|=  =|~ 
                #        []
                self.move(direction(1,0))
                self.state = "left"
                return [" A___ A",\
                        "|=  =| ",\
                        " ~ [] ~"] 
            elif(self.state=="destroyed"):
                #animate second move
                #     {}A__{}
                #     _|X X|{
                #     _ {} {}
                return ["{}A__{}",\
                        "_|X X|{",\
                        "_ {} {}"] 

class Player():

    def __init__(self,x,y,game=None):
        self.x = x
        self.y = y
        self.type = "player"
        self.state ="left"
        self.game = game
    def move(self,direction):
        self.x = (self.x + direction.x)%80
        self.y = (self.y + direction.y)%40
    def shoot(self):
        self.game.objects.append(Bullet(self.x,self.y,parent=self))
    def render(self):
        if(self.state=="left"):
            #animate first move
            #     |    |
            #     |-<>-|
            return ["|    |",\
                    "|-<>-|"]
        elif(self.state=="right"):
            #animate second move
            #     |    |
            #     |-<>-|
            return ["|    |",\
                    "|-<>-|"]
        elif(self.state=="destroyed"):
            #animate second move
            #     {}A__{}
            #     _|X X|{
            #     _ {} {}
            return ["{}{{}}",\
                    "|{}}}|"]

