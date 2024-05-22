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

class Mine(Scene):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        print("mine")
        Self.Ground = Entity(model = 'plane', texture = 'Textures/oak_planks_mine.png', texture_scale = (16, 16), parent = Self, position = (0, 0, 0), scale = (92,0.1,92), collider = 'box')
        Self.GroundCollider = BoxCollider(Instance.BulletWorld, Self.Ground)
        Self.GroundCollider.y = -1

        #Self.Wall1 = Entity(model = 'cube', texture = 'Textures/cobble.png', texture_scale = (32, 6), parent = Self, position = (0, 0, 46), scale = (92,18,1), collider = 'box')
        #Self.Wall1Collider = BoxCollider(Instance.BulletWorld, Self.Wall1)

        Self.Box = Box(model = 'Models/mystery_box.glb',  parent = Self, position = (0, 1, 0), scale = 2.5, collider = 'box')

        #RESPAWNS

        Self.Respawns = [
            Entity(model = "cube", scale = 1, x = 27, z = 27),
            Entity(model = "cube", scale = 1, x = -27, z = 27),
            Entity(model = "cube", scale = 1, x = 27, z = -27),
            Entity(model = "cube", scale = 1, x = -27, z = -27)
        ]
        
        Self.Sun = DirectionalLight()
        Self.Sun.look_at(Vec3(1,-1,-1) )
        Self.Sky = Sky()

