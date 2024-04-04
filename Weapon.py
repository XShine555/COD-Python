from ursina import Entity, camera as InstanceCamera, Vec3, lerp as Lerp, clamp as Clamp
from Bullet import Bullet
from Enums.FireModes import FireModes
from Enums.Keys import Keys
from typing import Tuple
from Game import Instance
from direct.task.Task import Task

class Weapon(Entity):
    
    def __init__(Self, Magazine, MaxMagazineAmmo, MaxTotalAmmo, BulletType : Bullet, FireMode : FireModes = FireModes.Safe, AvailableFireModes : Tuple[FireModes] = (FireModes.Safe, FireModes.SemiAutomatic, FireModes.Burst_2, FireModes.Burst_3, FireModes.Automatic), AimPosition = Vec3(-0.25, 0, 0), **KWArgs):
        
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
        
        Self.Aimming = False
        
        Self.StartPosition = Self.position
        
        Self.StartRotation = Self.rotation
        
        Self.AimPosition = Self.StartPosition + AimPosition
        
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
        
        elif Self.FireMode is FireModes.Burst_2:
            
            for I in range(2):
                
                if not Self.LeftMouseDown:
                    
                    break
                
                Self.WeaponCooldown = True
                
                Self.SpawnBullet()
                
                await Task.pause(Self.ShootRate)
                
                Self.WeaponCooldown = False
            
        elif Self.FireMode is FireModes.Burst_3:
            
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
            
        if Key == Keys.RightMouseDown.value:
            
            Self.Aimming = not Self.Aimming
            
    def update(Self):
        
        if Self.Aimming and not Instance.FPSController.Running:
            
            Self.position = Lerp(Self.position, Self.AimPosition,  0.2)
            
            InstanceCamera.fov = Lerp(InstanceCamera.fov, 65, 0.2)
            
        else:
            
            Self.Aimming = False
            
            Self.position = Lerp(Self.position, Self.StartPosition, 0.2)
            
            InstanceCamera.fov = Lerp(InstanceCamera.fov, 80, 0.2)
            
        # Weapon Sway
            
        Self.rotation = Lerp(Self.rotation, Self.StartRotation, 0.1)
            
        XAxis = Clamp(Instance.mouse.velocity.x * 10, -65, 65)
        
        YAxis = Clamp(Instance.mouse.velocity.y * 10, -65, 65)
            
        SwayTarget = Vec3(-YAxis, -XAxis, 0)
        
        Self.rotation = Lerp(Self.rotation, Self.rotation + SwayTarget, 0.8)