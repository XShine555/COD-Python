from ursina import color as Color, Vec2, Vec3, Button, application as SingletonApplication
from Menu import Menu

class MainMenu(Menu):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs)
        
        Self.ZombieGameMode = Button("Zombies", color = Color.red, scale = Vec2(0.6, 0.1), position = Vec2(0, 0.1), enabled = Self.Active)
        
        Self.Quit = Button("Quit", color = Color.black, scale = Vec2(0.6, 0.1), position = Vec2(0, -0.1), enabled = Self.Active)
        
        Self.ZombieGameMode.on_click = Self.Trigger
        
        Self.Quit.on_click = SingletonApplication.quit
        
    def Trigger(Self):
        
        Self.ShowMouse()
        
        Self.ZombieGameMode.enabled_setter(Self.Active)
        
        Self.Quit.enabled_setter(Self.Active)