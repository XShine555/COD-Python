from json import load as Loader, dump as Save
from Enums.Keys import Keys
from Enums.Actions import Actions
from os import environ as Env, path as Path, makedirs as Mkdir

class KeyMapper:
    
    def __init__(Self):

        Self.KeyMap = Self.SearchFile()

        Self.DefaultData = {
            Actions.Forward : Keys.W,
            Actions.Backward : Keys.S,
            Actions.Left : Keys.A,
            Actions.Right : Keys.D,
            Actions.Run : Keys.LeftShift,
            Actions.Jump : Keys.Space,
            Actions.Reload : Keys.R,
            Actions.Aim : Keys.RightMouseDown,
            Actions.ChangeFiremode : Keys.V,
            Actions.Shoot : Keys.LeftMouseDown
        }
    
    def SearchFile(Self):
        
        Documents = Path.join(Env.get("UserProfile"), "Documents")
        
        SavePath = Path.join(Documents, "COD-Pythons")

        if not Path.exists(SavePath):

            Mkdir(SavePath)

        SavedFile = Path.join(SavePath, "KeyMap.Json")
        
        try:
            
            with open(SavedFile, "r") as File:
            
                Load = Loader(File)
            
        except FileNotFoundError:
            
            with open(SavedFile, "w+") as File:
                
                Save(Self.DefaultData, File)
                
                return Self.DefaultData
        else:
            
            for Key, Value in Self.DefaultData.items():
                
                if not Key in Load:
                    
                    Load[Key] = Value
                    
            TemporalDict = dict(Load)
                    
            for Key, Value in TemporalDict.items():
                
                if not Key in Self.DefaultData:
                    
                    del Load[Key]
                    
            with open(SavedFile, "w+") as File:
                
                Save(Load, File, indent = 4)
                            
            return Load
            
    def GetKey(Self, Action):
        
        return Self.KeyMap[Action]