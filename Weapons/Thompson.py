from Weapon import Weapon
from BulletTypes.Bullet556Mm import Bullet556Mm
from ursina import Vec3, color, camera
from Enums.FireModes import FireModes

class Thompson(Weapon):
    
    Size = Vec3(7,7,7)
    Model = 'Models\m1a1_thompson.glb'
 
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs,
                        Magazine = 50, 
                        MaxMagazineAmmo = 50, 
                        ReserveAmmo = 200, 
                        MaxTotalAmmo = 200, 
                        AvailableFireModes=(FireModes.Safe, FireModes.Automatic), 
                        FireMode=FireModes.Safe, 
                        BulletType = Bullet556Mm, 
                        Damage= 50,
                        model = Thompson.Model, 
                        parent=camera,                         
                        position=(7,-2.2,7), 
                        rotation = (0,-90,0),
                        AimPosition =  Vec3(-3.5, 0.35,2.3 ),
                        scale=Thompson.Size, 
                        origin_z = -0.5, 
                    )