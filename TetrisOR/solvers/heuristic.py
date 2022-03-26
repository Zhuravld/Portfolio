from itertools import product

from game import Game, Grid
from pieces import COLORS
from utils import Point, AdjacencyList
from solvers.solution import SolutionNode, get_previous_state, prepopulate_grid


def solve_brute_force(G: Game, verbose=False):
    """Brute-force solver, but using simple heuristics.

    The solver generates an adjacency list of the grid graph, and finds all connected components.
    On each recursion, it compares these components against the remaining pieces, based on the size or span of the component.
    If this check fails, it rolls back 1 placement.
    """
    C, R = G.grid.shape

    def get_piece():
        return G._get_piece(next(filter(lambda c: c[1] > 0, G.pieces_left.items()))[0])

    def rollback_to(game: Game, grid_state: tuple([Grid, dict])):
        if grid_state is not None:
            grid, pieces_left = grid_state
            game.grid = grid
            game.pieces_left = pieces_left
            return True
        else:
            return False

    def check_no_space_left(game):
        """Check whether Grid can accomodate any more pieces."""

        def span(node_list):
            """Return the span of the list of nodes; that is, the shape
            of the smallest rectangle that can contain all nodes."""
            xs = []
            ys = []
            for (x, y) in node_list:
                xs.append(x)
                ys.append(y)
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            return (max_x - min_x + 1, max_y - min_y + 1)

        def check_fit_in_span(piece, span):
            """Check whether any possible orientation
            of `piece` would fit in `span`.
            """
            X, Y = span
            no_fit = []
            for piece_span in piece.spans:
                px, py = piece_span
                no_fit.append((px > X or py > Y))

            return not (all(no_fit))

        piece_nodes = []
        C, R = game.grid.shape
        for y in range(R):
            for x in range(C):
                field = game.grid[x, y]
                piece, _ = field.node
                if piece is not None:
                    piece_nodes.append((x, y))
        A = AdjacencyList(grid_shape=game.grid.shape, inaccessible=piece_nodes)
        components = A.find_connected_components()

        pieces_left = [code for code, n in game.pieces_left.items() if n > 0]
        color_codes = {piece.code: piece for piece in COLORS}
        # Try to find a component that won't fit any piece (by n empty nodes)
        for nodes in components.values():
            c_size = len(nodes)
            smallest_piece = min([color_codes[code].size for code in pieces_left])
            if smallest_piece > c_size:
                return True

        # Try to find a piece that won't fit in any empty space (by span)
        for code in pieces_left:
            piece = color_codes[code]
            fit = []
            for nodes in components.values():
                c_span = span(nodes)
                fit.append(check_fit_in_span(piece, c_span))
            if not (any(fit)):
                return True

        return False

    class GridCompleteException(Exception):
        pass

    def place_nth_piece(n, previous_node=None, verbose=verbose):
        """Cycle through all piece positions and orientations.
        If found a valid placement, attempt to place the next piece
        """
        piece = get_piece()
        current_node = previous_node
        placed = False
        if verbose:
            print(f"\nPlacing piece {n}: {piece}")

        no_space_left = check_no_space_left(game=G)
        if not no_space_left:
            for y, x, ori in product(range(R), range(C), piece.valid_orientations):
                placed = G.place(piece.code, at=Point(x, y), orientation=ori)
                if placed:
                    current_node = SolutionNode(
                        piece=piece, point=Point(x, y), orientation=ori
                    )
                    current_node.previous = previous_node
                    if verbose:
                        print(f"Piece placed! {G.pieces_left} pieces left")
                        print(G.grid)

                    if G.grid._is_complete():
                        raise GridCompleteException
                    else:
                        place_nth_piece(n + 1, previous_node=current_node)

        if (not placed) or (no_space_left):
            if verbose:
                if no_space_left:
                    print("No space left")
                print(f"Couldn't place piece {n}. Rolling back to previous state:")
            pieces_placed = get_previous_state(current_node)
            old_state = prepopulate_grid(G.grid.shape, G.n_pieces, pieces_placed)
            rollback_to(game=G, grid_state=old_state)

    try:
        place_nth_piece(n=0)
    except GridCompleteException:
        print("Grid complete!")
        print(G.grid)
    except Exception as e:
        print(e)
