from json import load as Loader, dump as Save
from Enums.Keys import Keys
from Enums.Actions import Actions
from os import environ as Env, path as Path, makedirs as Mkdir

class KeyMapper:
    
    @staticmethod
    def SearchFile():
        
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
                
                Data = {
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
                
                Save(Data, File)
                
                return Data
        else:
            
            DefaultData = {
                Actions.Forward : Keys.W,
                Actions.Backward : Keys.S,
                Actions.Left : Keys.A,
                Actions.Right : Keys.D,
                Actions.Run : Keys.LeftShift,
                Actions.Jump : Keys.Space,
                Actions.Reload : Keys.R,
                Actions.Aim : Keys.RightMouseDown,
                Actions.ChangeFiremode : Keys.V,
                Actions.Shoot : Keys.LeftMouseDown,
            }
            
            for Key, Value in DefaultData.items():
                
                if not Key in Load:
                    
                    Load[Key] = Value
                    
            TemporalDict = dict(Load)
                    
            for Key, Value in TemporalDict.items():
                
                if not Key in DefaultData:
                    
                    del Load[Key]
                    
            with open(SavedFile, "w+") as File:
                
                Save(Load, File, indent = 4)
                            
            return Load
            
    @staticmethod
    def GetKey(Action):
        
        return KeyMap[Action]
    
KeyMapper.KeyMap = KeyMapper.SearchFile()