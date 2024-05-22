from ursina import Entity, application as SingletonApplication
from Enums.Keys import Keys
from Game import Instance

ActiveMenus = []

class Menu(Entity):
    
    def __init__(Self, KeyToActive = None, IgnorePaused = True, PauseOnActive = True, **KWArgs):
        
        super().__init__(ignore_paused = IgnorePaused, **KWArgs)
        
        Self.Active = False
        
        Self.PauseOnActive = PauseOnActive
        
        Self.KeyToActive = KeyToActive
        
    def Enable(Self):
        
        Self.Active = True
        
    def Disable(Self):
        
        Self.Active = False
        
    def ToggleMenu(Self):
        
        Instance.ShowMouse(Self.Active)
        
        Instance.LockMouse(Self.Active)
        
        Self.Active = not Self.Active
        
        if Self.PauseOnActive:
            
            SingletonApplication.paused = Self.Active
            
        if Self.Active and not Self in ActiveMenus:
            
            ActiveMenus.append(Self)
            
        elif not Self.Active and Self in ActiveMenus:
            
            ActiveMenus.remove(Self)
        
    def Trigger(Self):
        
        pass
    
    def HandleInput(Self, Key):
        
        if Key == Self.KeyToActive and Instance.GameStarted:
            
            Self.Trigger()