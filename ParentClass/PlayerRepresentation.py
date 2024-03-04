from ursina import Entity

class PlayerRepresentation(Entity):
    
    def __init__(Self, Position = (0, 0, 0), Rotation = (0, 0, 0), **KWArgs ):

        super().__init__(**KWArgs)
        
        Self.position_setter(Position)
        
        Self.rotation_setter(Rotation)
        
    def UpdatePos(Self, Position):
        
        Self.position_setter(Position)
        
    def UpdateRot(Self, Rotation):
        
        Self.rotation_setter(Rotation)