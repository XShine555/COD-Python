from ursina import color as Color, Vec2, Vec3, Button
from Menu import Menu

class PauseInGame(Menu):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs)
        
        Self.Resume = Button("Zombies", color = Color.clear, scale = Vec2(0.2, 0.05), position = Vec2(0, 0.1), enabled = Self.Active)
        
        Self.Settings = Button("Settings", color = Color.clear, scale = Vec2(0.2, 0.05), position = Vec2(0, 0), enabled = Self.Active)
        
        Self.Quit = Button("Quit", color = Color.clear, scale = Vec2(0.2, 0.05), position = Vec2(0, -0.1), enabled = Self.Active)
        
    def Trigger(Self):
        
        Self.ShowMouse()
        
        Self.Resume.enabled_setter(Self.Active)
        
        Self.Settings.enabled_setter(Self.Active)
        
        Self.Quit.enabled_setter(Self.Active)