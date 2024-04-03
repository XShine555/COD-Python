from ursina import Entity, held_keys as HeldKeys, camera as InstanceCamera, invoke as Invoke, time as Time
from time import sleep as Sleep
from Bullet import Bullet
from Enums.FireModes import FireModes
from Enums.Keys import Keys
from typing import Tuple
from Game import Instance
from direct.task.Task import Task

class Weapon(Entity):
    
    def __init__(Self, Magazine, MaxMagazineAmmo, MaxTotalAmmo, BulletType : Bullet, FireMode : FireModes = FireModes.Safe, AvailableFireModes : Tuple[FireModes] = (FireModes.Safe, FireModes.SemiAutomatic, FireModes.Burst, FireModes.Automatic), **KWArgs):
        
        super().__init__(**KWArgs)
        
        Self.Magazine = Magazine
        
        Self.MaxMagazineAmmo = MaxMagazineAmmo
        
        Self.MaxTotalAmmo = MaxTotalAmmo
        
        Self.BulletType = BulletType
        
        Self.parent = InstanceCamera
        
        Self.FireMode : FireModes = FireMode
        
        Self.AvailableFireModes : Tuple[FireModes] = AvailableFireModes
        
        Self.LeftMouseDown = False
        
        Self.IsShooting = False
        
        Self.ShootRate = (60 / 750)
        
        Self.WeaponCooldown = False
        
    def CycleFireMode(Self):
        
        Index = Self.AvailableFireModes.index(Self.FireMode) + 1
        
        if Index >= len(Self.AvailableFireModes):
            
            Index = 0
         
        Self.FireMode = Self.AvailableFireModes[Index]
        
        print(Self.FireMode)
        
    def SpawnBullet(Self):
        
        Self.BulletType(StartPosition = Self.world_position)
        
    async def Shoot(Self):
        
        if Self.Magazine < 1:
            
            return
        
        if Self.FireMode is FireModes.Safe:
            
            return
        
        Self.WeaponCooldown = True
        
        if Self.FireMode is FireModes.SemiAutomatic:
            
            Self.SpawnBullet()
        
            await Task.pause(Self.ShootRate)
            
            Self.WeaponCooldown = False
            
        elif Self.FireMode is FireModes.Burst:
            
            for I in range(3):
                
                if not Self.LeftMouseDown:
                    
                    break
                
                Self.WeaponCooldown = True
                
                Self.SpawnBullet()
                
                await Task.pause(Self.ShootRate)
                
                Self.WeaponCooldown = False
                
        elif Self.FireMode is FireModes.Automatic:
            
            while Self.LeftMouseDown:
            
                Self.WeaponCooldown = True
                
                Self.SpawnBullet()
                
                await Task.pause(Self.ShootRate)
                
                Self.WeaponCooldown = False
        
    def input(Self, Key):
        
        if Key == Keys.V.value:
            
            Self.CycleFireMode()
        
        if Key == Keys.LeftMouseDown.value:
        
            Self.LeftMouseDown = True
            
            Instance.taskMgr.add(Self.Shoot() )
            
        if Key == Keys.LeftMouseUp.value:
            
            Self.LeftMouseDown = False