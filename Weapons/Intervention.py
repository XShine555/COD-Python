from Weapon import Weapon
from BulletTypes.Bullet556Mm import Bullet556Mm
from ursina import Vec3, color, camera
from Enums.FireModes import FireModes

class Intervention(Weapon):
    
    Size = Vec3(.3,.2,1)
    Model = 'cube'
    Color = color.rgb(128, 0, 128)
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, Magazine = 5, AvailableFireModes=(FireModes.Safe, FireModes.SemiAutomatic), MaxMagazineAmmo = 5, ReserveAmmo = 30, MaxTotalAmmo = 30, BulletType = Bullet556Mm, model = Intervention.Model, parent=camera, position=(.5,-.25,.25), scale=Intervention.Size, origin_z = -0.5, color = Intervention.Color)