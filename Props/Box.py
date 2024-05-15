from ursina import Entity, Vec3, destroy as Destroy, scene as InstanceScene, lerp as Lerp, color
from direct.task.Task import Task
from Enums.Keys import Keys
from Game import Instance
from random import choice as RandChoice
from importlib.util import spec_from_file_location as LoadFile, module_from_spec as ModuleToSpec

from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock

from os import walk as Cd

FrameTime = GlobalClock.getFrameTime

class Box(Entity):
    
    def __init__(Self, Offset = Vec3(1.85, 0, -1), **KWArgs):
        
        Self.Weapons = []
        
        Self._LoadWeapons()
        
        super().__init__(**KWArgs)
        
        Self.WeaponPosition = Offset
        
        Self.CosmeticWeapon = None
        
        Self.GetTime = None
        
        Self.Using = False
        
        Self.CanGrab = False
        
        Self.CurrentWeapon = None
        
        Self.color = color.black

        Self.Cost = 950

    def _LoadWeapons(Self):

        for Root, Dirs, Files in Cd("Weapons/"):

            for Name in Files:

                if Name.lower().endswith(".py"):

                    File = LoadFile(Name, F"Weapons/{Name}")
                    
                    Class = ModuleToSpec(File)
                    
                    File.loader.exec_module(Class)

                    WeaponToLoad = getattr(Class, Name.replace('.py', '') )
                    
                    Self.Weapons.append(WeaponToLoad)
        
    def Roll(Self):
        
        Instance.taskMgr.add(Self._Roll() )
        
    async def _Roll(Self):
        Instance.FPSController.Points -= Self.Cost
        Self.CosmeticWeapon = Entity(parent = Self, model = 'cube')
        Self.CosmeticWeapon.world_parent_setter(InstanceScene)
        
        Self.GetTime = FrameTime()
        
        Self.Using = True
        
        Self.CanGrab = False


        AvailableWeapons= []
        
        print(Instance.FPSController.Weapons[0].__class__, Self.Weapons[0])
        
        for Item in Self.Weapons:
            
            if Item.__name__ not in [type(weapon).__name__ for weapon in Instance.FPSController.Weapons]:
                
                AvailableWeapons.append(Item)
                
        Self.CosmeticWeapon.world_position = Self.world_position + Self.WeaponPosition
            
        for I in range(14):
            
            Self.CurrentWeapon = RandChoice(AvailableWeapons)
            
            Self.CosmeticWeapon.model_setter(Self.CurrentWeapon.Model)
            Self.CosmeticWeapon.scale_setter(Self.CurrentWeapon.Size)
            Self.CosmeticWeapon.rotation_setter(Self.world_rotation + Vec3(0, 90, 0) )
            
            await Task.pause(0.1)
            
        Self.CanGrab = True
                
    def HandleInput(Self, Key):
        
        if Key == Keys.E:
        
            if not Self.Using and Instance.FPSController.Points >= Self.Cost:
                
                Self.Roll()
                
            elif Self.Using:
                
                if Self.CanGrab:
                    
                    Instance.FPSController.GiveWeapon(Self.CurrentWeapon)
                    
                    Destroy(Self.CosmeticWeapon)
                    
                    Self.CosmeticWeapon = None 
                    
                    Self.CurrentWeapon = None
                    
                    Self.Using = False
            
    def Update(Self):
        
        if Self.CosmeticWeapon is None:
            
            return
        
        if FrameTime() > Self.GetTime + 7:
            
            Destroy(Self.CosmeticWeapon)
            
            Self.CosmeticWeapon = None
            
            Self.CurrentWeapon = None
            
            Self.Using = False
            
            Self.GetTime = None
            
            return
        
        if Self.CanGrab:
            
            return
        
        Self.CosmeticWeapon.world_position = Lerp(Self.CosmeticWeapon.world_position, Self.CosmeticWeapon.world_position + Vec3(0, 0.1, 0), 0.3)