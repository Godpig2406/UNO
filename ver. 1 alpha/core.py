import random
import com

class card:
    def __init__(self, uid, special, color, properties, name):
        self.uid = uid
        self.special = special
        self.color = color
        self.properties = properties
        self.name = name

    def change_color(self, player):
        while True:
            line = com.api("input", f"{player.name}, please pick a color (B)lue, (G)reen, (R)ed, (Y)ellow \n").upper()
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


class player:

    def __init__(self, **values):
        self.id = values["id"]
        self.name = values["name"]
        self.punished = values["punished"]
        self.hand = []
        self.neighbors = []
        self.chosen = None
        self.avaliable = None

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
        self.avaliable = playable


    def choose(self, game):
        avaliable_uid = [i.uid for i in self.avaliable]
        self.chosen = None
        while True:
            com.api("output", f"{self.name}'s turn")
            for i in range(len(self.hand)):
                avaliable = ""
                if self.hand[i].uid in avaliable_uid:
                    avaliable = "*"

                com.api("output", f"[{i}]{self.hand[i].name}{avaliable}")

            com.api("output", f"Current card on the table is: {game.current.name}")
            choice = com.api("input", "Choose a Card or (D)raw: ")

            if choice == "":
                continue
            
            elif choice.isnumeric():
                choice = int(choice)
                if choice < len(self.hand) and choice >= 0:

                    if self.hand[choice].uid in avaliable_uid:
                        self.chosen = self.hand[choice]
                        self.hand.pop(choice)
                        break

                    else:
                        com.api("output","Unvalid")
                        continue

                else:
                    com.api("output","Out of range")
                    continue

            elif choice.upper() == "D" or choice.upper() == "+":
                game.deal(self, 1)
                drawed=self.hand[-1]
                if procedures.check_valid(game.current, drawed):
                    a = com.api("input", f"{self.name}, {drawed.name} is playable, (Y/n)")
                    if a=="n" or a=="N" or a == "-":
                        com.api("output","ok")
                        self.chosen = None

                    else:
                        self.chosen = drawed
                        self.hand.pop(-1)
                    
                break

            else:
                com.api("output","input error")
                continue

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
    ancestor_cards=[]
    Used_id=[0]
    def __init__(self, **values): 
        self.status = values["status"]
        self.plr_num = values["plr_num"]
        self.deck = values["deck"]
        self.played = values["played"]
        self.players = values["players"]
        self.clockwise = values["clockwise"]
        self.current_player = values["current_player"]
        self.next_player = values["next_player"]
        self.current = values["current"]
        self.debug = values["debug"]

    def gen_Uid(self):
        while True:
            Uid = random.randint(0, 512)
            if Uid not in self.Used_id:
                self.Used_id.append(Uid)
                break

        return Uid

    def create(self):
        for color in ["RED", "GREEN", "BLUE", "YELLOW"]:
            self.ancestor_cards.append(card(self.gen_Uid(), True, color, "+2", f"{color} +2"))
            self.ancestor_cards.append(card(self.gen_Uid(), True, color, "+2", f"{color} +2"))
            self.ancestor_cards.append(card(self.gen_Uid(), True, color, "skip", f"{color} skip"))
            self.ancestor_cards.append(card(self.gen_Uid(), True, color, "skip", f"{color} skip"))
            self.ancestor_cards.append(card(self.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            self.ancestor_cards.append(card(self.gen_Uid(), True, color, "reverse", f"{color} reverse"))
            self.ancestor_cards.append(card(self.gen_Uid(), True, "black", "+4", "Wild +4"))
            self.ancestor_cards.append(card(self.gen_Uid(), True, "black", "change", "Change color"))
            for num in [str(i) for i in range(10)]:
                self.ancestor_cards.append(card(self.gen_Uid(), False, color, num, f"{color} {num}"))
                self.ancestor_cards.append(card(self.gen_Uid(), False, color, num, f"{color} {num}"))

        self.deck = self.ancestor_cards.copy()
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
                self.status = False
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
        global winner
        while True:
            self.gen_next_player()
            if not self.current_player.punished:
                self.current_player.check_playable(self.current)
                self.current_player.choose(self)
                player_played = self.current_player.chosen

                if isinstance(player_played, card):
                    self.current = player_played
                    self.played.append(self.current)
                    reversed = self.current_player.special_effects(self)

                    if reversed:
                        com.api("output","reversed")
                        self.clockwise = not self.clockwise
                        self.gen_next_player()

                    if len(self.current_player.hand) == 0:
                        winner = self.current_player
                        break


            elif self.current_player.punished:
                self.current_player.punished = False
                com.api("output", f"Skipped {self.current_player.name}")

            else:
                raise Exception(f"player status error {player.debug()}")

            self.current_player = self.next_player

game=procedures(status=True, plr_num=4, deck=None, played=[], players=[], clockwise=True, current_player=None, next_player=None, current=None, debug=False)
game.create()

game.players=[player(id=i+1, name=com.api("input","name: "), punished=False,) for i in range(game.plr_num)]

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

com.api("output",f"{winner.name} wins!!!")

