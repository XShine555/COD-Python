from ursina import color as Color, Vec2, Vec3, Button, Entity, Text, application as SingletonApplication, destroy as Destroy, camera as InstanceCamera
from Menu import Menu
from Game import Instance, ApplicationSingleton

class MainMenu(Menu):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs)
        
        Self.ZombieGameMode = Button(
            "Zombies", 
            color = Color.red, 
            scale = Vec2(0.2, 0.1), 
            position = Vec2(0, 0.1), 
            enabled = Self.Active
        )
        
        Self.Quit = Button(
            "Quit", 
            color = Color.black, 
            scale = Vec2(0.2, 0.1), 
            position = Vec2(0, -0.1), 
            enabled = Self.Active
        )

        Self.GoBack = Button(
            "Return", 
            color = Color.black, 
            scale = Vec2(0.2, 0.1), 
            position = Vec2(0, -0.1), 
            enabled = False,
            on_click = Self.Return
        )
        
        Self.ZombieGameMode.on_click = Self.ShowMaps
        
        Self.Quit.on_click = SingletonApplication.quit
        
        # Show Maps Function

        Self.AvailableScenes = Instance.GetScenes()

        Self.AvailableMapsButtons = []

        Self.SpaceBetweenButtons = Vec2(0, 0.15)

    def Trigger(Self):
        
        Self.ToggleMenu()
        
        Self.ZombieGameMode.enabled_setter(Self.Active)
        
        Self.Quit.enabled_setter(Self.Active)

        Self.HideMaps()

    def Return(Self):

        Self.HideMaps()

        Self.ZombieGameMode.enabled_setter(True)
        
        Self.Quit.enabled_setter(True)

        Self.GoBack.enabled_setter(False)

    def ShowMaps(Self):

        PositionOffset = Vec2(0, -0.1)

        Self.ZombieGameMode.enabled_setter(False)

        Self.GoBack.enabled_setter(True)

        Self.Quit.enabled_setter(False)

        for Scene in Self.AvailableScenes:

            PositionOffset += Self.SpaceBetweenButtons
            
            SanitizeName = Scene.replace('.py', '')

            SceneButton = Button(
                SanitizeName, 
                color = Color.red, 
                scale = Vec2(0.2, 0.1),
                position = PositionOffset, 
                enabled = True
            )
            
            SceneButton.on_click = lambda s=SanitizeName: Self.LoadSelectedMap(s)

            Self.AvailableMapsButtons.append(SceneButton)

    def HideMaps(Self):

        for Button in Self.AvailableMapsButtons:

            Destroy(Button)

    def LoadSelectedMap(Self, Map):
        
        if Instance.LoadSceneSafely(Map):

            Self.Trigger()

            Instance.GameStarted = True

            Instance.RoundManager.StartGame()

        else:

            Self.ShowErrorOnLoading(Map)

        Self.GoBack.enabled_setter(False)

    def ShowErrorOnLoading(Self, Map):

        pass