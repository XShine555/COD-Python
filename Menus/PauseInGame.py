from ursina import color as Color, Vec2, Vec3, Button
from Menu import Menu
from Game import ApplicationSingleton

class PauseInGame(Menu):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs)
        
        Self.Resume = Button("Resume", on_click = Self.Resume, color = Color.clear, scale = Vec2(0.2, 0.05), position = Vec2(0, 0.1), enabled = Self.Active)
        
        Self.Settings = Button("Settings", on_click = Self.Settings, color = Color.clear, scale = Vec2(0.2, 0.05), position = Vec2(0, 0), enabled = Self.Active)
        
        Self.Quit = Button("Quit", on_click = Self.Quit, color = Color.clear, scale = Vec2(0.2, 0.05), position = Vec2(0, -0.1), enabled = Self.Active)
        
    def Trigger(Self):
        
        Self.ToggleMenu()
        
        Self.Resume.enabled_setter(Self.Active)
        
        Self.Settings.enabled_setter(Self.Active)
        
        Self.Quit.enabled_setter(Self.Active)

    def Resume(Self):

        Self.ToggleMenu()

        Self.Resume.enabled_setter(Self.Active)
        
        Self.Settings.enabled_setter(Self.Active)
        
        Self.Quit.enabled_setter(Self.Active)

    def Settings(Self):

        pass

    def Quit(Self):

        ApplicationSingleton.quit()