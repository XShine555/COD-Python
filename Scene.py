from ursina import Entity, destroy as Destroy
from physics3d.core import BulletRigidBodyNode

class Scene(Entity):
    
    def __init__(Self, **KWargs):
        
        super().__init__(**KWargs)
        
    def EnableScene(Self):
        
        Self.enable()
        
    def DisableScene(Self):
        
        Self.disable()
        
    def DestroyScene(Self):
        
        for Key, Value in vars(Self).items():

            if isinstance(Value, BulletRigidBodyNode):
                
                Value.Disable()

            elif isinstance(Value, Entity):

                Destroy(Value)

        Destroy(Self)