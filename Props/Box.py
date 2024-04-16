from ursina import Entity, Vec3, destroy as Destroy, scene as InstanceScene, lerp as Lerp
from direct.task.Task import Task
from Enums.Keys import Keys
from Game import Instance
from random import choice as RandChoice
from importlib.util import spec_from_file_location as LoadFile, module_from_spec as ModuleToSpec

from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock

from os import walk as Cd

FrameTime = GlobalClock.getFrameTime

class Box(Entity):
    
    def __init__(Self, **KWArgs):
        
        Self.Weapons = []
        
        Self._LoadWeapons()
        
        super().__init__(**KWArgs)
        
        Self.WeaponPosition = Self.world_position +  Vec3(0, 2, 0)
        
        Self.CosmeticWeapon = None
        
        Self.GetTime = None
        
        Self.Using = False
        
        Self.CanGrab = False
        
        Self.CurrentWeapon = None
        
    def _LoadWeapons(Self):

        for Root, Dirs, Files in Cd("Weapons/"):

            for Name in Files:

                if Name.lower().endswith(".py"):

                    File = LoadFile(Name, F"Weapons/{Name}")
                    
                    Class = ModuleToSpec(File)
                    
                    File.loader.exec_module(Class)

                    WeaponToLoad = getattr(Class, Name.replace('.py', '') )
                    
                    Self.Weapons.append(WeaponToLoad)
                    
        print(Self.Weapons)
        
    def Roll(Self):
        
        Instance.taskMgr.add(Self._Roll() )
        
    async def _Roll(Self):
        
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
            
        for I in range(10):
            
            Self.CurrentWeapon = RandChoice(AvailableWeapons)
            
            Self.CosmeticWeapon.model_setter(Self.CurrentWeapon.Model)
            Self.CosmeticWeapon.color_setter(Self.CurrentWeapon.Color)
            Self.CosmeticWeapon.scale_setter(Self.CurrentWeapon.Size)
            
            await Task.pause(0.1)
            
        Self.CanGrab = True
                
    def HandleInput(Self, Key):
        
        if Key == Keys.E:
            
            if Instance.RoundManager is None or Instance.RoundManager.PlayerPoints < 950:
                
                return
            
            if not Self.Using:
                
                Self.Roll()
                
            else:
                
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