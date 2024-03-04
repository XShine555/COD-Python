from ursina import Entity

class PlayerRepresentation(Entity):
    
    def __init__(Self, **KWArgs ):
        
        super().__init__(**KWArgs)
        
    def UpdatePos(Self, Position):
        
        Self.position_setter(Position)
        
    def UpdateRot(Self, Rotation):
        
        Self.rotation_setter(Rotation)