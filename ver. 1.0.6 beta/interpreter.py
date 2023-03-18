
# encode- target=(name or everyone), form=(input or ouput), text=(text)
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
                    return f"everyone: output: {a}"
                case "skip":
                    a=values["text"]
                    return f"everyone: output: {a}"
                case "color":
                    a=values["text"].split(',')
                    return f"{a[0]}: input: {a[1]}"

        case "decode":
            msg=values['text']
            return msg.split(': ')


        case _:
            raise ValueError("translate")
        