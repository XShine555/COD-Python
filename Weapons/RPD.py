from Weapon import Weapon
from BulletTypes.Bullet762Mm import Bullet762Mm
from ursina import Vec3, color, camera
from Enums.FireModes import FireModes

class RPD(Weapon):
    
    Size = Vec3(.3,.2,1)
    Model = 'Models\minigun_animated.glb'

    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, Magazine = 100, 
                        MaxMagazineAmmo = 100, 
                        ReserveAmmo = 475, 
                        MaxTotalAmmo = 475, 
                        AvailableFireModes=(FireModes.Automatic,), 
                        FireMode=FireModes.Automatic, 
                        BulletType = Bullet762Mm, 
                        model = RPD.Model,
                        Damage = 40,
                        parent=camera, 
                        position=(.5,-.25,.25), 
                        scale=RPD.Size, 
                        origin_z = -0.5)