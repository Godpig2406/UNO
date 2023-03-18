history=[]

def api(**content):
    history.append([content["mode"],content["text"]])
    match content["mode"]:
        case "output":
            print(content["text"])
        case "input":
            return input(content["text"])
