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
            print("tetas")
            variableName = variable.name
            variableType = variable.content["type"]
            if variableType == "player":
                print("Creating new player")
                Self.Players[variableName] = PlayerRepresentation(model="cube", collider="box", color= color.blue)
        
        @Self.Easy.event
        def onReplicatedVariableUpdated(variable):
            variableName = variable.name
            variableType = variable.content["type"]
            if variableType == "player":
                Self.Players[variableName].UpdatePos(variable.content["position"] )
                Self.Players[variableName].UpdateRot(variable.content["rotation"] )
        
        
        