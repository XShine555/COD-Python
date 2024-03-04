from ursinanetworking import UrsinaNetworkingClient, EasyUrsinaNetworkingClient
from ParentClass.PlayerRepresentation import PlayerRepresentation
from ursina import color

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
            if variableType == "player":
                Self.Players[variableName] = PlayerRepresentation(variable.content["position"], variable.content["rotation"], model="cube", color=color.red )
        
        @Self.Easy.event
        def onReplicatedVariableUpdated(variable):
            variableName = variable.name
            variableType = variable.content["type"]
            if variableType == "position":
                Self.Players[variableName] = variable.content["position"]
            elif variableType == "rotation":
                Self.Players[variableName] = variable.content["rotation"]
        
        
        