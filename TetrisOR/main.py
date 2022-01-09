U = (0, 1)
L = (-1, 0)
R = (1, 0)
D = (0, -1)
DIRECTIONS = [U, R, D, L]

class Node:
    def __init__(self, id):
        self.id = id

    def go(self, direction):
        """Check whether a neighbour exists in this direction"""
        pass

    def get_position(self):
        pass


class Piece:
    def __init__(self, orientation=1):
        self.orientation = orientation
        self.directions = None
        self.assign_neighbours()
        self.set_orientation(orientation)

    def rotate(self, turn):
        """Adjust nodes according to direction of turn.
        Anti-clockwise is -1, clockwise is 1."""
        
        new_directions = {node: {} for node in self.directions}
        for node, neighbours in self.directions.items():
            for neighbour, direction in neighbours.items():
                new_directions[node][neighbour] = (direction + turn) % 4

        self.directions = new_directions
        return self

    def flip(self, dim):
        """Flip piece on a given axis.
        X-axis is 0, Y-axis is 1."""

        if dim == 0:
            flip_map = {0: 2, 1: 1, 2: 0, 3: 3}
        elif dim == 1:
            flip_map = {0: 0, 1: 3, 2: 2, 3: 1}
        else:
            raise ValueError("Only 2 dimensions supported: (0, 1)")

        new_directions = {node: {} for node in self.directions}
        for node, neighbours in self.directions.items():
            for neighbour, direction in neighbours.items():
                new_directions[node][neighbour] = flip_map[direction]

        self.directions = new_directions
        return self

    def assign_neighbours():
        pass

    def set_orientation(self, orientation):
        """Rotate and/or flip piece to the desired orientation.
        
        Note that the orientations are coded so that flipping on the X-axis
        changes between orientations 1 and -1.
        """

        if orientation not in self.valid_orientations:
            raise ValueError(f"Only valid orientations are: " + ", ".join(map(str, self.valid_orientations)))
        
        current = self.orientation
        
        current_flipped = (current < 0)
        target_flipped = (orientation < 0)

        if current_flipped:

            if current_flipped ^ target_flipped:
                self.set_orientation(-1)
                self.flip(0)  # [-1] flipped on X -> [1]
                
                # positive rotation
                for _ in range((orientation - 1) % 4):
                    self.rotate(1)
            
            else:
                # negative rotation
                for _ in range((current - orientation) % 4):
                    self.rotate(1)

        else:

            if current_flipped ^ target_flipped:
                self.set_orientation(1)
                self.flip(0)  # [1] flipped on X -> [-1]
                
                # negative rotation
                for _ in range((-1 - orientation) % 4):
                    self.rotate(1)
            
            else:
                # positive rotation
                for _ in range((orientation - current) % 4):
                    self.rotate(1)

        self.orientation = orientation
        return self


    def print_directions(self):
        """Replace integer directions with letters for a bit more readability."""
        to_print = {node: {} for node in self.directions}
        for node, neighbours in self.directions.items():
            for neighbour, direction in neighbours.items():
                string_map = dict(enumerate(["U", "R", "D", "L"]))
                to_print[node][neighbour] = string_map[direction]
        
        print(to_print)

class Cyan(Piece):
    """Base orientation:
        []
        [][]
    """
    valid_orientations = [1, 2, 3, 4]

    def __init__(self, orientation=1):
        super().__init__(orientation=orientation)
    
    def assign_neighbours(self):
        """Assign directions of neighbours according to base orientation"""
        self.directions = {
            0: {1: 2},
            1: {
                0: 0,
                2: 1
            },
            2: {1: 3}
        }
    

class Orange(Piece):
    """Base orientation:
          [][]            
        [][]
          []
    """
    valid_orientations = [-4, -3, -2, -1, 1, 2, 3, 4]

    def __init__(self, orientation=1):
        super().__init__(orientation=orientation)
    
    def assign_neighbours(self):
        """Assign directions of neighbours according to base orientation"""
        self.directions = {
            0: {1: 3},
            1: {
                0: 1,
                2: 2
            },
            2: {
                1: 0,
                3: 3,
                4: 2
            },
            3: {2: 1},
            4: {2: 0}
        }


from utils import Field, PointIndexed, Point, AdjacencyList

class Grid(PointIndexed):
    def __init__(self, Nx, Ny):
        fields = self._make_list(Nx, Ny)
        super().__init__(fields)

    def _make_list(self, Nx, Ny):
        """Return 2D list of Fields of shape (Nx, Ny)."""
        return [
            [Field((i, j)) for j in range(Ny)]
            for i in range(Nx)
        ]
    
    def place(piece: Piece, at: Point):
        pass

    
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

        R, C = self.shape
        body = ""
        for x in range(R):
            for y in range(C):
                field = self[x, y]
                piece, node_id = field.node
                if piece is not None:
                    if piece not in piece_ids:
                        piece_ids.append(piece)
                        piece_markers[piece] = len(piece_ids) % len(markers)

                    body += f"[{piece_markers[piece]}]"
                else:
                    body += "[ ]"
            
            body += "\n" if x < R-1 else ""

        return "\n".join([header, body])

