from Game import Instance
from direct.task.Task import Task
from enemies.zombies import Zombies
from ursina import Text, destroy as Destroy, Vec4, Color

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

        Self.Points = 1000

        Self.MaxZombies = 150

        Self.ZombiesInScene = 0

        Self.ZombiesRound = Self.BaseZombies * 1.5 * Self.Round


    def StartGame(Self, Map = "NoName"):

        Self.PlayerPoints = 0

        Self.Round = 1

        Instance.taskMgr.add(Self._MakeStartAnimation() )
    
    async def _spawnzombies(Self):
        for x in range(1): #int(Self.ZombiesRound)
            Self.ZombiesInScene += 1
            if Self.Round > 7:
                Zombies(can_run=True)
            elif Self.Round > 4:
                pass
            else:
                Zombies(can_run=False)
            await Task.pause(1)

        print(Self.ZombiesInScene)


    
    def checklast(Self):
        if Self.ZombiesInScene == 0:
            Self.Round += 1
            Instance.taskMgr.add(Self._MakeStartAnimation() )


    async def _MakeStartAnimation(Self):

        #Instance.FPSController.Freeze(True)

        StartText = Text(f"Round {Self.Round}")
        
        #for i in range(40, -1, -1):
            #newColor = rgba(1, 1, 1, i / 40)
            #StartText.color = newColor
            #await Task.pause(0.1)

        Instance.FPSController.Freeze(False)

        Destroy(StartText)

        #await Task.pause(3)

        #Instance.taskMgr.add(Self._spawnzombies() )

    