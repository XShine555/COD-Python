from Weapon import Weapon
from BulletTypes.Bullet9Mm import Bullet9Mm
from ursina import Vec3, color, camera

class Glock17(Weapon):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, Magazine = 17, MaxMagazineAmmo = 17, ReserveAmmo = 120, MaxTotalAmmo = 120, BulletType = Bullet9Mm, model = 'cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z = -0.5, color = color.red)