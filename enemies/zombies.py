from ursina import Entity, time, Vec3, destroy, raycast, color, distance_xz, random
from physics3d import BoxCollider
from physics3d.character_controller import CharacterController
from ursina.prefabs.health_bar import HealthBar
from Game import Instance

class Zombies(Entity):
    def __init__(self, can_run = False, **kwargs):
        super().__init__( model='cube', scale_y=4, origin_y=-.5, color=color.light_gray, collider='box', **kwargs)
        self.Controller = CharacterController(Instance.BulletWorld, self)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(4,4,4))
        self.max_hp = 100
        self.hp = self.max_hp
        self.random_position()
        self.velocity = 10
        if can_run:
            self.velocity = 20
        
    def random_position(self):
        x = random.uniform(-5, 5)
        y = random.uniform(-2, 2)  
        self.world_position = (x, y, 0)

    def Update(self):
        dist = distance_xz(Instance.FPSController.world_position, self.world_position)
        
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(Instance.FPSController.world_position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        # print(hit_info.entity)
        #self.world_position += self.forward * time.dt * 5
        self.Controller.setLinearMovement(self.forward * self.velocity, True)
        if hit_info.entity == Instance.FPSController:
            if dist > 2:
                self.position += self.forward * time.dt * 5




    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        print("HP", value)
        self._hp = value
        if value <= 0:
            Instance.BulletWorld.remove(self.Controller)
            Instance.RoundManager.Points += 100
            destroy(self)
            Instance.RoundManager.ZombiesInScene -= 1
            Instance.RoundManager.checklast()

            return  
        else:
            Instance.RoundManager.Points += 10

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1