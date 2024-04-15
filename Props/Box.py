from ursina import Entity, Vec3, destroy as Destroy, curve as Curve, scene as InstanceScene, lerp as Lerp
from direct.task.Task import Task
from Enums.Keys import Keys
from Game import Instance
from random import choice as RandChoice

from Weapons.Glock17 import Glock17
from Weapons.M4A1 import M4A1
from Weapons.Intervention import Intervention

from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock

FrameTime = GlobalClock.getFrameTime

class Box(Entity):
    
    def __init__(Self, **KWArgs):
        
        Self.Weapons = (
            Glock17,
            M4A1,
            Intervention
        )
        
        super().__init__(**KWArgs)
        
        Self.WeaponPosition = Self.world_position +  Vec3(0, 2, 0)
        
        Self.CosmeticWeapon = None
        
        Self.GetTime = None
        
        Self.Using = False
        
        Self.CanGrab = False
        
        Self.CurrentWeapon = None
        
    def Roll(Self):
        
        Instance.taskMgr.add(Self._Roll() )
        
    async def _Roll(Self):
        
        Self.CosmeticWeapon = Entity(parent = Self, model = 'cube')
        Self.CosmeticWeapon.world_parent_setter(InstanceScene)
        
        Self.GetTime = FrameTime()
        
        Self.Using = True
        
        for I in range(12):
            
            Self.CurrentWeapon = RandChoice(Self.Weapons)
            
            while Instance.FPSController.HasWeapon(Self.CurrentWeapon):
                
                Self.CurrentWeapon = RandChoice(Self.Weapons)
            
            Self.CosmeticWeapon.model_setter(Self.CurrentWeapon.Model)
            Self.CosmeticWeapon.color_setter(Self.CurrentWeapon.Color)
            Self.CosmeticWeapon.scale_setter(Self.CurrentWeapon.Size)
            
            await Task.pause(0.1)
            
        Self.CanGrab = True
                
    def HandleInput(Self, Key):
        
        if Key == Keys.E:
            
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
        
        if Self.CosmeticWeapon.world_position.y > Self.WeaponPosition.y:
            
            return
        
        Self.CosmeticWeapon.world_position = Lerp(Self.CosmeticWeapon.world_position, Self.CosmeticWeapon.world_position + Vec3(0, 0.1, 0), 0.6)