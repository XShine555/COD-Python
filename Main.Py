from ursina import Ursina, Entity, Vec3, Sky
from ursina import time as GlobalTime
from ursina.shaders import lit_with_shadows_shader
from physics3d import BoxCollider
from panda3d.bullet import BulletWorld
from Prefabs.PlayerController import PlayerController

from MultiplayerHandler.Server import Server
from MultiplayerHandler.Client import Client

Entity.default_shader = lit_with_shadows_shader

Main = Ursina()
World = BulletWorld()
World.setGravity(Vec3(0, -9.81, 0) )

#CS = Server("192.168.16.36", 8080)
Cl = Client("192.168.16.36", 8080)

Ground = Entity(model = 'plane', position = (0, 0, 0), scale = (62,0.1,62), texture = 'grass')
GroundCollider = BoxCollider(World, Ground)
GroundCollider.y = -1

Player = PlayerController(World, model = "cube", Height=2)

def update():
    DeltaTime = GlobalTime.dt
    World.doPhysics(DeltaTime)
    
    #CS.Server.process_net_events()
    Cl.Easy.process_net_events()
    
    Cl.Client.send_message("updatePosition", Player.position)

Sky()

Main.run()