from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from panda3d.ai import *

app = Ursina()

ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
new = Entity(model='cube', collider='box', color=color.orange, z=-10, origin_y=-.5)

player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))

aiworld = AIWorld(app.render)
aichar = AICharacter("mychar", new, 100, 0.05, 5)
aiworld.addAiChar(aichar)
aichar.generateAiMesh('navmesh')

app.run()