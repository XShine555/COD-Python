from Game import Instance
from direct.task.Task import Task
from enemies.zombies import Zombies
from ursina import Text, destroy as Destroy, Vec4, Color
from math import floor

def rgba(r, g, b, a=255):
    color = Color(r, g, b, a)
    if color[0] > 1 or color[1] > 1 or color[2] > 1 or color[3] > 1:
        color = Color(tuple(c/255 for c in color))
    # color[3] = min(1, color[3])
    return color

class RoundManager():

    def __init__(Self) -> None:
        
        Self.Round = 1

        Self.BaseZombies = 6

        Self.MaxZombies = 4

        Self.ZombiesMATH = 0

        Self.ZombiesRound = 0

        Self.TotalZombiesRound = 0
        
        Self.ZombiesDeath = 0        


    def StartGame(Self, Map = "NoName"):

        Instance.taskMgr.add(Self._MakeStartAnimation() )
    
    async def _spawnzombies(Self):
        for x in range(int(Self.ZombiesRound)):
            if Self.ZombiesInScene >= Self.MaxZombies:
                break
            Self.ZombiesInScene += 1
            Self.ZombiesRound -= 1
            if Self.Round > 7:
                Zombies(can_run=True)
            #elif Self.Round > 4:
                #pass
            else:
                Zombies(can_run=False)
            await Task.pause(1)

    def checklast(Self):
        if Self.ZombiesInScene < Self.MaxZombies and Self.ZombiesRound > 0:
            print("AQUI SI")
            if Self.Round > 7:
                Zombies(can_run=True)
            else:
                Zombies(can_run=False)
            Self.ZombiesInScene += 1
            Self.ZombiesRound -= 1

        elif Self.TotalZombiesRound == Self.ZombiesDeath:
            Self.Round += 1
            Instance.taskMgr.add(Self._MakeStartAnimation() )

        #print(Self.ZombiesRound)
        #print(Self.ZombiesRound, Self.TotalZombiesRound)



    async def _MakeStartAnimation(Self):

        #Instance.FPSController.Freeze(True)

        StartText = Text(f"Round {Self.Round}")
        
        #for i in range(40, -1, -1):
            #newColor = rgba(1, 1, 1, i / 40)
            #StartText.color = newColor
            #await Task.pause(0.1)

        Instance.FPSController.Freeze(False)

        Self.ZombiesRound = floor(Self.BaseZombies * 0.9 * Self.Round)
        Self.TotalZombiesRound = Self.ZombiesRound
        Self.ZombiesInScene = 0        
        Self.ZombiesDeath = 0        

        Destroy(StartText)

        #await Task.pause(3)

        #Instance.taskMgr.add(Self._spawnzombies() )

    