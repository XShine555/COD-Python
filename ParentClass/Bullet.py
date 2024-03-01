from ursina import Entity, Vec3
from direct.showbase.ShowBase import ShowBase

FrameTime = globalClock.getFrameTime

class Bullet(Entity):
    
    def __init__(Self, Speed, Gravity = 9.8, BulletDropPerMeter = 1, **KWargs):
        
        super().__init__(**KWargs)
        
        Self.StartPosition = Self.position
        
        Self.Forward = Vec3(0, 0, 1)
        
        Self.Speed = Speed,
        
        Self.Gravity = Gravity
        
        Self.BulletDropPerMeter = BulletDropPerMeter
        
    def ParabolicFormula(Self, Time):
        
        Point = Self.StartPosition + (Self.Forward * Self.Speed * Time)
        
        Gravity = Vec3(0, -Self.BulletDropPerMeter, 0) * Self.Gravity * Time * Time
        
        return Point + Gravity
    
    def FixedUpdate(Self):
        
        if Self.StarTime is None:
            
            Self.StartTime = FrameTime()
            
        CurrentTime = FrameTime() - Self.StartTime
        
        Parabola = Self.ParabolicFormula(CurrentTime)
        
        Self.world_position = Parabola
