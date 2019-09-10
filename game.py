import math
import time
from subprocess import call
from objects import Enemy,Bullet,Player,direction
import asyncio
from getch import getch
import random
def check_collision(i,j):
    return 1

class Agent():

    def __init__(self):
        self.choices = ['a','d',' ']
    def get_move(self):
        choose = random.choice(self.choices)
        return choose
agent = Agent()
class Game():
    def __init__(self):
        self.score = 0
        self.graphic = []
        self.objects = []
        self.shifty = 0
        self.player = Player(20,75,game=self)
        for i in range(0,20):
            for j in range(1,3):
                self.objects.append(Enemy(i*10,j*10,game=self))
        for i in range(0,40):
            self.graphic.append([])
            for j in range(0,80):
                if((j)%2==0 and i ==self.shifty):
                    self.graphic[i].append("A")
                else:
                    self.graphic[i].append("'")
    async def getinput(self):
        inputa = agent.get_move()
        if('a' == inputa):
            self.player.move(direction(-2,0))
        elif('d' == inputa):
            self.player.move(direction(2,0))
        elif(' ' == inputa):
            self.player.shoot()
    async def gameloop(self):
        if random.randint(0,4)==0:
            self.objects.append(Enemy(30,20,game=self))
        row = 0
        toprint = ""
        for i in range(0,40):
            for j in range(0,80):
                if((j)%2==0 and i ==self.shifty):
                    self.graphic[i][j] = "A"
                elif self.graphic[i][j]=="{" or self.graphic[i][j]=="}":
                    self.graphic[i][j] = "o"
                else:
                    self.graphic[i][j] = "'"
        #after initialization
        #for all the self.objects, render their position
        for idx,obj in enumerate(self.objects):
            render = obj.render()
            if(obj.type == "bullet" and type(obj.parent)==Player):
                for tracy,row in enumerate(render):
                    for tracx,c in enumerate(row):
                        if(self.graphic[(obj.y+tracy)%40][(obj.x-1+tracx)%80]!="'"):
                            for i in range(0,2):
                                for j in range(0,2):
                                    self.graphic[(obj.y+i)%40][(obj.x+j)%80] =\
                                        random.choice(['{','}'])
                        if(self.graphic[(obj.y+tracy)%40][(obj.x-1+tracx)%80]=="{" or\
                           self.graphic[(obj.y+tracy)%40][(obj.x-1+tracx)%80]=="}"):
                            self.objects[idx].state="destroyed"
                        else:
                            self.graphic[(obj.y-1+tracy)%40][(obj.x-1+tracx)%80] = c
            elif(obj.type=="enemy"):
                if random.randint(0,20) ==0:
                    obj.shoot(direction=1,velocity=2)
                for tracy,row in enumerate(render):
                    for tracx,c in enumerate(row):
                        if(self.graphic[(obj.y-1+tracy)%40][(obj.x-3+tracx)%80]=="o"):
                            destroyed = obj.damage()
                            if(destroyed):
                                self.score += 100
                        else:
                            self.graphic[(obj.y-1+tracy)%40][(obj.x-3+tracx)%80] = c
            else:
                 for tracy,row in enumerate(render):
                    for tracx,c in enumerate(row):
                        if(self.graphic[(obj.y+tracy)%40][(obj.x-1+tracx)%80]=="{" or\
                           self.graphic[(obj.y+tracy)%40][(obj.x-1+tracx)%80]=="}"):
                            self.objects[idx].state="destroyed"
                        else:
                            self.graphic[(obj.y-1+tracy)%40][(obj.x-1+tracx)%80] = c
            if(obj.state== "destroyed"):
                self.objects.remove(obj)
        render = self.player.render()
        for tracy,row in enumerate(render):
            for tracx,c in enumerate(row):
                if(self.graphic[(self.player.y-1+tracy)%40][(self.player.x-2+tracx)%80] in
                   ["{","}","[","]"]):
                      self.player.state="destroyed"
                else:
                    self.graphic[(self.player.y-1+tracy)%40][(self.player.x-2+tracx)%80] = c
        toprint += "score: " + str(self.score)
        toprint += "\n"
        toprint += "\n"
        if self.player.state !="destroyed":
            for y in range(0,40):
                toprint +="\n"
                for x in range(0,80):
                    toprint += self.graphic[y][x]
            call(['clear'])            
            print(toprint)
            print("player:",self.player.x,self.player.y,self.player.state)
            time.sleep(0.1)
        else:
            while(True):
                for y in range(0,40):
                    toprint +="\n"
                    for x in range(0,80):
                        toprint += self.graphic[y][x]
                call(['clear'])
                print(toprint)
                print("player:",self.player.x,self.player.y,self.player.state)
                print("GAME OVER!!!")
                time.sleep(0.1)
        
    async def main(self):
        await asyncio.gather(self.gameloop(),self.getinput())
if __name__=="__main__":
    game = Game()
    while(True):
     asyncio.run(game.main())
