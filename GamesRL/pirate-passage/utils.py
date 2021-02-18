# from dataclasses import dataclass
#
# @dataclass
class Field:
    """Placeholder object for a single field in the grid.
    It can empty, inaccessible, etc.

    Object should fully describe what's at `self.point`,
    but implement no mechanism for change."""

    def __init__(self, point):
        self.point = point
        self.pirates = []
        self.contains_player = False
        self.player_can_access = True

    def __repr__(self):
        return f"<Field: {self.point}>"


class PointIndexed:
    """Wrapper for multi-dimensional list-like, L.
    Replaces indexing by L[x][y] with L[x, y] instead."""

    def __init__(self, wrapped):
        self._wrapped = wrapped
        self._shape = self._init_shape(wrapped)

    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__

        return "<{}.{} object of shape {} at {}\n{}".format(
            module, qualname, self.shape, hex(id(self)), repr(self._wrapped)
        )

    def __getitem__(self, indices):
        current = self._wrapped
        for index in indices:
            current = current[index]
        return current

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = value

    def _init_shape(self, wrapped):
        """Calculate dimensions of list-like"""
        layer = wrapped
        shape = [len(layer)]

        while True:
            try:
                layer = layer[0]
                shape.append(len(layer))
            except:
                break

        return tuple(shape)


class AdjacencyList:
    """N-dimensional adjacency list. Implements DFS as a method.

    Neighbours are represented by a mapping of node coordinates
    to a `list` of neighbouring node coordinates.

    Option to instantiate directly from 2-dimensional shape alone.
    """

    def __init__(self, grid_shape=None, inaccessible=[]):
        self.neighbours = {}
        if grid_shape is not None:
            self._init_from_grid_shape(grid_shape, inaccessible)

    def are_adjacent(self, v1, v2):
        return v2 in self.neighbours[v1]

    def get_neighbours(self, v):
        return self.neighbours.get(v, [])

    def insert_edge(self, e):
        v1, v2 = e

        if v1 not in self.neighbours.keys():
            self.neighbours[v1] = []
        self.neighbours[v1].append(v2)

        if v2 not in self.neighbours.keys():
            self.neighbours[v2] = []
        self.neighbours[v2].append(v1)

    def depth_first_search(self, end, start):
        """Returns True if end node is reachable from start node."""
        discovered = {}

        def visit(node):
            found = False
            discovered[node] = True

            for nb in self.get_neighbours(node):
                if nb == end:
                    return True
                if not discovered.get(nb, False):
                    found = visit(nb)

            return found

        return visit(start)

    def _init_from_grid_shape(self, grid_shape, inaccessible):
        """Init adjacency list from a rectangular 2D grid of nodes.
        Pass over nodes marked "inaccessible"."""
        if len(grid_shape) != 2:
            raise NotImplementedError("Only 2D grid supported")

        rows, cols = grid_shape

        for r in range(rows):
            for c in range(cols):

                node = (r, c)
                if node not in inaccessible:

                    # Insert row edge, if not in last column
                    if c != cols - 1:
                        node_right = (r, c + 1)
                        if node_right not in inaccessible:
                            self.insert_edge(e=(node, node_right))

                    # Insert column edge, if not in last row
                    if r != rows - 1:
                        node_down = (r + 1, c)
                        if node_down not in inaccessible:
                            self.insert_edge(e=(node, node_down))

def points_adjacent(a, b):
    """Assert that point `a` differs from point `b`
    by -1/1 in row or column direction."""
    row_delta_is_one = (a[0] - b[0]) in (-1, 1)
    col_delta_is_one = (a[1] - b[1]) in (-1, 1)
    xor = row_delta_is_one ^ col_delta_is_one
    return xor