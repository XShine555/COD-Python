from Bullet import Bullet
from ursina import Vec3

class Bullet556Mm(Bullet):
    
    def __init__(Self, StartPosition):
        
        super().__init__(StartPosition, 1200, 9.8, 0.00127, model = "cube" )