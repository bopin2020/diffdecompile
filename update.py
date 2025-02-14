import io
import os
import sys
import json
from datetime import datetime

__AUTHOR__ = 'bopin'
__VERSION__ = '0.1'

'''
host diffdecompile grouping format
'''

g_data = []
class Object:
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

class Element(json.JSONEncoder):
    def __init__(self,file):
        self.File: str = file
    def data(self, o):
        return [o.File]

class SubMetadata(json.JSONEncoder):
    def __init__(self):        
        self.Date: str
        self.Count: int
        self.Items = []
    def data(self):
        return {
            'Date':self.Date,
            'Count':self.Count,
            'Items':self.Items
        }

class Metadata(json.JSONEncoder):
    def __init__(self):      
        self.OS: str
        self.Count : int
        self.Items = []

    def data(self):
        return {
            'OS':self.OS,
            'Count':self.Count,
            'Items':self.Items
        }

class GroupingFormat(json.JSONEncoder,Object):
    def __init__(self):
        self.Date: str
        self.Count: int
        self.Items = []

    def data(self):
        return {
            'Date':self.Date,
            'Count':self.Count,
            'Items':self.Items
        }
    

def write_tofile():
    f = get_decompile_files()
    save_to_json(f,'index.json')

def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        f.write(data.toJSON())


def get_decompile_files():
    gf = GroupingFormat()
    gf.Date = str(datetime.now())
    gf.Count = 0
    try:
        entries = os.listdir('data')
        for d in entries:
            mt = Metadata()
            mt.OS = d
            mt.Count = 0
            for sd in os.listdir(os.path.join('data',d)):
                smt = SubMetadata()
                smt.Date = sd
                smt.Count = 0
                for f in os.listdir(os.path.join('data',d,sd)):
                    smt.Items.append(Element(f))
                    smt.Count += 1
                    gf.Count += 1
                mt.Items.append(smt)
                mt.Count += 1
            gf.Items.append(mt)
    except PermissionError:
        return
    return gf

write_tofile()