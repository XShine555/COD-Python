from ursina import Entity, Vec3, destroy as DestroyEntity, raycast as Raycast, color, lerp as Lerp, distance as Distance1D
from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock
from ursina import camera
from ursina.scene import instance as InstanceScene
from Game import Instance

FrameTime = GlobalClock.getFrameTime

class Bullet(Entity):
    
    def __init__(Self, StartPosition, Speed = 350, Gravity = 9.8, BulletDropPerMeter = 1, DestroyAfter = 5, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.StartTime = FrameTime()
        
        Self.world_position = StartPosition
        
        Self.StartPosition = StartPosition
        
        Self.world_rotation = camera.world_rotation
        
        Self.Forward = Self.forward
        
        Self._Speed = Speed,
        
        Self.Speed = Self._Speed[0]
        
        Self.Gravity = Gravity
        
        Self.BulletDropPerMeter = BulletDropPerMeter
        
        Self.DestroyAfter = Self.StartTime + DestroyAfter
        
        Self.LastPoint = Self.world_position
        
    def ParabolicFormula(Self, Time):
        
        Point = Self.StartPosition + (Self.Forward * Self.Speed * Time)
        
        Gravity = Vec3(0, -Self.BulletDropPerMeter, 0) * Self.Gravity * Time * Time
        
        return Point + Gravity
    
    def Update(Self, DeltaTime):
            
        if FrameTime() > Self.DestroyAfter:
            
            DestroyEntity(Self)
            
            return
        
        CurrentTime = FrameTime() - Self.StartTime
        
        Parabola = Self.ParabolicFormula(CurrentTime)
        
        Calc = Distance1D(Self.LastPoint, Parabola)
        
        Hit = Raycast(Parabola, Self.Forward, Calc, ignore = (Self, Instance.FPSController) )
        
        if Hit.entity:
            
            DestroyEntity(Self)
            
            return
        
        Self.world_position = Parabola
        
        Self.LastPoint = Self.world_position