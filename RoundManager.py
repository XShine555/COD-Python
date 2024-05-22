from Game import Instance
from direct.task.Task import Task
from enemies.zombies import Zombies
from ursina import Text, destroy as Destroy, Vec4, Color, color
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
        
        Self.ZombiesInScene = 0

        Self.TotalZombiesRound = 0
        
        Self.ZombiesDeath = 0      
        
        Self.RoundText = None  
        
        Self.ZombiesEntities = []
        
    def Reset(Self):
        Self.Round = 1
        Self.ZombiesMATH = 0
        Self.ZombiesRound = 0
        Self.ZombiesInScene = 0
        Self.TotalZombiesRound = 0
        Self.ZombiesDeath = 0
        Self.RoundText = None
        Self.ZombiesEntities = []

    def StartGame(Self, Map = "NoName"):

        Instance.taskMgr.add(Self._MakeStartAnimation() )
    
    async def _spawnzombies(Self):
        for x in range(int(Self.ZombiesRound)):
            if Self.ZombiesInScene >= Self.MaxZombies:
                break
            Self.ZombiesInScene += 1
            Self.ZombiesRound -= 1
            if Self.Round > 7:
                zomb = Zombies(can_run=True)
            else:
                zomb = Zombies(can_run=False)
            Self.ZombiesEntities.append(zomb)
            await Task.pause(1)
            
    def setZombieDeath(Self, ent):
        Instance.RoundManager.ZombiesInScene -= 1
        Instance.RoundManager.ZombiesDeath += 1
        if ent in Self.ZombiesEntities:
            Self.ZombiesEntities.remove(ent)

    def checklast(Self):
        if Self.ZombiesInScene < Self.MaxZombies and Self.ZombiesRound >= 1:
            Self.ZombiesInScene += 1
            if Self.Round > 7:
                zomb = Zombies(can_run=True)
            else:
                zomb = Zombies(can_run=False)
            Self.ZombiesEntities.append(zomb)

            Self.ZombiesRound -= 1
        elif Self.TotalZombiesRound == Self.ZombiesDeath:
            Self.Round += 1
            Instance.taskMgr.add(Self._MakeStartAnimation() )

    async def _MakeStartAnimation(Self):
        
        if Self.Round == 1:
            Self.RoundText = Text(origin=(0, 0) )
            Self.RoundText.size = 0.1
            Self.RoundText.color = color.red
            Self.RoundText.text = str(Self.Round)
            
            Self.RoundText.animate_position((-0.85, -0.45), 4.0)
        
            StartText = Text(origin=(0, -1.0))
            StartText.size = 0.15
            StartText.text = "Round"
            
            for i in range(40, -1, -1):
                newColor = rgba(1, 1, 1, i / 40)
                StartText.color = newColor
                await Task.pause(0.1)
        else:
            Self.RoundText.animate_color(color.white, 1.0)
            await Task.pause(1)
            Self.RoundText.animate_color(color.red, 1.0)
            await Task.pause(1)
            Self.RoundText.animate_color(color.white, 1.0)
            await Task.pause(1)
            Self.RoundText.text = str(Self.Round)
            Self.RoundText.animate_color(color.red, 1.0)
            await Task.pause(1)
            
        await Task.pause(1)

        Self.ZombiesRound = floor(Self.BaseZombies * 0.9 * Self.Round)
        Self.TotalZombiesRound = Self.ZombiesRound
        Self.ZombiesInScene = 0        
        Self.ZombiesDeath = 0     
        
        if Self.Round == 1:
            Destroy(StartText)   
        
        Instance.taskMgr.add(Self._spawnzombies() )

    