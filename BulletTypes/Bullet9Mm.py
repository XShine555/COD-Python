from Bullet import Bullet
from ursina import Vec3

class Bullet9Mm(Bullet):
    
    def __init__(Self, StartPosition):
        
        super().__init__(StartPosition, 350, 9.8, 1, model = "cube" )