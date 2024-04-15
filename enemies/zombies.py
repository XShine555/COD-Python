from ursina import Entity

class Zombies(Entity):
    def __init__(Self, MaxHP,Damage, Speed):

        super().__init__(**KWArgs)
    
        Self.MaxHP = MaxHP
        
        Self.HP = MaxHP

        Self.Damage = Damage

        Self.Speed = Speed
    def follow(self, target):
        direction = target.position - self.position
        self.position += direction.normalized() * self.speed * time.dt

    