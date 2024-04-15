from collections import defaultdict as DefaultDict
from panda3d.bullet import BulletWorld
from panda3d.core import WindowProperties
from Enums.Keys import Keys
from importlib.util import spec_from_file_location as LoadFile, module_from_spec as ModuleToSpec

from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock, ClockObject
from direct.showbase.ShowBase import ShowBase
from ursina.prefabs.hot_reloader import HotReloader

from ursina import application as ApplicationSingleton, Vec3, Vec2, time as Time, Text, entity as Entity
from ursina.window import instance as InstanceWindow
from ursina.camera import instance as InstanceCamera
from ursina.mouse import instance as InstanceMouse
from ursina.scene import instance as InstanceScene

from ursina.main import keyboard_keys as KeyboardKeys

from KeyMapper import KeyMapper

from Scene import Scene
from math import floor
from os import walk as Cd

import __main__

class Game(ShowBase):
    
    def __init__(Self, Title = 'COD-Python', Icon = '', WindowType = "OnScreen", Borderless = False, Fullscreen = False, Size = None, ForcedAspectRatio = None, Position = None, VSync = True, EditorUiEnabled = True, DevelopmentMode = False, RenderMode = None):

        # Game States
        
        Self.ShowFPS = False
        
        Self.VSync = False

        Self.WindowType = WindowType.lower()

        # Application / Window Instance

        ApplicationSingleton.window_type = Self.WindowType
        
        ApplicationSingleton.base = Self
        
        ApplicationSingleton.development_mode = DevelopmentMode
        
        ApplicationSingleton.show_ursina_splash = False
        
        Entity._warn_if_ursina_not_instantiated = False
        
        InstanceWindow.ready(Title, Icon, Borderless, Fullscreen, Size, ForcedAspectRatio, Position, VSync, Self.WindowType, EditorUiEnabled, RenderMode)

        # Initialize ShowBase
        
        super().__init__(True, Self.WindowType)
        
        # Camera Instance

        InstanceWindow.apply_settings()
        
        InstanceCamera._cam = Self.camera
        
        InstanceCamera._cam.reparent_to(InstanceCamera)
        
        InstanceCamera.render = Self.render
        
        InstanceCamera.position = (0, 0, -20)
        
        InstanceScene.camera = InstanceCamera
        
        InstanceCamera.set_up()
        
        # Mouse Instance
        
        Self.disableMouse()
        
        InstanceMouse._mouse_watcher = Self.mouseWatcherNode
        
        InstanceMouse.enabled = True
        
        Self.mouse = InstanceMouse

        # Physics
        
        Self.BulletWorld = BulletWorld()
        
        Self.Gravity = Vec3(0, 0, -9.81)
        
        Self.BulletWorld.setGravity(Self.Gravity)

        # Render Pipe Line

        Self.taskMgr.add(Self._UpdatePipeLine, "UpdatePipeLine")
        
        Self.taskMgr.add(Self._UpdatePhysics, "UpdatePhysics")

        # Key Detection And Mapper

        Self.KeyMapper = KeyMapper()
        
        Self.buttonThrowers[0].node().setButtonUpEvent('ButtonUp')

        Self.buttonThrowers[0].node().setButtonDownEvent('ButtonDown')
        
        Self.buttonThrowers[0].node().setRawButtonUpEvent('RawKeyUp')

        Self.buttonThrowers[0].node().setRawButtonDownEvent('RawKeyDown')

        Self.accept('ButtonUp', Self._ButtonUp)

        Self.accept('ButtonDown', Self._ButtonDown)

        Self.accept('RawKeyUp', Self._RawKeyUp)

        Self.accept('RawKeyDown', Self._RawKeyDown)

        Self.HeldKeys = DefaultDict(lambda: 0)

        # Scene

        Self.CurrentScene : Scene = None
        
        Self.SceneName = None
        
        Self.SceneDirectory = "Scenes"

        InstanceScene.set_up()
        
        ApplicationSingleton.load_settings()
        
        ApplicationSingleton.hot_reloader = HotReloader(__main__.__file__ if hasattr(__main__, '__file__') else 'None')
        
        ApplicationSingleton.base.input = Self._ButtonDown
        
        InstanceWindow.make_editor_gui()
        
        InstanceWindow.editor_ui.enabled = False

        InstanceWindow.borderless = Borderless


    # Private Functions

    def _SearchAndCall(Self, Attribute, Call = None):

        for Entity in InstanceScene.entities:
                
            if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                continue
                
            if ApplicationSingleton.paused and not Entity.ignore_paused:
                    
                continue

            if hasattr(Entity, Attribute):

                Method = getattr(Entity, Attribute)

                if Call is None:

                    Method()

                else:

                    Method(Call)

    def _ClearKey(Self, Key):

        if Key in KeyboardKeys:

            for Prefix in (Keys.PrefixControl, Keys.PrefixAlt, Keys.PrefixShift):

                if Prefix in Key:

                    Key.replace(Prefix, '')

                    break

        if Key in Keys.InputNameChanges:

            Key = Keys.InputNameChanges[Key]

        return Key

    def _RawKeyUp(Self, Key):
        
        Key = Self._ClearKey(Key)

        Self.HeldKeys[Key] = 0

        if Key in Keys.InputNameChanges:

            Key = Keys.SpecialWhiteListKeys[Key]

        Self._SearchAndCall("HandleInput", F"{Key} up")

    def _RawKeyDown(Self, Key):
        
        Key = Self._ClearKey(Key)

        Self.HeldKeys[Key] = 1

        if Key in Keys.InputNameChanges:

            Key = Keys.SpecialWhiteListKeys[Key]

        Self._SearchAndCall("HandleInput", Key)

    def _ButtonUp(Self, Key):

        if Key in Keys.SpecialWhiteListKeys:

            Key = Keys.SpecialWhiteListKeys[Key]

            Self._SearchAndCall("HandleInput", F"{Key} up")

    def _ButtonDown(Self, Key):
        
        if Key in Keys.SpecialWhiteListKeys:

            Key = Keys.SpecialWhiteListKeys[Key]

            Self._SearchAndCall("HandleInput", Key)

            InstanceMouse.input(Key)
                    
    def _UpdatePipeLine(Self, Task):

        Time.dt = GlobalClock.getDt() * ApplicationSingleton.time_scale

        Self.mouse.update()
        
        if hasattr(__main__, 'Update') and __main__.Update and not ApplicationSingleton.paused:

            __main__.Update(Time.dt)
            
        Self._SearchAndCall("Update")
            
        return Task.cont
    
    def _UpdatePhysics(Self, Task):
        
        if ApplicationSingleton.paused:
            
            return Task.cont
        
        Self.BulletWorld.doPhysics(Time.dt, 10, 1.0/360.0)

        return Task.cont

    # Public Functions
        
    def GetScenes(Self):

        AvailableScenes = []

        for Root, Dirs, Files in Cd(Self.SceneDirectory):

            for File in Files:

                if File.lower().endswith(".py"):

                    AvailableScenes.append(File)

        return AvailableScenes

    def LoadSceneSafely(Self, Name):

        SceneToLoad = None

        try:

            File = LoadFile(Name, F"{Self.SceneDirectory}/{Name}.py")

            Class = ModuleToSpec(File)
            
            File.loader.exec_module(Class)

            SceneToLoad = getattr(Class, Name)
        
        except FileNotFoundError:

            print("File Not Found")

            return False
        
        if Self.CurrentScene is not None:
                
            Self.CurrentScene.DestroyScene()

        Self.CurrentScene = SceneToLoad()

        Self.SceneName = Name

        Self.CurrentScene.EnableScene()

        return True

    def SetGravity(Self, Gravity):
        
        Self.Gravity = Gravity
        
        Self.BulletWorld.setGravity(Self.Gravity)
        
    def EnableShowFPS(Self):
        
        if Self.ShowFPS:
            
            return
        
        Self.FPS = Text(origin = Vec2(-9, -19) )
        
        Self.ShowFPS = True
        
    def DisableShowFPS(Self):
        
        Self.FPS = None
        
        Self.ShowFPS = False
        
    def Run(Self):

        super().run()

    def Fullscreen(Self):

        InstanceWindow.borderless = False

    def Borderless(Self):

        InstanceWindow.borderless = True

    def Windowed(Self):

        InstanceWindow.borderless = False
        
    def ActivateVSync(Self):
        
        Self.VSync = True
        
        GlobalClock.set_mode(ClockObject.MLimited)
        
    def DisableVSync(Self):
        
        Self.VSync = False
        
        GlobalClock.set_mode(ClockObject.MNormal)
        
    def LimitFPS(Self, Value):
        
        if Self.VSync:
            
            return
        
        GlobalClock.set_mode(ClockObject.MIntegerLimited)
        
        GlobalClock.set_dt( (1/Value) )
        
    def UnLimitFPS(Self):
        
        if Self.VSync:
            
            return

        GlobalClock.set_mode(ClockObject.MNormal)
        
    def ShowMouse(Self, Value):
        
        Window = WindowProperties()
        
        Window.setCursorHidden(Value)
        
        ApplicationSingleton.base.win.requestProperties(Window)
        
    def LockMouse(Self, Value):
        
        InstanceMouse._locked = Value
        
        InstanceMouse.position = Vec2(0, 0)

Instance = Game()