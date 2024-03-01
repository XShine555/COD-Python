from ursinanetworking import UrsinaNetworkingServer, EasyUrsinaNetworkingServer

class Server():
    
    def __init__(Self, IP, Port):
        
        Self.Server = UrsinaNetworkingServer(IP, Port)
        
        Self.Easy = EasyUrsinaNetworkingServer(Self.Server)
        
        @Self.Server.event
        def onClientConnected(Client):
            Self.Easy.create_replicated_variable(
                F"player_{Client.id}",
                { 
                 "type" : "player", 
                 "id" : Client.id, 
                 "position" : (0, 0, 0),
                 "rotation" : (0, 0, 0) 
                }
            )
            Client.send_message("GetId", Client.id)
            
        @Self.Server.event
        def onClientDisconnected(Client):
            Self.Easy.remove_replicated_variable_by_name(f"player_{Client.id}")
            
        @Self.Server.event
        def updatePosition(Client, NewPos):
            Self.Easy.update_replicated_variable_by_name(f"player_{Client.id}", "position", NewPos)
            
        @Self.Server.event
        def updateRotation(Client, LookAt):
            Self.Easy.update_replicated_variable_by_name(f"player_{Client.id}", "rotation", LookAt)