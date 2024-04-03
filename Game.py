from ursina import Ursina, Vec3
from ursina import time as Time
from Scene import Scene
from importlib.util import spec_from_file_location as LoadFile, module_from_spec as ModuleToSpec
from panda3d.bullet import BulletWorld

class Game(Ursina):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.CurrentScene : Scene = None
        
        Self.SceneName = None
        
        Self.SceneDirectory = "Scenes"
        
        # Physics
        
        Self.BulletWorld = BulletWorld()
        
        Self.Gravity = Vec3(0, -9.81, 0)
        
        Self.BulletWorld.setGravity(Self.Gravity)
        
        Self.taskMgr.add(Self.PipeLineRender, "PipeLineRender")
        
        Self.FixedTimeStep = 1.0 / 60.0
        
        Self.PhysicsAccumulator = 0
        
    def LoadScene(Self, Name):
        
        try:
            
            if Self.CurrentScene is not None:
                
                Self.CurrentScene.DestroyScene()
            
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
        
    def PipeLineRender(Self, Task):
        
        Self.PhysicsAccumulator += Time.dt
        
        while Self.PhysicsAccumulator >= Self.FixedTimeStep:
            
            Self.BulletWorld.doPhysics(Self.FixedTimeStep, 10)
            
            Self.PhysicsAccumulator -= Self.FixedTimeStep
        
        return Task.cont
        
Instance = Game()