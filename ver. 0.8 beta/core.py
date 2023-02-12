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

    def __init__(self, id, name, punished):
        self.id = id
        self.name = name
        self.punished = punished
        self.hand = []
        self.neighbors = []

    def deal(self, amount, deck):
        for i in range(amount):
            self.hand.append(deck[0])
            deck.pop(0)

    def create_neighbors(self, players):
        for i in range(len(players)):
            if players[i] == self:
                id=self.id
                break
        if len(players) <= 2:
            if i == 0:
                self.neighbors=[players[1],players[1]]

        elif len(players) >= 3:
            prev, after = i-1, i+1

            if i == 0:
                prev=-1
            
            elif i == len(players)-1:
                after = 0

            self.neighbors = [players[prev], players[after]]

    def check_playable(self, current):
        playable = []
        for card in self.hand:
            if procedures.check_valid(current, card):
                playable.append(card)
        return playable

    def choose(self, avaliable, deck, current):
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
            self.deal(1,deck)
            return None

        else:
            return "a"

    def special_effects(self, card, next_player, deck):
        if not card.special:
            return False

        elif card.special:
            next_player.punished = True

            if card.color == "black":

                if card.properties == "+4":
                    next_player.deal(4,deck)
                    card.change_color(self)

                elif card.properties == "change":
                    next_player.punished = False
                    card.change_color(self)

            elif card.color != "black":

                if card.properties == "+2":
                    next_player.deal(2, deck)

                elif card.properties == "skip":
                    return False

                elif card.properties == "reverse":
                    next_player.punished = False
                    return True


class procedures:
    def __init__(self, status=None, deck=None, played=None, players=None, clockwise=None, current_player=None, next_player=None, current=None):
        self.status = status #number of players and etc.
        self.deck=deck
        self.played=played
        self.players=players
        self.clockwise=clockwise
        self.current_player=current_player
        self.next_player=next_player
        self.current=current

    def gen_Uid():
        while True:
            UID = random.randint(0, 255)
            if UID in UIDs:
                pass
            else:
                UIDs.append(UID)
                break
        return UID

    def create():
        for color in ["RED", "GREEN", "BLUE", "YELLOW"]:
            ancestor_cards.append(card(procedures.gen_Uid(), True, color, "+2", f"{color} +2"))
            ancestor_cards.append(card(procedures.gen_Uid(), True, color, "+2", f"{color} +2"))
            ancestor_cards.append(card(procedures.gen_Uid(), True, color, "skip", f"{color} skip"))
            ancestor_cards.append(card(procedures.gen_Uid(), True, color, "skip", f"{color} skip"))
            ancestor_cards.append(card(procedures.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            ancestor_cards.append(card(procedures.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            ancestor_cards.append(card(procedures.gen_Uid(), True, "black", "+4", "Wild +4"))
            ancestor_cards.append(card(procedures.gen_Uid(), True, "black", "change", "Change color"))
            for num in [str(i) for i in range(10)]:
                ancestor_cards.append(card(procedures.gen_Uid(), False, color, num, f"{color} {num}"))
                ancestor_cards.append(card(procedures.gen_Uid(), False, color, num, f"{color} {num}"))

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

    def gen_next_player(current_player, clockwise):
        if clockwise:
            return current_player.neighbors[1]
        elif not clockwise:
            return current_player.neighbors[0]


game = procedures([3])
procedures.create()
game.deck = ancestor_cards.copy()
random.shuffle(game.deck)
name1 = "God"
name2 = "Pig"
name3 = "sa"
p1 = player(1, name1, False)
p2 = player(2, name2, False)
p3 = player(3, name3, False)
game.players = [p1, p2, p3]
for i in game.players:
    i.create_neighbors(game.players)
    i.deal(7,game.deck)

game.played = []

for cards in game.deck:
    if not cards.special:
        game.current = cards
        game.played.append(game.current)
        break

game.clockwise = True
game.current_player=game.players[0]
game.next_player=procedures.gen_next_player(game.current_player, game.clockwise)
while True:
    game.next_player = procedures.gen_next_player(game.current_player, game.clockwise)
    if not game.current_player.punished:
        player_avaliable = game.current_player.check_playable(game.current)
        player_chosen = game.current_player.choose(player_avaliable, game.deck, game.current)
        if player_chosen != None:
            game.current = player_chosen
            game.played.append(game.current)
            reversed=game.current_player.special_effects(game.current, game.next_player, game.deck)
            if reversed:
                print("reversed")
                game.clockwise = not game.clockwise
                game.next_player=procedures.gen_next_player(game.current_player, game.clockwise)
            if len(game.current_player.hand) == 0:
                winner=game.current_player
                break


    if game.current_player.punished:
        game.current_player.punished = False
        print(f"Skipped {game.current_player.name}")

    game.current_player=game.next_player

print(f"{game.current_player.name} wins!!!")