from ursina import Entity, Vec3
from ursina import clamp as Clamp
from physics3d.character_controller import CharacterController
from panda3d.bullet import BulletWorld
from ursina import held_keys as HeldKeys
from ursina import camera as StaticCamera
from ursina import mouse as StaticMouse

class PlayerController(Entity):

    def __init__(Self, World : BulletWorld, Height = 10, Fov = 85, **KWArgs):

        super().__init__(**KWArgs)

        # Physics And Character Controller.

        Self.Controller = CharacterController(World, Self)

        Self.Velocity = 14
        
        Self.Height = Height
        
        Self.CameraPivot = Entity(parent = Self, y = Height)
        
        # Camera
        
        Self.SetFirstPerson()
        
        Self.SetFov(Fov)
        
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
        
    def SetFirstPerson(Self):
        
        Self.SetCameraDistance(0)
        
    def SetThirdPerson(Self):
        
        Self.SetCameraDistance(-10)
        
    def update(Self):
        
        # Player Movement
        
        Direction = Vec3(
            
            Self.forward * (HeldKeys['w'] - HeldKeys['s'] )
            
            + Self.right * (HeldKeys['d'] - HeldKeys['a'] )
            
        ).normalized()
        
        Self.Move(Direction * Self.Velocity, True)
        
        # Camera Rotation
        
        Self.rotation_y += StaticMouse.velocity[0] * Self.MouseSensitivity[1]
        
        Self.CameraPivot.rotation_x -= StaticMouse.velocity[1] * Self.MouseSensitivity[0]
        
        Self.CameraPivot.rotation_x = Clamp(Self.CameraPivot.rotation_x, -90, 90)