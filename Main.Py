from ursina import Vec3, Entity
from PlayerController import PlayerController
from Weapons.Glock17 import Glock17
from ursina import *
from Game import Instance

Instance.LoadScene("Town")

Instance.FPSController = PlayerController(World = Instance.BulletWorld, model = "cube", Height=2)
Gun = Glock17()
Gun.parent = camera

Instance.run()