from ursina import Ursina, Entity, Vec3, Sky
from ursina import time as GlobalTime
from ursina.shaders import lit_with_shadows_shader
from physics3d import BoxCollider, Debugger
from panda3d.bullet import BulletWorld
from Prefabs.PlayerController import PlayerController
from Prefabs.Zombie import Zombie

from MultiplayerHandler.Server import Server, Instance as SInstance
from MultiplayerHandler.Client import Client, Instance as CInstance

Entity.default_shader = lit_with_shadows_shader

Main = Ursina()
World = BulletWorld()
World.setGravity(Vec3(0, -9.81, 0) )

Debugger(World, wireframe=True)

SInstance = Server("192.168.16.36", 8080)
CInstance = Client("192.168.16.36", 8080)

Ground = Entity(model = 'plane', position = (0, 0, 0), scale = (62,0.1,62), texture = 'grass')
GroundCollider = BoxCollider(World, Ground)
GroundCollider.y = -1

_Ground = Entity(model = 'plane', position = (0, -4, 0), scale = (128,0.1,128), texture = 'grass')
_GroundCollider = BoxCollider(World, _Ground)
_GroundCollider.y = -5

Player = PlayerController(World, model = "cube", Height=2)
import random
from ursina import color

EntZombie = Zombie(World, model = "cube")

def update():
    DeltaTime = GlobalTime.dt
    World.doPhysics(DeltaTime)
    
    SInstance.Easy.process_net_events()
    CInstance.Easy.process_net_events()
    
    CInstance.Client.send_message("updatePosition", Player.world_position)
    CInstance.Client.send_message("updateRotation", Player.world_rotation)

Sky()

Main.run()