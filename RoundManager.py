from Game import Instance
from direct.task.Task import Task
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

        Self.Points = []

    def StartGame(Self, Map = "NoName"):

        Self.PlayerPoints = 0

        Self.Round = 1

        Instance.taskMgr.add(Self._MakeStartAnimation() )

    async def _MakeStartAnimation(Self):

        Instance.FPSController.Freeze(True)

        StartText = Text("Round 1")
        
        for i in range(40, -1, -1):
            newColor = rgba(1, 1, 1, i / 40)
            StartText.color = newColor
            await Task.pause(0.1)

        Instance.FPSController.Freeze(False)

        Destroy(StartText)