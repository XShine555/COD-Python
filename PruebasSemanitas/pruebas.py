from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

from Enemigos import Enemies

class Weapon(Entity):
    def __init__(self, name, maxAmmo,model,parent,position,scale,origin_z,color):
        super().__init__()
        self.name = name
        self.maxAmmo = maxAmmo
        self.ammo = maxAmmo
        self.model = model
        self.parent = parent
        self.position = position
        self.scale = scale
        self.origin_z = origin_z
        self.color = color
        self.reloading = False
        self.cooldown = False
        self.display_text = Text(parent= self, text=f'Ammo: {self.ammo}/{self.maxAmmo}', y=-0.3, origin=(0, 0), background=True)


    def shoot(self):
        self.display_text.disable = False
        self.cooldown = True
        self.muzzle_flash.enabled = True   
        self.ammo -= 1
        invoke(self.muzzle_flash.disable, delay=.05)
        invoke(setattr,self,'cooldown', False, delay=.05)
        print(self.ammo)
        if self.ammo == 0:
            self.reload()

    def reload(self):
        if self.ammo < self.maxAmmo:
            self.reloading = True

    def makeReload(self):
        if self.ammo>= self.maxAmmo:
            self.reloading = False
            return
        self.ammo += 1 
        print(self.ammo)
        self.display_text.text = f'Ammo: {self.ammo}/{self.maxAmmo}'


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.weapons = []
        self.current_weapon_index = 0
        self.current_weapon = pistol
    def switch_weapon(self):
        self.current_weapon.visible_setter(False)
        self.current_weapon_index = (self.current_weapon_index + 1) % len(self.weapons)
        self.current_weapon = self.weapons[self.current_weapon_index]
        self.current_weapon.visible_setter(True)

    def añadir_arma(self, arma):
        self.weapons.append(arma)
    
    def input(self,key):
        if key == "r" and not self.current_weapon.cooldown:
            self.current_weapon.reload() 
        if key == 'q'and not _player.current_weapon.cooldown and not self.current_weapon.reloading:
            self.switch_weapon()

    def update(self):
        if held_keys["left mouse"] and not self.current_weapon.cooldown and not self.current_weapon.reloading:
            self.current_weapon.shoot()

        if self.current_weapon.reloading and not self.current_weapon.cooldown:
            self.current_weapon.cooldown = True
            invoke(setattr, self.current_weapon, 'cooldown', False, delay=1)
            invoke(self.current_weapon.makeReload, delay= 0.5)

            self.current_weapon.display_text.text = f'Ammo: {self.current_weapon.ammo}/{self.current_weapon.maxAmmo}'

pistol = Weapon("Pistol", 8, 'cube', camera,(.5,-.25,.25), (.3,.2,1), -.5, color.red) 
pistol.muzzle_flash = Entity(parent=pistol, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
_pistol = Weapon("Pistol", 8, 'cube', camera,(-.5,-.25,.25), (.3,.2,1), -.5, color.green) 
_pistol.muzzle_flash = Entity(parent=_pistol, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
_pistol.visible_setter(False)
_player = Player()
_player.añadir_arma(pistol)
_player.añadir_arma(_pistol)


app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))

shootables_parent = Entity()
mouse.traverse_target = shootables_parent
for i in range(16):
    Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1,2),
        x=random.uniform(-8,8),
        z=random.uniform(-8,8) + 8,
        collider='box',
        scale_y = random.uniform(2,3),
        color=color.hsv(0, 0, random.uniform(.9, 1))
        )



sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()