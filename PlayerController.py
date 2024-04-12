from ursina import Entity, Vec3
from ursina import clamp as Clamp
from physics3d.character_controller import CharacterController
from panda3d.bullet import BulletWorld
from ursina import camera as StaticCamera
from ursina import mouse as StaticMouse
from Enums.Actions import Actions
from KeyMapper import KeyMapper

from Game import Instance

class PlayerController(Entity):

    def __init__(Self, World : BulletWorld, StandardFov = 80, Height = 10, Fov = 85, RunVelocity = 24, WalkVelocity = 14, **KWArgs):

        super().__init__(**KWArgs)

        # Physics And Character Controller.

        Self.Controller = CharacterController(World, Self)

        Self.WalkVelocity = WalkVelocity
        
        Self.RunVelocity = RunVelocity

        Self.Velocity = Self.WalkVelocity
        
        Self.Height = Height
        
        Self.CameraPivot = Entity(parent = Self, y = Height)
        
        Self.CanMove = True

        Self.Freeze = False

        Self.CanJump = True

        Self.Running = False

        Self.CanRun = True
        
        Self.Jumping = not Self.Controller.can_jump
        
        # Camera
        
        Self.SetFirstPerson()
        
        Self.SetFov(StandardFov)
        
        StaticCamera.parent = Self.CameraPivot
        
        # Mouse Settings
        
        Self.MouseSensitivity = (40, 40)
        
        StaticMouse.locked = True

    # Basic Movement (Inherits From Controller)

    def Move(Self, Direction : Vec3, IsLocal : bool):

        Self.Controller.setLinearMovement(Direction, IsLocal)

    def Rotate(Self, Direction : float):

        Self.Controller.setAngularMovement(Direction)

    def Jump(Self):

        Self.Controller.doJump()
        
    def SetHeight(Self, Height):
        
        Self.Height = Height
        
        Self.CameraPivot.Y = Height
        
    # Static Camera Settings
        
    def SetCameraDistance(Self, Value):
        
        StaticCamera.z = Value
        
    def SetFov(Self, Value):
        
        StaticCamera.fov = Value
        
    def AddFov(Self, Value):
        
        StaticCamera.fov += Value
        
    def RemoveFov(Self, Value):
        
        StaticCamera.fov -= Value
        
    def SetFirstPerson(Self):
        
        Self.SetCameraDistance(0)
        
    def SetThirdPerson(Self):
        
        Self.SetCameraDistance(-10)

    def SetRunningState(Self, Running):

        Self.Running = Running

        if Self.Running:

            Self.Velocity = Self.RunVelocity

        else:

            Self.Velocity = Self.WalkVelocity
        
    def HandleInput(Self, Key):
        
        if Key == KeyMapper.GetKey(Actions.Run) and Self.CanRun:

            Self.SetRunningState(True)

        elif Key == F"{KeyMapper.GetKey(Actions.Run) }_up":

            Self.SetRunningState(False)
            
        elif Key == KeyMapper.GetKey(Actions.Jump):

            if Self.Jumping or Self.Freeze or not Self.CanJump:
                
                return
            
            Self.Jump()

    def Update(Self, DeltaTime):
        
        # Player Movement
        
        if Self.Freeze:

            return

        if not Self.CanMove:

            Direction = Vec3(
            
                Self.forward * (Instance.HeldKeys[KeyMapper.GetKey(Actions.Forward) ] - Instance.HeldKeys[KeyMapper.GetKey(Actions.Backward) ] )
                
                + Self.right * (Instance.HeldKeys[KeyMapper.GetKey(Actions.Right) ] - Instance.HeldKeys[KeyMapper.GetKey(Actions.Left) ] )
                
            ).normalized()
            
            Self.Move(Direction * Self.Velocity, True)
        
        # Camera Rotation
        
        Self.rotation_y += StaticMouse.velocity[0] * Self.MouseSensitivity[1]
        
        Self.CameraPivot.rotation_x -= StaticMouse.velocity[1] * Self.MouseSensitivity[0]
        
        Self.CameraPivot.rotation_x = Clamp(Self.CameraPivot.rotation_x, -90, 90)