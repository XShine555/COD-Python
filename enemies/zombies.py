from ursina import Entity, time

class Zombies(Entity):
    def __init__(Self, MaxHP,Damage, Speed, **KWArgs):

        super().__init__(**KWArgs)
    
        Self.MaxHP = MaxHP
        
        Self.HP = MaxHP

        Self.Damage = Damage

        Self.Speed = Speed
    def follow(self, target):
        direction = target.position - self.position
        self.position += direction.normalized() * self.speed * time.dt

    