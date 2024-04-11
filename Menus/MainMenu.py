from Enums.Keys import Keys
from Game import Instance
from ursina import color as Color, Vec2, Vec3, Button, Entity
from ursina import application as SingletonApplication

class MainMenu(Entity):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(ignore_paused = True, **KWArgs)
        
        # Buttons
        
        Self.MenuEnabled = False
        
        Self.ZombieGameMode = Button("Zombies", color = Color.red, scale = Vec2(0.6, 0.1), position = Vec2(0, 0.1), enabled = Self.MenuEnabled)
        
        Self.Quit = Button("Quit", color = Color.black, scale = Vec2(0.6, 0.1), position = Vec2(0, -0.1), enabled = Self.MenuEnabled)
        
    def Trigger(Self):
        
        # Menu Enabled/Disable
        
        Self.MenuEnabled = not Self.MenuEnabled
        
        SingletonApplication.paused = Self.MenuEnabled
        
        # Each Entity
        
        Self.ZombieGameMode.enabled_setter(Self.MenuEnabled)
        
        Self.Quit.enabled_setter(Self.MenuEnabled)
        
        # Other Entities
        
        Instance.ShowMouse(not Self.MenuEnabled)
        
        Instance.LockMouse(not Self.MenuEnabled)
     
    def HandleInput(Self, Key):

        if Key == Keys.Escape:
            
            Self.Trigger()

