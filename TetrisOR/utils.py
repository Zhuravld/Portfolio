class Point:
    """Point in 2D space. Supports vector arithmetic"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)
    
    def __iter__(self):
        self.i = 0
        return self
    
    def __next__(self):
        if self.i < 2:
            e = [self.x, self.y][self.i]
            self.i += 1
            return e
        else:
            raise StopIteration


class Field:
    """Placeholder object for a single field in the grid.
    
    Points to a node of a piece, represented as (obj, int)
    where obj = piece instance and int = node id.
    """

    def __init__(self, point: Point):
        self.point = point
        self._node = (None, None)
    
    @property
    def node(self) -> tuple:
        return self._node

    @node.setter
    def node(self, value: tuple):
        self._node = value

    def __repr__(self):
        return f"<{self.point}>"



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
    def shape(self) -> tuple:
        return self._shape

    @shape.setter
    def shape(self, value: tuple):
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

    def depth_first_search(self, start, end, discovered={}):
        """Returns True if end node is reachable from start node."""
        newly_discovered = []

        def visit(node):
            found = False
            discovered[node] = True
            newly_discovered.append(node)

            for nb in self.get_neighbours(node):
                if nb == end:
                    return True
                if not discovered.get(nb, False):
                    found = visit(nb)

            return found

        found = visit(start)
        if end:
            return found
        else:
            return newly_discovered
    
    def find_connected_components(self):
        """Return connected components.
        Call DFS on each node, visit each node once.
        """
        component_ids = {}
        component_count = 0
        discovered = {}
        
        if self.nodes:
            node_list = self.nodes
        else:
            node_list = self.neighbours.keys()

        for node in node_list:
            node_component_id = component_ids.get(node, None)
            if node_component_id is None:
                newly_discovered = self.depth_first_search(start=node, end=None, discovered=discovered)
                for discovered_node in newly_discovered:
                    component_ids[discovered_node] = component_count

                component_count += 1
        
        return self._group_by_value(component_ids)

    def _init_from_grid_shape(self, grid_shape, inaccessible):
        """Init adjacency list from a rectangular 2D grid of nodes.
        Pass over nodes marked "inaccessible"."""
        if len(grid_shape) != 2:
            raise NotImplementedError("Only 2D grid supported")

        self.nodes = []

        rows, cols = grid_shape

        for r in range(rows):
            for c in range(cols):

                node = (r, c)
                if node not in inaccessible:
                    self.nodes.append(node)

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

    def _group_by_value(self, d: dict) -> dict:
        grouped = {}
        for key, value in d.items():
            key_list = grouped.get(value, [])
            if not key_list:
                grouped[value] = key_list
            key_list.append(key)

        return grouped

def points_adjacent(a: Point, b: Point) -> bool:
    """Return whether point `a` differs from point `b`
    by -1 or 1 in row or column direction."""
    row_delta_is_one = (a.x - b.x) in (-1, 1)
    col_delta_is_one = (a.y - b.y) in (-1, 1)
    xor = row_delta_is_one ^ col_delta_is_one
    return xor


def value_is_integer(n) -> bool:
    try:
        f = float(n)
        return f.is_integer()
    except:
        return False