from ursina import Vec3, Entity
from PlayerController import PlayerController
from Weapons.Glock17 import Glock17
from ursina import EditorCamera, camera as InstanceCamera, application
from Game import Instance
from Menus.MainMenu import MainMenu

Instance.LoadScene("Town")
#Instance.LoadScene("Casa")

Instance.FPSController = PlayerController(World = Instance.BulletWorld, model = "cube", Height = 4, collider = 'box')
Instance.EditorCamera = EditorCamera()

Gun = Glock17()
Gun.parent = InstanceCamera

Instance.Menu = MainMenu()
Instance.Menu.menu2()
Instance.Menu.button3.on_click = Instance.Menu.menu2
Instance.Menu.button4.on_click = application.quit

Instance.EnableShowFPS()

Instance.LimitFPS(60)

Instance.Run()