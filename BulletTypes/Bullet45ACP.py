from Bullet import Bullet
from ursina import Vec3

class Bullet45ACP(Bullet):
    
    def __init__(Self, StartPosition):
        
        super().__init__(StartPosition, 1150, 9.8, 0.00127, model = "cube" )