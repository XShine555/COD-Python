from ursina import Entity

class Scene(Entity):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        
    def EnableScene(Self):
        
        Self.enable()
        
    def DisableScene(Self):
        
        Self.disable()
        
    def DestroyScene(Self):
        
        Self.destroy()