from ursina import Vec3, Entity
from PlayerController import PlayerController
from Weapons.Glock17 import Glock17
from ursina import camera as InstanceCamera
from Game import Instance
from Menus.MainMenu import MainMenu
from Menus.PauseInGame import PauseInGame
from Enums.Keys import Keys
from RoundManager import RoundManager

A = Instance.LoadSceneSafely("Town")
#Instance.LoadSceneSafely("Casa")

Instance.FPSController = PlayerController(World = Instance.BulletWorld, model = "cube", Height = 4, collider = 'box')
Instance.GameStarted = False
Instance.RoundManager = RoundManager()

Gun = Glock17()
Gun.parent = InstanceCamera

Instance.MainMenu = MainMenu()
Instance.MainMenu.Trigger()
Instance.Escape = PauseInGame(KeyToActive = Keys.Escape)
#Instance.Menu.Trigger()

Instance.EnableShowFPS()

#Instance.LimitFPS(60)

Instance.Run()