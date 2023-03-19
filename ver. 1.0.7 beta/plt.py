import com, time, interpreter

def api(**content):
    global connection
    match content["mode"]:
        case "output":
            print(content["text"])

        case "input":
            return input(content["text"])
        
        case "win":
            msg=interpreter.translate(mode="encode", text=content["text"], form="win")
            connection.write(msg)

        case "color":
            msg=interpreter.translate(mode='encode', text=content["text"], form='color')
            connection.client.send(msg.encode())
            while True:
                print(type(com.reply))
                if com.reply != None:
                    break
            print(com.reply+'afe')
            com.reply=None
            # return reply

        case "skip":
            msg=interpreter.translate(mode='encode', text=content["text"], form='skip')
            connection.write(msg)

        case 'reverse':
            msg=interpreter.translate(mode='encode', text=content["text"], form='reverse')
            connection.write(msg)
        case 'listcard':
            pass
        case 'pickcard':
            pass
        case 'current':
            pass

connection=com.start(1)

while len(com.connected) < 1:
    time.sleep(1)
    print("wait for join")

names=list(com.connected.values())
api(mode ="win",text=f"asdf wins!!!")
asdf=api(mode ="color",text=f"{names[0]},color")