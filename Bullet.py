from ursina import Entity, Vec3, destroy as DestroyEntity
from direct.showbase.ShowBaseGlobal import globalClock as GlobalClock
from ursina import camera
from Game import Instance

FrameTime = GlobalClock.getFrameTime

class Bullet(Entity):
    
    def __init__(Self, StartPosition, Speed = 350.0, Gravity = 9.8, BulletDropPerMeter = 1, DestroyAfter = 5, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.StartTime = FrameTime()
        
        Self.world_position = StartPosition
        
        Self.StartPosition = StartPosition
        
        Self.world_rotation = camera.world_rotation
        
        Self.Forward = Self.forward
        
        Self.Speed = Speed,
        
        Self.Gravity = Gravity
        
        Self.BulletDropPerMeter = BulletDropPerMeter
        
        Self.DestroyAfter = Self.StartTime + DestroyAfter
        
    def ParabolicFormula(Self, Time):
        
        Point = Self.StartPosition + (Self.Forward * Self.Speed[0] * Time)
        
        Gravity = Vec3(0, -Self.BulletDropPerMeter, 0) * Self.Gravity * Time * Time
        
        return Point + Gravity
    
    def update(Self):
            
        if FrameTime() > Self.DestroyAfter:
            
            DestroyEntity(Self)
            
            return
            
        CurrentTime = FrameTime() - Self.StartTime
        
        Parabola = Self.ParabolicFormula(CurrentTime)
        
        Self.world_position = Parabola