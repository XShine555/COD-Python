from ursinanetworking import UrsinaNetworkingClient, EasyUrsinaNetworkingClient
from ParentClass.PlayerRepresentation import PlayerRepresentation
from ursina import color

@staticmethod
class Client():
    
    def __init__(Self, IP, Port = 8080) -> None:
        
        Self.Client = UrsinaNetworkingClient(IP, Port)
        
        Self.Easy = EasyUrsinaNetworkingClient(Self.Client)
        
        Self.Id = None
        
        Self.Players = { }
        
        @Self.Client.event
        def GetId(Id):
            Self.Id = Id
        
        @Self.Easy.event
        def onReplicatedVariableCreated(variable):
            variableName = variable.name
            variableType = variable.content["type"]
            if variableType == "player" and variable.content["id"] == Self.Id:
                return
            if variableType == "player":
                Self.Players[variableName] = PlayerRepresentation(model="cube", collider="box", color= color.blue)
        
        @Self.Easy.event
        def onReplicatedVariableUpdated(variable):
            variableName = variable.name
            variableType = variable.content["type"]
            if variableType == "player" and variable.content["id"] == Self.Id:
                return
            if variableType == "player":
                Self.Players[variableName].UpdatePos(variable.content["position"] )
                Self.Players[variableName].UpdateRot(variable.content["rotation"] )
                
Instance = None