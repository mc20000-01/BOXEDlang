# box-code-utills.py
import sys
from pathlib import Path

def get_boxfile(path):
    path = Path(path)
    if path.suffix != ".bx" and path.suffix != ".box":
        print(f"Error: The file '{path}' does not have a .bx or .box extension.", file=sys.stderr)
        print(f"the file has a {path.suffix} extension", file=sys.stderr)
        return None
    else:
        return path.read_text()
    
print(get_boxfile(sys.argv[1]))