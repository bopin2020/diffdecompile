import io
import os
import msgspec #type: ignore

from datetime import datetime

class Metadata(msgspec.Struct):
    Date : str
    Count : int
    Items : set[str] = set()

def write_tofile():
    f = list(get_decompile_files())
    msg = msgspec.json.encode(Metadata(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),len(f),f))
    with open('index.json','wb') as f:
        f.write(msg)

def get_decompile_files():
    for root,dirs,files in os.walk('.'):
        for file in files:
            if file.endswith('diffdecompile'):
                yield file

write_tofile()