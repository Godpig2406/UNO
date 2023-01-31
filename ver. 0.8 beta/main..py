import random

ancestor_cards = []
UIDs = [0]


class card:

    def __init__(self, uid, special, color, properties, name):
        self.uid = uid
        self.special = special
        self.color = color
        self.properties = properties
        self.name = name

    def change_color(self,player):
        line = input(f"{player.name}, please pick a color (B)lue, (G)reen, (R)ed, (Y)ellow \n").upper()
        if line == "B" or line == "1":
            self.color = "BLUE"
        elif line == "G" or line == "2":
            self.color = "GREEN"
        elif line == "R" or line == "3":
            self.color = "RED"
        elif line == "Y" or line == "4":
            self.color = "YELLOW"


class player:

    def __init__(self, id, name, punished, next_player_id):
        self.id = id
        self.name = name
        self.punished = punished
        self.hand = []
        self.next_player_id = next_player_id

    def deal(self, amount):
        global deck
        for i in range(amount):
            self.hand.append(deck[0])
            deck.pop(0)

    def check_playable(self, current):
        playable = []
        for card in self.hand:
            if procedures.check_valid(current, card):
                playable.append(card)
        return playable

    def choose(self, avaliable):
        avaliable_uid = [i.uid for i in avaliable]
        print(f"{self.name}'s turn")
        for i in range(len(self.hand)):
            avaliable = ""
            if self.hand[i].uid in avaliable_uid:
                avaliable = "*"
            print(f"[{i}]{self.hand[i].name}{avaliable}")
        print("Current card on the table is: " + current.name)
        choice = input("Choose a Card or (D)raw: ")
        if choice.isnumeric():
            choice = int(choice)
            if choice <= (len(self.hand)) and choice >= 0:
                if self.hand[choice].uid in avaliable_uid:
                    record = self.hand[choice]
                    self.hand.pop(choice)
                    return record

        elif choice.upper() == "D" or choice.upper() == "+":
            self.deal(1)
            return current

    def special_effects(self, card, next_player):
        if not card.special:
            return

        elif card.special:
            next_player.punished = True

            if card.color == "black":

                if card.properties == "+4":
                    next_player.deal(4)
                    card.change_color(self)

                elif card.properties == "change":
                    next_player.punished = False
                    card.change_color(self)

            elif card.color != "black":

                if card.properties == "+2":
                    next_player.deal(2)

                elif card.properties == "skip":
                    return


class procedures:

    def generateUid():
        while True:
            UID = random.randint(0, 111)
            if UID in UIDs:
                pass
            else:
                UIDs.append(UID)
                break
        return UID

    def create():
        for color in ["RED", "GREEN", "BLUE", "YELLOW"]:
            ancestor_cards.append(card(procedures.generateUid(), True, color, "skip", f"{color} skip"))
            ancestor_cards.append(card(procedures.generateUid(), True, color, "skip", f"{color} skip"))
            ancestor_cards.append(card(procedures.generateUid(), True, color, "+2", f"{color} +2"))
            ancestor_cards.append(card(procedures.generateUid(), True, color, "+2", f"{color} +2"))
            ancestor_cards.append(card(procedures.generateUid(), True, "black", "+4", "Wild +4"))
            ancestor_cards.append(card(procedures.generateUid(), True, "black", "change", "Change color"))
            for num in [str(i) for i in range(10)]:
                ancestor_cards.append(card(procedures.generateUid(), False, color, num, f"{color} {num}"))

    def check_valid(old, new):
        if not old.special and not new.special:
            if old.color == new.color or old.properties == new.properties:
                return True

        elif not old.special and new.special:
            if old.color == new.color or new.color == "black":
                return True

        elif old.special and not new.special:
            if old.color == new.color:
                return True
            elif old.color == "black":
                return True

        elif old.special and new.special:
            if old.color == new.color or old.properties == new.properties or new.color == "black":
                return True

    def next_player(list_of_players, current_player):
        for i in list_of_players:
            if i.id == current_player.next_player_id:
                return i


procedures.create()
deck = ancestor_cards.copy()
random.shuffle(deck)

name1 = "God"
name2 = "Pig"
p1 = player(1, name1, False, 2)
p2 = player(2, name2, False, 1)
players = [p1, p2]
p1.deal(7)
p2.deal(7)

played = []

for cards in deck:
    if not cards.special:
        current = cards
        played.append(current)
        break

playing=True
i=0

while True:
    player = players[i]
    if i+1 == len(players):
        i=0
        next_player = players[0]
    elif i+1 != len(players):
        next_player=players[i+1]
        i=i+1

    next_player = procedures.next_player(players, player)

    if not player.punished:
        player_avaliable = player.check_playable(current)
        player_chosen = player.choose(player_avaliable)
        if player_chosen != current:
            current = player_chosen
            played.append(current)
            player.special_effects(current, next_player)
            if len(player.hand) == 0:
                winner=player
                playing=False
                break

    if player.punished:
        player.punished = False
        print(f"Skipped {player.name}")

print(f"{player.name} wins!!!")