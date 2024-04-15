from Weapon import Weapon
from BulletTypes.Bullet45ACP import Bullet45ACP
from ursina import Vec3, color, camera
from Enums.FireModes import FireModes

class M1911(Weapon):
    
    Size = Vec3(.3,.2,1)
    Model = 'cube'
    Color = color.cyan
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, Magazine = 7, MaxMagazineAmmo = 7, ReserveAmmo = 30, MaxTotalAmmo = 30, AvailableFireModes=(FireModes.Safe, FireModes.SemiAutomatic), FireMode=FireModes.Safe, BulletType = Bullet45ACP, model = M1911.Model, parent=camera, position=(.5,-.25,.25), scale=M1911.Size, origin_z = -0.5, color = M1911.Color)