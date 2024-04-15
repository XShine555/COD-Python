from Weapon import Weapon
from BulletTypes.Bullet556Mm import Bullet556Mm
from ursina import Vec3, color, camera

class M4A1(Weapon):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, Magazine = 30, MaxMagazineAmmo = 30, ReserveAmmo = 120, MaxTotalAmmo = 120, BulletType = Bullet556Mm, model = 'cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z = -0.5, color = color.blue)