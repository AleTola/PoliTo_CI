import logging
import argparse
import random

import quarto
from final_agent import my_Agent

class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        # print({x}, {y})
        return y, x


def main():
    agent1 = 0
    agent2 = 0

    num_games = 10
    for i in range(num_games):
        print("*** GAME ", {i+1}, " ***")
        game = quarto.Quarto(1)
        game.set_players((RandomPlayer(game), my_Agent(game)))
        winner = game.run()
        logging.warning(f"main: Winner: player {winner}")
        if(winner == 0):
            agent1 = agent1 + 1
        if(winner == 1):
            agent2 = agent2 + 1

    logging.warning(f"main: Number of wins of Agent 1: {agent1}")
    logging.warning(f"main: Number of wins of Agent 2: {agent2}")
    logging.warning(f"main: Number of ties: {num_games - agent1 - agent2}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()