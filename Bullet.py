from ursina import Entity, Vec3, destroy as DestroyEntity, raycast as RayCast
from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock
from ursina import camera
from enemies import zombies
from Game import Instance

FrameTime = GlobalClock.getFrameTime

class Bullet(Entity):
    
    def __init__(Self, StartPosition, Speed = 350, Gravity = 9.8, BulletDropPerMeter = 0.00127, DestroyAfter = 5, Collider = 'box', **KWargs):
        
        super().__init__(**KWargs)
        
        Self.StartTime = FrameTime()
        
        Self.world_position = StartPosition
        
        Self.StartPosition = StartPosition
        
        Self.collider_setter(Collider)
        
        Self.world_rotation = camera.world_rotation
        
        Self.Forward = Self.forward
        
        Self.Speed = Speed / 100
        
        Self.Gravity = Gravity
        
        Self.BulletDropPerMeter = BulletDropPerMeter
        
        Self.DestroyAfter = Self.StartTime + DestroyAfter
    
    def UpdateRayCastPosition(Self):
        
        PassTime = FrameTime() - Self.StartTime
        
        Ray = RayCast(Self.world_position, Self.Forward, Self.Speed, ignore = (Self, ) )
        
        if Ray.hit:
            
            if type(Ray.entity).__name__ == "Zombies":

                Ray.entity.hp -= Instance.FPSController.CurrentWeapon.Damage
            
            DestroyEntity(Self)
            
            return
        
        PassTime = FrameTime() - Self.StartTime
        
        Gravity = Vec3(0, -Self.BulletDropPerMeter, 0) * Self.Gravity * PassTime * PassTime
        
        Distance = (Self.Forward * Self.Speed)
        
        Self.world_position += Gravity + Distance
            
    def Update(Self):
            
        if FrameTime() > Self.DestroyAfter:
            
            DestroyEntity(Self)
            
            return
        
        Self.UpdateRayCastPosition()