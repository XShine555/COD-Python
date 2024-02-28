from ursina import Ursina

class MainRender(Ursina):
    
    def __init__(Self, **KWArgs):
        
        super().__init__(**KWArgs)
        
Render = MainRender()

Render.run()
