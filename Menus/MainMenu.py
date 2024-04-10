from Enums.Keys import Keys
from Game import Instance
from ursina.mouse import instance as InstanceMouse
from ursina import color, Vec2, Vec3, Button, Entity, application

class MainMenu (Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, ignore_paused=True, **kwargs)
        self.buttons_enabled = False
        self.button3 = Button(text="Zombies", color=color.red, scale=(0.6, 0.1), position=(0, 0.1),enabled = False)
        self.button4 = Button(text="Exit", color=color.black, scale=(0.6, 0.1), position=(0, -0.1), enabled = False)
        #self.pause_handler = Entity(ignore_paused=True, input=self.inputmenu)
        #self.button3.on_click = self.button3cllick

    def menu2 (self):
        self.buttons_enabled = not self.buttons_enabled
        Instance.menu = self.buttons_enabled
        Instance.FPSController._visible_self = self.buttons_enabled
        Instance.FPSController.CameraPivot.enabled_setter(not Instance.FPSController.CameraPivot.enabled)
        Instance.EditorCamera.enabled_setter(not Instance.FPSController.CameraPivot.enabled)
        Instance.EditorCamera.position_setter(Vec3(1, 2, 1) )
        InstanceMouse.locked = Instance.FPSController.CameraPivot.enabled
        InstanceMouse.position = Vec2(0,0)
        self.button3.enabled = self.buttons_enabled
        self.button4.enabled = self.buttons_enabled
        application.paused = self.buttons_enabled

        #camera.ui.enabled_setter(camera.enabled)
        #Instance.paused = Instance.time_paused  
    def button3cllick(Self):
        print("click")
     
    def HandleInput(Self, Key):
        if Key == Keys.Escape:
            Self.menu2()

