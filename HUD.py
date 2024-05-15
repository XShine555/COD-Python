from ursina import Entity

class HUD(Entity):
    
    def __init__(Self):
        
        super().__init__()
        
        Self.IsWeaponHudActive = True
        
        Self.ToggleWeaponHud()
        
    def ToggleWeaponHud(Self):
        
        pass