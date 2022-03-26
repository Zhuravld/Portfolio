from game import Grid


class SolutionNode:
    """Single node of a solution tree.

    Has the following information:

    Sequence of:
    - pieces placed in order
    - location of each piece
    """

    def __init__(self, piece, point, orientation) -> None:
        self.piece = piece
        self.point = point
        self.orientation = orientation
        self.previous = None

    @property
    def data(self):
        return (self.piece, self.point, self.orientation)


def get_previous_state(node: SolutionNode) -> list:
    """Return the solution at `node` by following
    up the levels of the solution tree."""
    current_node = node
    solution = []
    while current_node.previous is not None:
        current_node = current_node.previous
        solution.append(current_node.data)
    return solution


def prepopulate_grid(grid_shape: tuple([int, int]), pieces: dict, pieces_placed: list):
    """Build a game grid and piece set from a solution state."""
    grid = Grid(*grid_shape)

    pieces_left = pieces.copy()
    for (piece, point, ori) in pieces_placed:
        grid.place(piece(orientation=ori), point)
        pieces_left[piece.code] -= 1

    return grid, pieces_left
