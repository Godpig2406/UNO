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

    def change_color(self, player):
        line = input(
            f"{player.name}, please pick a color (B)lue, (G)reen, (R)ed, (Y)ellow \n").upper()
        if line == "B" or line == "1":
            self.color = "BLUE"

        elif line == "G" or line == "2":
            self.color = "GREEN"

        elif line == "R" or line == "3":
            self.color = "RED"

        elif line == "Y" or line == "4":
            self.color = "YELLOW"


class player:

    def __init__(self, id, name, punished):
        self.id = id
        self.name = name
        self.punished = punished
        self.hand = []
        self.neighbors = []
        self.chosen = None

    def create_neighbors(self, players):
        for i in range(len(players)):
            if players[i] == self:
                id = self.id
                break

        if len(players) <= 2:
            if i == 0:
                self.neighbors = [players[1], players[1]]

        elif len(players) >= 3:
            prev, after = i - 1, i + 1
            if i == 0:
                prev = -1

            elif i == len(players) - 1:
                after = 0

            self.neighbors = [players[prev], players[after]]

    def check_playable(self, current):
        playable = []
        for card in self.hand:
            if procedures.check_valid(current, card):
                playable.append(card)

        return playable

    def choose(self, avaliable, deck, current, game):
        avaliable_uid = [i.uid for i in avaliable]
        print(f"{self.name}'s turn")

        for i in range(len(self.hand)):
            avaliable = ""
            if self.hand[i].uid in avaliable_uid:
                avaliable = "*"

            print(f"[{i}]{self.hand[i].name}{avaliable}")

        print("Current card on the table is: " + current.name)
        choice = input("Choose a Card or (D)raw: ")

        if choice == "":
            return False

        if choice.isnumeric():
            choice = int(choice)
            if choice < (len(self.hand)) and choice >= 0:

                if self.hand[choice].uid in avaliable_uid:
                    record = self.hand[choice]
                    self.hand.pop(choice)
                    self.chosen = record
                    return True

                else:
                    print("Unvalid")
                    return False

            else:
                print("Out of range")
                return False

        elif choice.upper() == "D" or choice.upper() == "+":
            game.deal(self, 1)
            self.chosen = None
            return True

        else:
            print("input error")
            return False

    def special_effects(self, card, next_player, game):
        if not card.special:
            return False

        elif card.special:
            next_player.punished = True

            if card.color == "black":

                if card.properties == "+4":
                    game.deal(game.gen_next_player(), 4)
                    card.change_color(self)

                elif card.properties == "change":
                    next_player.punished = False
                    card.change_color(self)

            elif card.color != "black":

                if card.properties == "+2":
                    game.deal(game.gen_next_player(), 2)

                elif card.properties == "skip":
                    return False

                elif card.properties == "reverse":
                    next_player.punished = False
                    return True


class procedures:

    def __init__(self, status, deck=None, players=None):
        self.status = status  #number of players and etc.
        self.deck = deck
        self.played = []
        self.players = players
        self.clockwise = True
        self.current_player = None
        self.next_player = None
        self.current = None

    def gen_Uid(self):
        while True:
            UID = random.randint(0, 255)
            if UID in UIDs:
                pass

            else:
                UIDs.append(UID)
                break

        return UID

    def create(self):
        for color in ["RED", "GREEN"]:  #, "BLUE", "YELLOW"
            ancestor_cards.append(card(self.gen_Uid(), True, color, "+2", f"{color} +2"))
            #ancestor_cards.append(card(self.gen_Uid(), True, color, "+2", f"{color} +2"))
            ancestor_cards.append(card(self.gen_Uid(), True, color, "skip", f"{color} skip"))
            #ancestor_cards.append(card(self.gen_Uid(), True, color, "skip", f"{color} skip"))
            ancestor_cards.append(card(self.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            #ancestor_cards.append(card(self.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            ancestor_cards.append(card(self.gen_Uid(), True, "black", "+4", "Wild +4"))
            ancestor_cards.append(card(self.gen_Uid(), True, "black", "change", "Change color"))
            for num in [str(i) for i in range(10)]:
                ancestor_cards.append(card(self.gen_Uid(), False, color, num, f"{color} {num}"))
            #     ancestor_cards.append(card(self.gen_Uid(), False, color, num, f"{color} {num}"))

        self.deck = ancestor_cards.copy()
        random.shuffle(self.deck)

    def gen_next_player(self):
        if self.clockwise:
            self.next_player = self.current_player.neighbors[1]
            return self.current_player.neighbors[1]

        elif not self.clockwise:
            self.next_player = self.current_player.neighbors[0]
            return self.current_player.neighbors[0]

    def deal(self, player, amount):
        for i in range(amount):
            if len(self.deck) != 0:
                player.hand.append(self.deck[0])
                self.deck.pop(0)
            
            elif len(self.deck) == 0:
                self.status.append(False)
                break
                
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

    def gameloop(self):
        while True:
            self.gen_next_player()
            print(len(self.deck), len(self.played))
            if not self.current_player.punished:
                player_avaliable = self.current_player.check_playable(self.current)
                while True:
                    valid = self.current_player.choose(player_avaliable, self.deck, self.current, self)
                    if valid:
                        break

                if len(self.status) == 2:
                    a=[len(i.hand) for i in self.players]
                    b=max(a)
                    for i in self.players:
                        if len(i.hand) == b:
                            winner = i
                    break

                player_chosen = self.current_player.chosen

                if player_chosen != None:
                    self.current = player_chosen
                    self.played.append(self.current)
                    reversed = self.current_player.special_effects(self.current, self.next_player, self)

                    if reversed:
                        print("reversed")
                        self.clockwise = not self.clockwise
                        self.gen_next_player()

                    if len(self.current_player.hand) == 0:
                        winner = self.current_player
                        break

            if self.current_player.punished:
                self.current_player.punished = False
                print(f"Skipped {self.current_player.name}")

            self.current_player = self.next_player

        return winner


game = procedures([3])
game.create()
game.players = [player(1, "name1", False), player(2, "name2", False), player(3, "name3", False)]

for i in game.players:
    i.create_neighbors(game.players)
    game.deal(i, 7)

for cards in game.deck:
    if not cards.special:
        game.current = cards
        game.played.append(game.current)
        break

game.clockwise = True
game.current_player = game.players[0]
game.gen_next_player()
game.gameloop()

print(f"{game.current_player.name} wins!!!")
