from Scene import Scene
from ursina import Entity
from physics3d import BoxCollider
from Game import Instance

from ursina import destroy

from ursina import Vec3
from panda3d.core import LMatrix3
from panda3d.bullet import BulletBodyNode, BulletRigidBodyNode, BulletGhostNode

class Town(Scene):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.Ground = Entity(model = 'plane', parent = Self, position = (0, 0, 0), scale = (62,0.1,62), texture = 'grass')
        Self.GroundCollider = BoxCollider(Instance.BulletWorld, Self.Ground)
        Self.GroundCollider.y = -1