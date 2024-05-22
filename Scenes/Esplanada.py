from Scene import Scene
from ursina import Entity, Sky, DirectionalLight
from ursina.shaders import lit_with_shadows_shader
from physics3d import BoxCollider, MeshCollider
from Game import Instance
from Props.Box import Box

from ursina import destroy

from ursina import Vec3
from panda3d.core import LMatrix3
from panda3d.bullet import BulletBodyNode, BulletRigidBodyNode, BulletGhostNode

class Esplanada(Scene):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.Ground = Entity(model = 'plane', parent = Self, position = (0, 0, 0), scale = (256,0.1,256), texture = 'grass', collider = 'box')
        Self.GroundCollider = BoxCollider(Instance.BulletWorld, Self.Ground)
        Self.GroundCollider.scale_x = 4
        Self.GroundCollider.scale_z = 4
        Self.GroundCollider.y = -1
        
        Self.Box = Box(model = 'Models/mystery_box.glb',  parent = Self, position = (0, 1, 0), scale = 2.5, collider = 'box')

        #RESPAWNS

        Self.Respawns = [
            Entity(model = "cube", scale = 1, x = 42, z = 3),
            Entity(model = "cube", scale = 1, x = -37, z = 7),
            Entity(model = "cube", scale = 1, x = 28, z = -17),
            Entity(model = "cube", scale = 1, x = 15, z = -33),
            Entity(model = "cube", scale = 1, x = 56, z = -23),
            Entity(model = "cube", scale = 1, x = 34, z = -17),
            Entity(model = "cube", scale = 1, x = -14, z = -57)
        ]
        
       # Self.Sun = DirectionalLight()
        #Self.Sun.look_at(Vec3(1,-1,-1) )
        #Self.Sky = Sky()

