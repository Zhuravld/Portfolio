from functools import reduce
from pieces import Piece, DIRECTIONS, COLORS
from utils import Field, PointIndexed, Point

class Grid(PointIndexed):
    def __init__(self, Nx, Ny):
        fields = self._make_list(Nx, Ny)
        super().__init__(fields)
        self._pieces = []

    def _make_list(self, Nx, Ny):
        """Return 2D list of Fields of shape (Nx, Ny)."""
        return [
            [Field((i, j)) for j in range(Ny)]
            for i in range(Nx)
        ]
    
    def __getitem__(self, indices):
        for i, ind in enumerate(indices):
            if ind < 0:
                raise IndexError(f"Index {i} out of bounds, value = {ind}")
        return super().__getitem__(indices)

    def check_placement(self, piece: Piece, at: Point) -> dict:
        """Attempt to place a piece with the root node at a point.
        
        Return list of piece nodes that can be successfully placed
        (either entire piece, or empty dict).

        Traverses all nodes in a piece with DFS, and checks
        each node visited against the grid.
        """
        from_point = at
        discovered = {}
        path = {0: [from_point]}
        nodes_to_place = {}
        class PieceFoundException(Exception): pass
        class OutOfBoundsException(Exception): pass

        def visit(node: int) -> bool:
            discovered[node] = True
            for nb, direction in piece.directions[node].items():

                if not discovered.get(nb, False):
                    path[nb] = path[node] + [DIRECTIONS[direction]]
                    path_to_nb = reduce(lambda a, b: a+b, path[nb])
                    try:
                        field = self[path_to_nb]
                    except IndexError:  
                        # print("Nowhere to place piece")
                        raise OutOfBoundsException
                    if field.node[0] is not None:
                        # print(f"Piece found at {path_to_nb}: {field.node[0]}")
                        raise PieceFoundException
                    else:
                        nodes_to_place[nb] = path_to_nb
                        visit(nb)

        field = self[from_point]
        if field.node[0] is not None:
            # print(f"Piece found at {from_point}: {field.node[0]}")
            return {}

        nodes_to_place[0] = from_point
        try:
            visit(0)
            return nodes_to_place
        except (PieceFoundException, OutOfBoundsException):
            return {}

    def place(self, piece: Piece, at: Point) -> bool:
        """Attempt to place a `piece` with the root node `at` a point.
        Return whether placement was successful or not.
        """
        nodes_to_place = self.check_placement(piece=piece, at=at)
        if nodes_to_place:
            for n, path_to_n in nodes_to_place.items():
                self[path_to_n].node = (piece, n)
            self._pieces.append(piece)
            return True

        return False

    def _is_complete(self):
        """Return True iff every field is occupied by a piece."""
        try:
            return self.size == sum(map(
                lambda piece: piece.size,
                self._pieces
            ))
        except:
            return self.size == sum(map(
                    lambda column:
                    sum(map(
                        lambda field:
                        isinstance(field.node[0], Piece),
                        column
                    )),
                    self._wrapped
                ))

    @property
    def pieces(self) -> list:
        return self._pieces
    
    @property
    def size(self) -> int:
        return self.shape[0] * self.shape[1]
    
    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__

        header = "<{}.{} object of shape {} at {}".format(
            module, qualname, self.shape, hex(id(self))
        )

        markers = ['o', 'x', '+', '~', '¤', '*', '#', '@', 'ø', '§', '%', '&']
        piece_ids = []
        piece_markers = {}

        C, R = self.shape
        body = ""
        for y in range(R):
            for x in range(C):
                field = self[x, y]
                piece, _ = field.node
                if piece is not None:
                    if piece not in piece_ids:
                        piece_ids.append(piece)
                        piece_markers[piece] = markers[len(piece_ids) % len(markers)]

                    body += f"[{piece_markers[piece]}]"
                else:
                    body += "[ ]"
            
            body += "\n" if y < R-1 else ""

        return "\n".join([header, body])


class Game:
    def __init__(self, grid_shape: tuple([int, int]), pieces: dict=None) -> None:
        self.grid = Grid(*grid_shape)
        if pieces is None:
            self.n_pieces = self.get_default_pieces()
            self.pieces_left = self.n_pieces.copy()
        else:
            self.n_pieces = pieces
            self.pieces_left = self.n_pieces.copy()
    
    def get_default_pieces(self):
        """Generate library of pieces.
        Currently just hardcodes 2x Cyan pieces.
        """
        return {"C": 2}
    
    def place(self, code: str, at: Point, orientation: int = 1, check=False):
        """Place a piece of type `code` with the root node `at` a point."""
        placed = False
        if self.pieces_left.get(code, 0) > 0:
            piece = self._get_piece(code)(orientation=orientation)
            if check:
                nodes = self.grid.check_placement(piece=piece, at=at)
                placed = any(nodes)
            else:
                placed = self.grid.place(piece=piece, at=at)

            if placed:
                self.pieces_left[code] -= 1
        else:
            print("No more pieces remaining of type:", code)

        return placed
    
    def _get_piece(self, code):
        return next(filter(
            lambda piece: piece.code == code,
            COLORS
        ))