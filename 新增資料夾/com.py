history=[]

class protocol:
    def __init__(self):
        self.dictionary = dict()

    def load(self,version):
        try:
            with open(f"dict v{version}.txt") as dictionary:
                list=[lines.split("\n")[0] for lines in dictionary]
                for i in list:
                    self.dictionary.update({list.index(i):i})

        except:
            print("error")

    def api(self, **values):
        mode=values["mode"]
        data=values["data"]
        name=values["name"]


def api(**content):
    history.append([content["mode"],content["text"]])
    match content["mode"]:
        case 0:
            pass
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case 10:
            pass
        case 11:
            pass
        case 12:
            pass
        case 13:
            pass
        case 14:
            pass
        case "output":
            print(content["text"])
        case "input":
            return input(content["text"])

a=protocol()
a.load(0.1)


import server
server.start_server()