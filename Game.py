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

from Scene import Scene
from math import floor
from PlayerController import Instance

from os import walk as Cd

import __main__

class Game(ShowBase):
    
    def __init__(Self, Title = 'COD-Python', Icon = '', Borderless = True, Fullscreen = False, Size = None, ForcedAspectRatio = None, Position = None, VSync = True, EditorUiEnabled = True, DevelopmentMode = False, RenderMode = None):

        # Init
        
        Self.ShowFPS = False
        
        Self.VSync = False
        
        ApplicationSingleton.window_type = "onscreen"
        ApplicationSingleton.base = Self
        ApplicationSingleton.development_mode = DevelopmentMode
        ApplicationSingleton.show_ursina_splash = False
        Entity._warn_if_ursina_not_instantiated = False
        
        InstanceWindow.ready(Title, Icon,
            Borderless, Fullscreen, Size, ForcedAspectRatio, Position, VSync, "onscreen",
            EditorUiEnabled, RenderMode)

        super().__init__(windowType = ApplicationSingleton.window_type)
        
        InstanceWindow.apply_settings()
        
        InstanceCamera._cam = Self.camera
        InstanceCamera._cam.reparent_to(InstanceCamera)
        InstanceCamera.render = Self.render
        InstanceCamera.position = (0, 0, -20)
        InstanceScene.camera = InstanceCamera
        InstanceCamera.set_up()
        
        Self.disableMouse()
        InstanceMouse._mouse_watcher = Self.mouseWatcherNode
        InstanceMouse.enabled = True
        Self.mouse = InstanceMouse
        
        Self.CurrentScene : Scene = None
        Self.SceneName = None
        Self.SceneDirectory = "Scenes"
        
        InstanceScene.set_up()
        
        # Physics
        
        Self.BulletWorld = BulletWorld()
        Self.Gravity = Vec3(0, 0, -9.81)
        Self.BulletWorld.setGravity(Self.Gravity)
        
        Self.taskMgr.remove("update")
        Self.taskMgr.add(Self._UpdatePipeLine, "UpdatePipeLine")
        Self.taskMgr.add(Self._UpdatePhysics, "UpdatePhysics")

        # Custom Mapping Keys

        Self.buttonThrowers[0].node().setButtonUpEvent('ButtonUp')
        Self.buttonThrowers[0].node().setButtonDownEvent('ButtonDown')
        Self.buttonThrowers[0].node().setRawButtonUpEvent('RawKeyUp')
        Self.buttonThrowers[0].node().setRawButtonDownEvent('RawKeyDown')
                    
        Self.InputNameChanges = {
            'mouse1' : 'left mouse down', 'mouse1 up' : 'left mouse up', 'mouse2' : 'middle mouse down', 'mouse2 up' : 'middle mouse up', 'mouse3' : 'right mouse down', 'mouse3 up' : 'right mouse up',
            'wheel_up' : 'scroll up', 'wheel_down' : 'scroll down',
            'arrow_left' : 'left arrow', 'arrow_left up' : 'left arrow up', 'arrow_up' : 'up arrow', 'arrow_up up' : 'up arrow up', 'arrow_down' : 'down arrow', 'arrow_down up' : 'down arrow up', 'arrow_right' : 'right arrow', 'arrow_right up' : 'right arrow up',
            'lcontrol' : 'left control', 'rcontrol' : 'right control', 'lshift' : 'left shift', 'rshift' : 'right shift', 'lalt' : 'left alt', 'ralt' : 'right alt',
            'lcontrol up' : 'left control up', 'rcontrol up' : 'right control up', 'lshift up' : 'left shift up', 'rshift up' : 'right shift up', 'lalt up' : 'left alt up', 'ralt up' : 'right alt up',
            'control-mouse1' : 'left mouse down', 'control-mouse2' : 'middle mouse down', 'control-mouse3' : 'right mouse down',
            'shift-mouse1' : 'left mouse down', 'shift-mouse2' : 'middle mouse down', 'shift-mouse3' : 'right mouse down',
            'alt-mouse1' : 'left mouse down', 'alt-mouse2' : 'middle mouse down', 'alt-mouse3' : 'right mouse down',
            'page_down' : 'page down', 'page_down up' : 'page down up', 'page_up' : 'page up', 'page_up up' : 'page up up',
        }

        Self.accept('ButtonUp', Self._ButtonUp)
        Self.accept('ButtonDown', Self._ButtonDown)
        Self.accept('RawKeyUp', Self._RawKeyUp)
        Self.accept('RawKeyDown', Self._RawKeyDown)

        Self.HeldKeys = DefaultDict(lambda: 0)

        # Whitelisted Special Keys

        Self.SpecialWhiteListKeys = {
            'mouse1' : Keys.LeftMouseDown,
            'mouse1 up' : Keys.LeftMouseUp, 
            'mouse2' : Keys.MiddleMouseDown, 
            'mouse2 up' : Keys.MiddleMouseUp, 
            'mouse3' : Keys.RightMouseDown, 
            'mouse3 up' : Keys.RightMouseUp
        }
        
        ApplicationSingleton.load_settings()
        
        ApplicationSingleton.hot_reloader = HotReloader(__main__.__file__ if hasattr(__main__, '__file__') else 'None')
        
        ApplicationSingleton.base.input = Self._ButtonDown
        
        InstanceWindow.make_editor_gui()
        InstanceWindow.editor_ui.enabled = False
        InstanceWindow.borderless = False
        
        Self._FixedTimeStep = (1/60)
        
        Self._PhysicsAccumulator = 0

        Self.FPSController = None
        Self.PlayerPoints = 0
        Self.Round = 1
        
    # Private Functions
    
    # Keys Binding Functions

    def _SanitizeKey(Self, Key):

        if Key in KeyboardKeys:

            for Prefix in (Keys.PrefixControl, Keys.PrefixAlt, Keys.PrefixShift):

                if Prefix in Key:

                    Key.replace(Prefix, '')

                    break

        if Key in Self.InputNameChanges:

            Key = Self.InputNameChanges[Key]

        return Key

    def _RawKeyUp(Self, Key):
        
        SanitizeKey = Self._SanitizeKey(Key)

        Self.HeldKeys[SanitizeKey] = 0

        if Key in Self.InputNameChanges:

            for Entity in InstanceScene.entities:
                
                if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
                if ApplicationSingleton.paused and not Entity.ignore_paused:
                    
                    continue

                if hasattr(Entity, "HandleInput"):

                    Entity.HandleInput(F"{SanitizeKey} up")

    def _RawKeyDown(Self, Key):
        
        SanitizeKey = Self._SanitizeKey(Key)

        Self.HeldKeys[SanitizeKey] = 1

        for Entity in InstanceScene.entities:
            
            if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
            if ApplicationSingleton.paused and not Entity.ignore_paused:
                    
                continue

            if hasattr(Entity, "HandleInput"):

                Entity.HandleInput(SanitizeKey)

    def _ButtonUp(Self, Key):

        if Key in Self.SpecialWhiteListKeys:

            for Entity in InstanceScene.entities:
                
                if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
                if ApplicationSingleton.paused and not Entity.ignore_paused:
                    
                    continue

                if hasattr(Entity, "HandleInput"):

                    Entity.HandleInput(Self.SpecialWhiteListKeys[F"{Key} up"] )

    def _ButtonDown(Self, Key):
        
        if Key in Self.SpecialWhiteListKeys:

            for Entity in InstanceScene.entities:
                
                if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
                if ApplicationSingleton.paused and not Entity.ignore_paused:
                    
                    continue

                if hasattr(Entity, "HandleInput"):

                    Entity.HandleInput(Self.SpecialWhiteListKeys[Key] )

            InstanceMouse.input(Self.SpecialWhiteListKeys[Key] )
                    
    # Render Update
                    
    def _UpdatePipeLine(Self, Task):

        Time.dt = GlobalClock.getDt() * ApplicationSingleton.time_scale

        Self.mouse.update()
        
        if hasattr(__main__, 'Update') and __main__.Update and not ApplicationSingleton.paused:

            __main__.Update(Time.dt)
            
        for Entity in InstanceScene.entities:
            
            if not Entity.enabled or Entity.ignore:
                
                continue

            if ApplicationSingleton.paused and not Entity.ignore_paused:
                
                continue

            if hasattr(Entity, 'Update') and callable(Entity.Update):
                
                Entity.Update(Time.dt)

            InstanceWindow.fps_counter.update()
            
        if Self.ShowFPS:
            
            Self.FPS.text = F"FPS: {floor(1//Time.dt) }"
            
        return Task.cont
    
    def _UpdatePhysics(Self, Task):
        
        if ApplicationSingleton.paused:
            
            return Task.cont
        
        Self._PhysicsAccumulator += Time.dt

        if Self._PhysicsAccumulator >= Self._FixedTimeStep:
            
            Self.BulletWorld.doPhysics(Time.dt, 10, 1.0/180.0)
            
            Self._PhysicsAccumulator -= Self._FixedTimeStep
            
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