from copy import deepcopy
from itertools import chain

class Board:

    nodes = []

    def __init__(self):
        self.nodes.extend([[''] for _ in range(20)])
        self.create_nodes()
        self.link_nodes()

    def create_nodes(self):
        for i in range(20):
            for j in range(9):
                node = Node(13.5+34.5*j, 613-i*29, (i, j))
                if isinstance(self.nodes[i][-1], Node):
                    self.nodes[i].append(node)
                else:
                    self.nodes[i][0] = node
        self.delete_excess_nodes()
        for i in range(len(self.nodes)):
            self.nodes[i].extend([deepcopy(node) for node in self.nodes[i][:-1]])
        self.rearrange_nodes()

    def rearrange_nodes(self):
        for line in self.nodes:
            line[9:] = line[9:][::-1]

    def link_nodes(self):
        self.link_nodes_horizontally()
        self.link_nodes_vertically()
        self.nodes[10][0].left = self.nodes[10][-1]
        self.nodes[10][-1].right = self.nodes[10][0]

    def link_nodes_horizontally(self):
        for line in self.nodes:
            for i in range(1, len(line)):
                if isinstance(line[i-1], Node) and isinstance(line[i], Node):
                    line[i-1].right = line[i]
                    line[i].left = line[i-1]

    def link_nodes_vertically(self):
        for i in range(1, len(self.nodes)):
            for j in range(len(self.nodes[i])):
                if isinstance(self.nodes[i - 1][j], Node) and isinstance(self.nodes[i][j], Node):
                    self.nodes[i - 1][j].up = self.nodes[i][j]
                    self.nodes[i][j].down = self.nodes[i - 1][j]

    def delete_excess_nodes(self):
        self.delete_([[1, chain(range(1, 7), range(8, 9))], [2, range(4, 9, 4)], [3, (0, 2, 4, 6, 7, 8)]])
        self.delete_([[4, [2]], [5, chain(range(1, 3), range(4, 7), [8])], [6, [8]]])
        self.delete_([[7, chain(range(3), [4], range(6, 9))], [8, chain(range(3), [4])]])
        self.delete_([[9, chain(range(3), [4], range(6, 9))], [10, [6]], [11, chain(range(3), [4], range(6, 8))]])
        self.delete_([[12, chain(range(3), [4])], [13, chain(range(3), range(4, 7), [8])]])
        self.delete_([[14, [4, 8]], [15, [1, 2, 4, 6, 7, 8]], [17, [1, 2, 4, 5, 6, 8]], [18, [1, 2, 4, 5, 6, 8]]])
        self.delete_([[19, [8]]])

    def delete_(self, places):
        for place in places:
            index = place[0]
            for column in place[1]:
                self.nodes[index][column] = None

    def __getitem__(self, item):
        return self.nodes[item]

class Node:

    right = None
    left = None
    down = None
    up = None

    def __init__(self, x, y, coords):
        self.x = x
        self.y = y
        self.coords = coords

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        x = self.__dict__['x']
        y = self.__dict__['y']
        setattr(result, 'x', deepcopy(x, memodict))
        setattr(result, 'y', deepcopy(y, memodict))
        result.x = 578 - result.x
        return result
