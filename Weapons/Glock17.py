from Weapon import Weapon
from BulletTypes.Bullet9Mm import Bullet9Mm
from ursina import Vec3, color, camera, Entity

class Glock17(Weapon):
    
    Size = Vec3(.3,.2,1)
    Model = 'cube'
    Color = color.red
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, Magazine = 11111117, MaxMagazineAmmo = 17, ReserveAmmo = 120, MaxTotalAmmo = 120, BulletType = Bullet9Mm, model = Glock17.Model, parent=camera, position=(.5,-.25,.25), scale=Glock17.Size, origin_z = -0.5, color = Glock17.Color)
        
        Self.Muzzle = Entity(model = 'cube', scale = 0.9, visible = False, color = color.blue, parent = Self, position = Vec3(0, 0, 1.4) )