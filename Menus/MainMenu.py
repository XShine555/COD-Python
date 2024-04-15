from ursina import color as Color, Vec2, Vec3, Button, Entity, Text, application as SingletonApplication, destroy as Destroy, camera as InstanceCamera
from Menu import Menu
from Game import Instance

class MainMenu(Menu):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs)
        
        Self.ZombieGameMode = Button("Zombies", color = Color.red, scale = Vec2(0.2, 0.1), position = Vec2(0, 0.1), enabled = Self.Active)
        
        Self.Quit = Button("Quit", color = Color.black, scale = Vec2(0.2, 0.1), position = Vec2(0, -0.1), enabled = Self.Active)
        
        Self.ZombieGameMode.on_click = Self.ShowMaps
        
        Self.Quit.on_click = SingletonApplication.quit
        
        # Show Maps Function

        Self.AvailableScenes = Instance.GetScenes()

        Self.AvailableMapsButtons = []

        Self.SpaceBetweenButtons = Vec2(0, 0.2)

    def Trigger(Self):
        
        Self.ShowMouse()
        
        Self.ZombieGameMode.enabled_setter(Self.Active)
        
        Self.Quit.enabled_setter(Self.Active)

        Self.HideMaps()

    def ShowMaps(Self):

        PositionOffset = Vec2(0, 0)

        for Scene in Self.AvailableScenes:

            PositionOffset += Self.SpaceBetweenButtons
            
            SanitizeName = Scene.replace('.py', '')

            SceneButton = Button(SanitizeName, color = Color.clear, scale = Vec2(0.2, 0.1), position = PositionOffset, enabled = True)

            SceneButton.on_click = lambda : Self.LoadSelectedMap(SanitizeName)

            Self.AvailableMapsButtons.append(SceneButton)

    def HideMaps(Self):

        for Button in Self.AvailableMapsButtons:

            Destroy(Button)

    def LoadSelectedMap(Self, Map):

        if Instance.LoadSceneSafely(Map):

            Self.Trigger()

            Instance.GameStarted = True

            Instance.RoundManager.StartGame()

            #Instance.StartGame()

        else:

            Self.ShowErrorOnLoading(Map)

    def ShowErrorOnLoading(Self, Map):

        pass