import sys
from pathlib import Path


def get_boxfile(path):
    """
    Reads a box code file (.bx or .box) and returns its contents.
    """
    path = Path(path)
    if path.suffix not in [".bx", ".box"]:
        print(f"Error: The file '{path}' does not have a .bx or .box extension.", file=sys.stderr)
        print(f"The file has a {path.suffix} extension", file=sys.stderr)
        return None
    
    try:
        return path.read_text()
    except FileNotFoundError:
        print(f"Error: Could not find file '{path}'", file=sys.stderr)
        return None


def pull_cmd_from(line):
    """
    Gets the command from a line.
    Example: 'say is~$age?:~>=~:$drinking_age~?|2' returns 'say'
    """
    if not line.strip():
        return None
    
    parts = line.split(' ', 1)
    return parts[0] if parts else None


def pull_inputs_from(line):
    """
    Gets the arguments from a line, split by |
    Example: 'say is~$age?:~>=~:$drinking_age~?|2' returns ['is~$age?:~>=~:$drinking_age~?', '2']
    """
    if not line.strip():
        return []
    
    parts = line.split(' ', 1)
    if len(parts) < 2:
        return []
    
    args = parts[1].split('|')
    return args


def parse_boxcode(code):
    """
    Parses box code into a list of commands with their arguments.
    Just parsing - no execution.
    """
    if isinstance(code, str):
        code = code.splitlines()
    
    parsed = []
    
    for line in code:
        line = line.strip()
        if not line:
            continue
            
        cmd = pull_cmd_from(line)
        args = pull_inputs_from(line)
        
        if cmd:
            parsed.append({
                'cmd': cmd,
                'args': args
            })
    
    return parsed


def format_parsed_code(parsed_code):
    """
    Formats parsed code back into readable box code format.
    """
    output = []
    for instruction in parsed_code:
        cmd = instruction['cmd']
        args = instruction['args']
        if args:
            line = f"{cmd} {('|').join(args)}"
        else:
            line = cmd
        output.append(line)
    return '\n'.join(output)


# Example usage
if __name__ == "__main__":
    # Example box code
    code = """box drinking_age|21
ask age?
say is~$age?:~>=~:$drinking_age~?|2
box test|data
say ~|1
del test"""
    
    print("code")
    print(code)
    print("code parsed")
    
    parsed = parse_boxcode(code)
    print(format_parsed_code(parsed))
    
    print("\nParsed structure:")
    for instruction in parsed:
        print(instruction)