from game import Game
from pieces import *
from solvers.heuristic import solve_brute_force

if __name__ == "__main__":

    G = Game(grid_shape=(5,3), pieces={
        piece.code: 1
        for piece in [MintGreen, EmeraldGreen, Yellow]
    })

    solve_brute_force(G, verbose=True)