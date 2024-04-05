from Scene import Scene
from ursina import Entity
from physics3d import BoxCollider
from Game import Instance

class Casa(Scene):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        
        #Self.Wall1 = Entity(model = 'cube', parent=Self.parent, position = (0, 0, 0), scale = (4,1,4), rotation = (90, 0, 0) )
        #Self.Wall1 = BoxCollider(Instance.BulletWorld, Self.Wall1)
        #Self.Wall1.y = -1