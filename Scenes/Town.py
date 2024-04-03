from Scene import Scene
from ursina import Entity
from physics3d import BoxCollider
from Game import Instance

class Town(Scene):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.Ground = Entity(model = 'plane', parent=Self.parent, position = (0, 0, 0), scale = (62,0.1,62), texture = 'grass')
        Self.GroundCollider = BoxCollider(Instance.BulletWorld, Self.Ground)
        Self.GroundCollider.y = -1