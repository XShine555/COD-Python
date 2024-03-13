from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

class Game():
    def __init__(self):
        self.menu = False
        self.gameStarted = False

    def hudmenu(self):
        if self.gameStarted:
           pass 

    def start_game(self):
        destroy(button)
        destroy(button2)
        random.seed(0)
        Entity.default_shader = lit_with_shadows_shader
        ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
        editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
        player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
        self.setupWeapons()
        self.gameStarted = True

    def setupWeapons(self):
        self.pistol = Weapon("Pistol", 8, 'cube', camera,(.5,-.25,.25), (.3,.2,1), -.5, color.red,1) 
        self.pistol.muzzle_flash = Entity(parent=self.pistol, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False,)
        self._pistol = Weapon("Pistol", 8, 'cube', camera,(-.5,-.25,.25), (.3,.2,1), -.5, color.green,0.5) 
        self._pistol.muzzle_flash = Entity(parent=self._pistol, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
        self._player = Player(self.pistol)

        self._pistol.visible_setter(False)
        self._player.añadir_arma(self._pistol)
        self._player.añadir_arma(self.pistol)

class HUD():
    def __init__(self):
        self.ammoText = Text(parent= camera.ui, text=f'Ammo: Not Set', y=-0.3, origin=(0, 0), background=True)
    def updateAmmo(self, newAmmo, newMaxAmmo):
        self.ammoText.text = f'Ammo: {newAmmo}/{newMaxAmmo}'

class Weapon(Entity):
    def __init__(self, name, maxAmmo,model,parent,position,scale,origin_z,color,time_cooldown):
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
        self.time_cooldown = time_cooldown

    def shoot(self):
        self.cooldown = True
        self.muzzle_flash.enabled = True   
        self.ammo -= 1
        invoke(self.muzzle_flash.disable, delay=.05)
        invoke(setattr,self,'cooldown', False, delay=self.time_cooldown)
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




class Player(Entity):
    def __init__(self, pistol):
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


            
def input(key):
    if game.gameStarted:
        if key == "r" and not _player.current_weapon.cooldown:
            game._player.current_weapon.reload() 

        if key == 'q'and not _player.current_weapon.cooldown and not _player.current_weapon.reloading:
            game._player.switch_weapon()

    if key == "enter":
        game.start_game()
        print("hola")

def update():
    if game.gameStarted:
        if held_keys["left mouse"] and not game._player.current_weapon.cooldown and not game._player.current_weapon.reloading:
            game._player.current_weapon.shoot()

        if game._player.current_weapon.reloading and not game._player.current_weapon.cooldown:
            game._player.current_weapon.cooldown = True
            invoke(setattr, game._player.current_weapon, 'cooldown', False, delay=1)
            invoke(game._player.current_weapon.makeReload, delay= 0.5)
        hud.updateAmmo(game._player.current_weapon.ammo, game._player.current_weapon.maxAmmo)
        #_player.current_weapon.display_text.text = f'Ammo: {_player.current_weapon.ammo}/{_player.current_weapon.maxAmmo}'

hud = HUD()

app = Ursina()
game = Game()
button = Button(text="Zombies", color=color.red, scale=(0.6, 0.1), position=(-0.5, 0.1))
button2 = Button(text="Quit", color=color.black, scale=(0.6, 0.1), position=(-0.5, -0.1))

button.on_click = game.start_game
button2.on_click = application.quit

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()