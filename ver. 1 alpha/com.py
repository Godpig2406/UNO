import os

def api(mode, content):
    if mode == "input":
        return input(content)

    elif mode == "output":
        print(content)

    else:
        raise ValueError(f"Invalid api mode: {mode}")
