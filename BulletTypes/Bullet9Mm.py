from Bullet import Bullet
from ursina import Vec3

class Bullet9Mm(Bullet):
    
    def __init__(Self, StartPosition):
        
        super().__init__(StartPosition, Speed = 965, Gravity = 9.8, BulletDropPerMeter = 0.00127, model = "cube", scale = Vec3(0.1, 0.1, 0.1) )