import random

ancestor_cards = []
UIDs = [0]

def api(mode, content):
    if mode == "input":
        return input(content)

    elif mode == "output":
        print(content)

    else:
        raise ValueError(f"Invalid api mode: {mode}")

class card:
    def __init__(self, uid, special, color, properties, name):
        self.uid = uid
        self.special = special
        self.color = color
        self.properties = properties
        self.name = name

    def change_color(self, player):
        while True:
            line = api("input", f"{player.name}, please pick a color (B)lue, (G)reen, (R)ed, (Y)ellow \n").upper()
            if line == "B" or line == "1":
                self.color = "BLUE"
                break

            elif line == "G" or line == "2":
                self.color = "GREEN"
                break

            elif line == "R" or line == "3":
                self.color = "RED"
                break

            elif line == "Y" or line == "4":
                self.color = "YELLOW"
                break

            else:
                raise ValueError("Change color")

    def debug(self):
        return f"{self.uid, self.special, self.color, self.properties, self.name}"


class player:

    def __init__(self, id, name, punished):
        self.id = id
        self.name = name
        self.punished = punished
        self.hand = []
        self.neighbors = []
        self.chosen = None

    def debug(self):
        return f"{self.id, self.name, self.punished, self.hand, self.hand, self.neighbors, self.chosen}"

    def create_neighbors(self, players):
        for i in range(len(players)):
            if players[i] == self:
                id = self.id
                break

        if len(players) == 2:
            if i == 0:
                self.neighbors = [players[1], players[1]]
            
            elif i == 1:
                self.neighbors = [players[0], players[0]]


        elif len(players) >= 3:
            prev, after = i - 1, i + 1
            if i == 0:
                prev = -1

            elif i == len(players) - 1:
                after = 0

            self.neighbors = [players[prev], players[after]]

        else:
            raise Exception(f"Only one player {players}")


    def check_playable(self, current):
        playable = []
        for card in self.hand:
            if procedures.check_valid(current, card):
                playable.append(card)
        
        return playable

    def choose(self, avaliable, game):
        avaliable_uid = [i.uid for i in avaliable]
        api("output", f"{self.name}'s turn")

        for i in range(len(self.hand)):
            avaliable = ""
            if self.hand[i].uid in avaliable_uid:
                avaliable = "*"

            api("output", f"[{i}]{self.hand[i].name}{avaliable}")

        api("output", f"Current card on the table is: {game.current.name}")
        choice = api("input", "Choose a Card or (D)raw: ")

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
                    api("output","Unvalid")
                    return False

            else:
                api("output","Out of range")
                return False

        elif choice.upper() == "D" or choice.upper() == "+":
            game.deal(self, 1)
            drawed=self.hand[-1]
            if procedures.check_valid(game.current, drawed):
                a = api("input", f"{self.name}, {drawed.name} is playable, (Y/n)")
                if a=="n" or a=="N" or a == "-":
                    api("output","ok")
                    self.chosen = None

                else:
                    self.chosen = drawed
                

            return True

        else:
            api("output","input error")
            return False

    def special_effects(self, game):
        card = game.current
        if not card.special:
            return False

        elif card.special:
            game.next_player.punished = True

            if card.color == "black":

                if card.properties == "+4":
                    game.deal(game.gen_next_player(), 4)
                    card.change_color(self)

                elif card.properties == "change":
                    game.next_player.punished = False
                    card.change_color(self)

            elif card.color != "black":

                if card.properties == "+2":
                    game.deal(game.gen_next_player(), 2)

                elif card.properties == "skip":
                    return False

                elif card.properties == "reverse":
                    game.next_player.punished = False
                    return True

        else:
            raise Exception("Impossible error in card.properties")


class procedures:

    def __init__(self, status=None, deck=None):
        self.status = status  #number of players and etc.
        self.deck = deck
        self.played = []
        self.players = []
        self.clockwise = True
        self.current_player = None
        self.next_player = None
        self.current = None
        self.debug = False

    def gen_Uid(self):
        while True:
            UID = random.randint(0, 512)
            if UID not in UIDs:
                UIDs.append(UID)
                break

        return UID

    def create(self):
        for color in ["RED", "GREEN", "BLUE", "YELLOW"]:
            ancestor_cards.append(card(self.gen_Uid(), True, color, "+2", f"{color} +2"))
            ancestor_cards.append(card(self.gen_Uid(), True, color, "+2", f"{color} +2"))
            ancestor_cards.append(card(self.gen_Uid(), True, color, "skip", f"{color} skip"))
            ancestor_cards.append(card(self.gen_Uid(), True, color, "skip", f"{color} skip"))
            ancestor_cards.append(card(self.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            ancestor_cards.append(card(self.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            ancestor_cards.append(card(self.gen_Uid(), True, "black", "+4", "Wild +4"))
            ancestor_cards.append(card(self.gen_Uid(), True, "black", "change", "Change color"))
            for num in [str(i) for i in range(10)]:
                ancestor_cards.append(card(self.gen_Uid(), False, color, num, f"{color} {num}"))
                ancestor_cards.append(card(self.gen_Uid(), False, color, num, f"{color} {num}"))

        self.deck = ancestor_cards.copy()
        random.shuffle(self.deck)

    def gen_next_player(self):
        if self.clockwise:
            self.next_player = self.current_player.neighbors[1]
            return self.current_player.neighbors[1]

        elif not self.clockwise:
            self.next_player = self.current_player.neighbors[0]
            return self.current_player.neighbors[0]

        else:
            raise Exception("Impossible error game.proerties status")

    def deal(self, player, amount):
        for i in range(amount):
            if len(self.deck) != 0:
                player.hand.append(self.deck[0])
                self.deck.pop(0)
            
            elif len(self.deck) == 0:
                self.status.append(False)
                break

            else:
                raise Exception("dealing")
                
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

        else:
            raise Exception("Comparing 2 cards")

    def gameloop(self):
        global winner, winners
        while True:
            self.gen_next_player()
            if not self.current_player.punished:
                player_avaliable = self.current_player.check_playable(self.current)
                while True:
                    valid = self.current_player.choose(player_avaliable, self)
                    if valid:
                        break

                if len(self.status) == 2:#additional status when game ends
                    highest=max([len(i.hand) for i in self.players])

                    winners=[ i for i in self.players if len(i.hand) == highest]
                    for i in self.players:
                        if len(i.hand) == highest:
                            winner = i
                    break

                player_chosen = self.current_player.chosen

                if player_chosen != None:
                    self.current = player_chosen
                    self.played.append(self.current)
                    reversed = self.current_player.special_effects(self)

                    if reversed:
                        api("output","reversed")
                        self.clockwise = not self.clockwise
                        self.gen_next_player()

                    if len(self.current_player.hand) == 0:
                        winner = self.current_player
                        break

            elif self.current_player.punished:
                self.current_player.punished = False
                api("output", f"Skipped {self.current_player.name}")

            else:
                raise Exception(f"player status error {player.debug_()}")

            self.current_player = self.next_player
