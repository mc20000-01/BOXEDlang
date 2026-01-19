#!/usr/bin/env python3
# boxparser.py

import sys
import argparse
import json
from pathlib import Path


def is_boxfile(path):
    p = Path(path)
    return p.suffix.lower() in (".bx", ".box")


def get_boxfile(path):
    p = Path(path)
    if not is_boxfile(p):
        print(f"error: '{p}' isnt a box file (its '{p.suffix}')", file=sys.stderr)
        return None

    try:
        text = p.read_text(encoding="utf-8")
        return text
    
    except FileNotFoundError:
        print(f"error: cant find '{p}'", file=sys.stderr)
        return None
    
    except PermissionError:
        print(f"error: no permission to read '{p}'", file=sys.stderr)
        return None
    
    except UnicodeDecodeError:
        print(f"error: cant decode '{p}' as utf-8", file=sys.stderr)
        return None


def pull_cmd_from(line):
    if not line or not line.strip():
        return None
    parts = line.lstrip().split(" ", 1)
    return parts[0] if parts else None


def pull_inputs_from(line):
    if not line or not line.strip():
        return []
    parts = line.split(" ", 1)
    if len(parts) < 2:
        return []
    return [arg.strip() for arg in parts[1].split("|")]


def parse_boxcode(code):
    if isinstance(code, str):
        lines = code.splitlines()
    else:
        lines = list(code)

    parsed = []
    
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue

        cmd = pull_cmd_from(line)
        args = pull_inputs_from(line)
        
        if cmd:
            parsed.append({"cmd": cmd, "args": args})
    
    return parsed


def format_parsed_code(parsed_code):
    lines = []
    for instr in parsed_code:
        cmd = instr.get("cmd", "")
        args = instr.get("args", [])
        if args:
            line = f"{cmd} {'|'.join(args)}"
        else:
            line = cmd
        lines.append(line)
    return "\n".join(lines)


def pretty_print(parsed):
    for i, instr in enumerate(parsed, start=1):
        cmd = instr.get("cmd", "")
        args = instr.get("args", [])
        print(f"{i:>3}. {cmd}")
        if args:
            for j, a in enumerate(args, start=1):
                print(f"     - arg {j}: {a}")
    if not parsed:
        print("(nothing found)")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="boxparser", description="parses .bx/.box files")
    parser.add_argument("file", help="box file to parse")
    parser.add_argument("-o", "--output", help="write output to file")
    parser.add_argument("--json", action="store_true", help="output as json")
    parser.add_argument("--raw", action="store_true", help="just print the raw file")
    parser.add_argument("--pretty", action="store_true", help="print in pretty format")
    args = parser.parse_args(argv)

    text = get_boxfile(args.file)
    if text is None:
        return 2

    if args.raw:
        print(text)
        return 0

    parsed = parse_boxcode(text)
    formatted = format_parsed_code(parsed)

    if args.output:
        outp = Path(args.output)
        try:
            outp.write_text(formatted, encoding="utf-8")
            print(f"wrote to: {outp}")
        except Exception as e:
            print(f"error: couldnt write to '{outp}': {e}", file=sys.stderr)
            return 3
        return 0

    if args.json:
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
        return 0

    if args.pretty:
        pretty_print(parsed)
        return 0

    print(formatted)
    return 0


if __name__ == "__main__":
    sys.exit(main())