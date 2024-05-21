from Weapon import Weapon
from BulletTypes.Bullet45ACP import Bullet45ACP
from ursina import Vec3, color, camera
from Enums.FireModes import FireModes

class M1911(Weapon):
    
    Size = Vec3(0.8,-0.7,1.2)
    Model = 'Weapons\colt_m1911.glb'
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs,
                        Magazine = 7, 
                        MaxMagazineAmmo = 7, 
                        ReserveAmmo = 30, 
                        MaxTotalAmmo = 30, 
                        AvailableFireModes=(FireModes.Safe, FireModes.SemiAutomatic), 
                        FireMode=FireModes.Safe, 
                        BulletType = Bullet45ACP, 
                        Damage= 70,
                        model = M1911.Model, 
                        rotation = (180,90,0),
                        parent=camera, 
                        AimPosition =  Vec3(-1.27, 0.15,1.1),
                        position=(2,-.60,2.5), 
                        scale=M1911.Size, 
                        origin_z = -0.5 )