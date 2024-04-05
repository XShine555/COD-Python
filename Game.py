from ursina import Ursina, Vec3, time as Time, application as ApplicationInstance
from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock
from ursina.main import keyboard_keys as KeyboardKeys
from ursina.scene import instance as SceneInstance
from Scene import Scene
from importlib.util import spec_from_file_location as LoadFile, module_from_spec as ModuleToSpec
from panda3d.bullet import BulletWorld
from Enums.Keys import Keys
from collections import defaultdict as DefaultDict
from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock
from direct.showbase.ShowBaseGlobal import ClockObject
import __main__

from physics3d import Debugger

class Game(Ursina):
    
    def __init__(Self, **KWargs):

        super().__init__(**KWargs)
        
        Self.CurrentScene : Scene = None
        
        Self.SceneName = None
        
        Self.SceneDirectory = "Scenes"
        
        # Physics
        
        Self.BulletWorld = BulletWorld()
        
        Debugger(Self.BulletWorld, wireframe=True)
        
        Self.Gravity = Vec3(0, -9.81, 0)
        
        Self.BulletWorld.setGravity(Self.Gravity)
        
        Self.taskMgr.remove("update")
        
        Self.taskMgr.add(Self._UpdatePipeLine, "UpdatePipeLine")
        
        Self.taskMgr.add(Self._PhysicsPipeLine, "PipeLineRender")
        
        Self.FixedTimeStep = 1.0 / 60.0
        
        Self.PhysicsAccumulator = 0

        # Custom Mapping Keys
        
        for Mode in ('buttonDown', 'buttonUp', 'buttonHold', 'keystroke'):

            Self.ignore(Mode)

        Self.buttonThrowers[0].node().setButtonUpEvent('ButtonUp')

        Self.buttonThrowers[0].node().setButtonDownEvent('ButtonDown')

        Self.buttonThrowers[0].node().setRawButtonUpEvent('RawKeyUp')

        Self.buttonThrowers[0].node().setRawButtonDownEvent('RawKeyDown')

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

    # Private Functions
    
    # Keys Binding Functions

    def _SanitizeKey(Self, Key):

        if Key in KeyboardKeys:

            for Prefix in (Keys.PrefixControl, Keys.PrefixAlt, Keys.PrefixShift):

                if Prefix in Key:

                    Key.replace(Prefix, '')

                    break

        if Key in Self._input_name_changes:

            Key = Self._input_name_changes[Key]

        return Key

    def _RawKeyUp(Self, Key):
        
        SanitizeKey = Self._SanitizeKey(Key)

        Self.HeldKeys[SanitizeKey] = 0

        if Key in Self._input_name_changes:

            for Entity in SceneInstance.entities:
                
                if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
                if ApplicationInstance.paused and not Entity.ignore_paused:
                    
                    continue

                if hasattr(Entity, "HandleInput"):

                    Entity.HandleInput(F"{SanitizeKey} up")

    def _RawKeyDown(Self, Key):
        
        SanitizeKey = Self._SanitizeKey(Key)

        Self.HeldKeys[SanitizeKey] = 1

        for Entity in SceneInstance.entities:
            
            if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
            if ApplicationInstance.paused and not Entity.ignore_paused:
                    
                continue

            if hasattr(Entity, "HandleInput"):

                Entity.HandleInput(SanitizeKey)

    def _ButtonUp(Self, Key):

        if Key in Self.SpecialWhiteListKeys:

            for Entity in SceneInstance.entities:
                
                if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
                if ApplicationInstance.paused and not Entity.ignore_paused:
                    
                    continue

                if hasattr(Entity, "HandleInput"):

                    Entity.HandleInput(Self.SpecialWhiteListKeys[F"{Key} up"] )

    def _ButtonDown(Self, Key):
        
        if Key in Self.SpecialWhiteListKeys:

            for Entity in SceneInstance.entities:
                
                if not Entity.enabled or Entity.ignore or Entity.ignore_input:
                    
                    continue
                
                if ApplicationInstance.paused and not Entity.ignore_paused:
                    
                    continue

                if hasattr(Entity, "HandleInput"):

                    Entity.HandleInput(Self.SpecialWhiteListKeys[Key] )
                    
    # Physics Update

    def _PhysicsPipeLine(Self, Task):
        
        Self.PhysicsAccumulator += Time.dt
        
        while Self.PhysicsAccumulator >= Self.FixedTimeStep:
            
            Self.BulletWorld.doPhysics(Self.FixedTimeStep, 10)
            
            Self.PhysicsAccumulator -= Self.FixedTimeStep
            
            for Entity in SceneInstance.entities:
                
                 if hasattr(Entity, "PhysicsUpdate"):
                     
                    Entity.PhysicsUpdate()
                    
            return Task.cont
                    
    def _UpdatePipeLine(Self, Task):
            
        Time.dt = GlobalClock.getDt() * ApplicationInstance.time_scale
        
        Self.mouse.update()
        
        if hasattr(__main__, 'Update') and __main__.Update and not ApplicationInstance.paused:

            __main__.Update(Time.dt)
            
        for Entity in SceneInstance.entities:
            
            if not Entity.enabled or Entity.ignore:
                
                continue

            if ApplicationInstance.paused and not Entity.ignore_paused:
                
                continue

            if hasattr(Entity, 'Update') and callable(Entity.Update):
                
                Entity.Update(Time.dt)
            
        return Task.cont

    # Public Functions
        
    def LoadScene(Self, Name):
        
        try:
            
            if Self.CurrentScene is not None:
                
                pass
                
                #Self.CurrentScene.DestroyScene()
            
            File = LoadFile(Name, F"{Self.SceneDirectory}/{Name}.py")
            
            File_Class = ModuleToSpec(File)
            
            File.loader.exec_module(File_Class)
            
            Scene_Class = getattr(File_Class, Name)
            
            Self.CurrentScene = Scene_Class()
            
            Self.SceneName = Name
            
            Self.CurrentScene.EnableScene()
            
        except FileNotFoundError:
            
            print("File Not Found")
        
    def SetGravity(Self, Gravity):
        
        Self.Gravity = Gravity
        
        Self.BulletWorld.setGravity(Self.Gravity)

    def LimitFPS(Self, Limit):

        GlobalClock.setMode(ClockObject.MLimited)

        GlobalClock.setFrameRate(Limit)

    def UnLimitFPS(Self):

        GlobalClock.setMode(ClockObject.MNormal)
        
Instance = Game()