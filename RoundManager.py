from Game import Instance

class RoundManager():

    def __init__(Self) -> None:
        
        Self.Round = 1

        Self.Points = []

    def StartGame(Self, Map):

        Self.PlayerPoints = 0

        Self.Round = 1

        Instance.taskMgr.add(Self._MakeStartAnimation() )

    async def _MakeStartAnimation(Self, Task):

        Self.SetupPlayer()

        Self.FPSController.Freeze = True

        await Task.pause(4)

        Instance.FPSController.Freeze = False