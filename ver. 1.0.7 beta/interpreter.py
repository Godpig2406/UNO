
# encode- target=(name or everyone), form=(win or color), text=(text)
# decode-
# forms:
"""
skipped player
reversed
input error
ok(didnt play drawed card)
drawed card is playable play or not 
error input out of range
error inout invalid
pick a color
pick a card
players turn
this card is avaliable or not
current card on the table
print winner
"""


def translate(**values):
    match values["mode"]:
        case "encode":
            match values["form"]:
                case "win":
                    a=values["text"]
                    return f"everyone: win: {a}"
                case "skip":
                    a=values["text"]
                    return f"everyone: {a}"
                case "color":
                    a=values["text"].split(',')
                    return f"admin: {a[0]}: {a[1]}"
                case 'reverse':
                    a=values["text"]
                    return f"everyone: {a}"


        case "decode":
            msg=values['text']
            return msg.split(': ')


        case _:
            raise ValueError("translate")
        