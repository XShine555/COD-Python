from ursina import Entity, time, Vec3, destroy, raycast, color, distance_xz, random
from physics3d import BoxCollider, CapsuleCollider
from physics3d.character_controller import CharacterController
from ursina.prefabs.health_bar import HealthBar
from Game import Instance
from Scenes.Town import Town
from panda3d.core import Vec3 as PVec3

class Zombies(Entity):
    def __init__(self, can_run = False, **kwargs):
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(4,4,4))
        self.max_hp = 100 * (1.2 ** (Instance.RoundManager.Round - 1))
        self.hp = self.max_hp
        self.random_position()
        self.velocity = 2
        if can_run:
            self.velocity = 8
        super().__init__( model='Models/ZombieMine.obj', texture = 'Models/zombie.png', scale = 2.75, origin_y = 0.5, collider='box', **kwargs)
        self.Controller = CharacterController(Instance.BulletWorld, self)
        #self.ConColl = CapsuleCollider(Instance.BulletWorld, self)

    def random_position(self):
        position = random.choice(Instance.CurrentScene.Respawns)
        print(position.z)
        self.world_position = Vec3(position.world_position.x, position.world_position.y, position.world_position.z)
        #randomnumber = random.randint(0,3)
        #print(self.Respawn[randomnumber])
        #self.world_position = (self.Respawn[randomnumber].x,0,self.Respawn[randomnumber].z )

    def Update(self):
        dist = distance_xz(Instance.FPSController.world_position, self.world_position)
        
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(Instance.FPSController.world_position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        # print(hit_info.entity)
        #self.world_position += self.forward * time.dt * 2
        self.Controller.setLinearMovement(self.forward * self.velocity, True)
        if dist > 2:
            #self.world_position += self.forward * time.dt * 2
            #self.ConColl.position += self.forward * time.dt * 2
            #self.ConColl.setLinearVelocity(PVec3(1, 0, 0) )
            pass
        if hit_info.entity == Instance.FPSController:
            pass
            #if dist > 2:
                #self.world_position += self.forward * time.dt * 2




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