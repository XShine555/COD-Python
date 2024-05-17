from Weapon import Weapon
from BulletTypes.Bullet9Mm import Bullet9Mm
from ursina import Vec3, color, camera, Entity, load_model as LoadModel

class Glock17(Weapon):
    
    Size = Vec3(3, 3, 3)
    Model = 'Models/g18.glb'
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs, Magazine = 11111117, MaxMagazineAmmo = 17, AimPosition = Vec3(-0.4, 0.13, 0), ReserveAmmo = 120, MaxTotalAmmo = 120, BulletType = Bullet9Mm, model = Glock17.Model, parent=camera, position=(0.4, -0.35, 2.5), rotation=(0, 180, 0), scale=Glock17.Size, origin_z = -0.5)
        
        Self.Muzzle = Entity(model = 'cube', scale = 0.9, visible = False, color = color.blue, parent = Self, position = Vec3(0, 0, 1.4) )