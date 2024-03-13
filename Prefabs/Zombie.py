from ursina import Entity, Vec3, time
from ursina import distance_xz as DistanceVec3
from physics3d.character_controller import CharacterController
from MultiplayerHandler.Client import Instance

class Zombie(Entity):
    
    def __init__(Self, World, **KWArgs):
        
        super().__init__(**KWArgs)
        
        # Physics And Character Controller.

        Self.Controller = CharacterController(World, Self)

        Self.Velocity = 10
        
    def GoForPlayer(Self, Players : Entity):
        
        ClosestDistance = float('inf')
        
        FEntity : Entity = None
        
        for X in Players:
            
            print(X)
            
            Dist = DistanceVec3(X.world_position, Self.world_position)
            
            if Dist < ClosestDistance:
                
                ClosestDistance = Dist
                
                FEntity = X
                
        Self.look_at_2d(FEntity.world_position, 'y')
        
        if ClosestDistance > 2:
        
            Self.Controller.setLinearMovement(Self.forward * Self.Velocity, True)
            
        else:
            
            Self.Controller.setLinearMovement(Vec3.zero, True)
            
    def update(Self):
        
        if Instance is None:
            
            return
        
        Self.GoForPlayer(Instance.Players.values() )