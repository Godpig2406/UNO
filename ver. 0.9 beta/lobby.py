from core import *

num_player=2

game=procedures([num_player])
game.debug = False
game.create()

game.players.extend([player(i+1, api("input","name: "), False) for i in range(num_player)])

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

print(f"{winner.name} wins!!!")
