from game import Game
from solvers.heuristic import solve_brute_force

if __name__ == "__main__":
    G = Game(grid_shape=(8, 12), pieces={"C": 32})
    solve_brute_force(G, verbose=False)
