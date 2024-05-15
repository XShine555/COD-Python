from ursina import Vec3, Entity
from PlayerController import PlayerController
from Weapons.Glock17 import Glock17
from ursina import camera as InstanceCamera
from Game import Instance
from Menus.MainMenu import MainMenu
from Menus.PauseInGame import PauseInGame
from Enums.Keys import Keys
from RoundManager import RoundManager
from enemies.zombies import Zombies
from Minigames.Minesweeper import MineSweeper

from physics3d import Debugger

A = Instance.LoadSceneSafely("Town")
#Instance.LoadSceneSafely("Casa")

Instance.FPSController = PlayerController(World = Instance.BulletWorld, model = "cube", Height = 4, collider = 'box')
Instance.GameStarted = False
Instance.RoundManager = RoundManager()

Deb = Debugger(Instance.BulletWorld, wireframe = True)

#Gun = Glock17()
#Gun.parent = InstanceCamera

Instance.MainMenu = MainMenu()
Instance.MainMenu.Trigger()
Instance.Escape = PauseInGame(KeyToActive = Keys.Escape)
#Instance.Menu.Trigger()
Instance.EnableShowFPS()

#Instance.LimitFPS(60)
#Instance.enemies = Zombies()

#A = MineSweeper()

Instance.Run()