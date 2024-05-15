from Weapon import Weapon
from BulletTypes.Bullet556Mm import Bullet556Mm
from ursina import Vec3, color, camera

class M4A1(Weapon):
    
    Size = Vec3(0.3, 0.3, 0.3)
    Model = 'Models/m4a1.glb'
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, 
                        Magazine = 30, 
                        MaxMagazineAmmo = 30, 
                        ReserveAmmo = 120, 
                        MaxTotalAmmo = 120, 
                        BulletType = Bullet556Mm, 
                        Damage= 50,
                        model = M4A1.Model, 
                        parent=camera, 
                        position=(.5,-.25, 0.75), 
                        rotation=(0, -90, 0),
                        AimPosition =  Vec3(-0.35, 0.02, 0),
                        scale=M4A1.Size, 
                        origin_z = -0.5
                    )