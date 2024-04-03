from ursina import Entity, Vec3
from direct.showbase.ShowBaseGlobal import globalClock
from ursina import camera
from Game import Instance

FrameTime = globalClock.getFrameTime

class Bullet(Entity):
    
    def __init__(Self, StartPosition, Speed = 350.0, Gravity = 9.8, BulletDropPerMeter = 1, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.StartTime = None
        
        Self.world_position = StartPosition
        
        Self.StartPosition = StartPosition
        
        Self.world_rotation = camera.world_rotation
        
        Self.Forward = Self.forward
        
        Self.Speed = Speed,
        
        Self.Gravity = Gravity
        
        Self.BulletDropPerMeter = BulletDropPerMeter
        
    def ParabolicFormula(Self, Time):
        
        Point = Self.StartPosition + (Self.Forward * Self.Speed[0] * Time)
        
        Gravity = Vec3(0, -Self.BulletDropPerMeter, 0) * Self.Gravity * Time * Time
        
        return Point + Gravity
    
    def update(Self):
        
        if Self.StartTime is None:
            
            Self.StartTime = FrameTime()
            
        CurrentTime = FrameTime() - Self.StartTime
        
        Parabola = Self.ParabolicFormula(CurrentTime)
        
        Self.world_position = Parabola