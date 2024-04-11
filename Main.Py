from ursina import Vec3, Entity
from PlayerController import PlayerController
from Weapons.Glock17 import Glock17
from ursina import EditorCamera, camera as InstanceCamera, application
from Game import Instance
from Menus.MainMenu import MainMenu
from Menus.PauseInGame import PauseInGame
from Enums.Keys import Keys

Instance.LoadScene("Town")
#Instance.LoadScene("Casa")

Instance.FPSController = PlayerController(World = Instance.BulletWorld, model = "cube", Height = 4, collider = 'box')

Gun = Glock17()
Gun.parent = InstanceCamera

Instance.MainMenu = MainMenu()
Instance.MainMenu.Trigger()
Instance.Escape = PauseInGame(KeyToActive = Keys.Escape)
#Instance.Menu.Trigger()

Instance.EnableShowFPS()

Instance.LimitFPS(60)

Instance.Run()