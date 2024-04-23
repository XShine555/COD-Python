from ursina import Entity, load_texture as LoadTexture, Vec2, camera as InstanceCamera, Button
from random import sample as RandomWithoutRepeating

from ursina import color as Color

class BoxState:

    Bomb = "Bomb"

    Number = "Number"

    Empty = "Empty"

class MineBox(Button):

    def __init__(Self, Parent, Position, Offset, Texture, Size, State, **KWArgs):

        super().__init__(parent = Parent, radius = 0, **KWArgs)

        Self.texture_setter(Texture)

        Self.color = Color.white

        Self.highlight_color = 0.8

        Self.position_setter(Vec2(Position.X / 50, Position.Y / 50) )

        Self.origin_setter(Offset)

        Self.scale_x_setter(Size.X / 100)

        Self.scale_y_setter(Size.Y / 100)

        Self.State = State

class MineSweeper(Entity):

    def __init__(Self, Rows = 16, Cols = 16, Bombs = 8, **KWArgs):

        Self.Rows = Rows

        Self.Cols = Cols

        Self.Bombs = Bombs

        Self.Empty = LoadTexture("Sprites/Empty.png")

        Self.X_Offset = Rows / 2 - 0.5

        Self.Y_Offset = Rows / 2 - 0.5

        Self.Boxs = []

        super().__init__(**KWArgs)

        Self.parent = InstanceCamera.ui

        Self.MakeBoard()

    def MakeBoard(Self):

        BombsSet = RandomWithoutRepeating(range(Self.Rows * Self.Cols), Self.Bombs)
        
        for I in range(Self.Rows):

            for J in range(Self.Cols):

                State = BoxState.Empty

                if (I * J) in BombsSet:

                    State = BoxState.Bomb
                
                Box = MineBox(Parent = Self, Position = Vec2(I, J), Offset = Vec2(Self.X_Offset, Self.Y_Offset), Texture = Self.Empty, Size = Vec2(2, 2), State = State)

                Self.Boxs.append(Box)