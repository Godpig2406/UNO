
# encode- target=(name or everyone), form=(input or ouput), text=(text)
# decode-
# forms:
"""
ask for player name
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
            pass

        case "decode":
            pass

        case _:
            raise ValueError("translate")
        