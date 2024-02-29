from ursina import Entity, Vec3
from physics3d.character_controller import CharacterController
from physics3d import BoxCollider
from panda3d.bullet import BulletWorld
from json import load as JsonLoad
from json import dump as JsonWrite
from os.path import exists as PathExists
from Modules.KeyMapper import KeyMapper

class PlayerController(Entity):

    def __init__(Self, KeyMapper : KeyMapper, World : BulletWorld, **KWArgs):

        super().__init__(**KWArgs)

        # Physics And Character Controller.

        Self.Controller = CharacterController(Self)

        Self.BoxCollider = BoxCollider(World, Self)

        # Key Maps

        Self.KeyMapperInstance = KeyMapper

        Self.ReadKeyMap()

    # Basic Movement (Inherits From Controller)

    def Move(Self, Direction : Vec3, IsLocal : bool):

        Self.Controller.setLinearMovement(Direction, IsLocal)

    def Rotate(Self, Direction : float):

        Self.Controller.setAngularMovement(Direction)

    def Jump(Self):

        Self.Controller.doJump()

    # Not Finished ToDo.

    def ReadKeyMap(Self):

        if not PathExists("Configuration.Json"):

            with open("Configuration.Json", "w+") as Config:

                DefaultKeyMap = {

                    "KeyMap" : 
                    { 
                        
                    }
                }

                JsonWrite(DefaultKeyMap, Config)

        with open("Configuration.Json", "r") as Config:

            Load = JsonLoad(Config)

            for Action, Key in Load["KeyMap"]:

                Self.KeyMapperInstance.addKey(Action, Key)

    def AssignKey(Self, Action, NewKey):

        if Action in Self.KeyMap:

            Self.KeyMap[Action] = NewKey