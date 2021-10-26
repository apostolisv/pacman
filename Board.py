from copy import deepcopy


class Board:

    nodes = []

    def __init__(self):
        self.nodes.extend([[''] for _ in range(20)])
        self.create_nodes()
        self.link_nodes()

    def create_nodes(self):
        for i in range(20):
            for j in range(9):
                node = Node(5+35*j, 615-i*29)
                if isinstance(self.nodes[i][-1], Node):
                    self.nodes[i].append(node)
                else:
                    self.nodes[i][0] = node
        for i in range(len(self.nodes)):
            self.nodes[i].extend([deepcopy(node) for node in self.nodes[i][:-1]])

    def link_nodes(self):
        self.link_nodes_horizontally()
        self.link_nodes_vertically()

    def link_nodes_horizontally(self):
        for line in self.nodes:
            for i in range(1, len(line)):
                line[i-1].right = line[i]
                line[i].left = line[i-1]

    def link_nodes_vertically(self):
        for i in range(1, len(self.nodes)):
            for j in range(len(self.nodes[i])):
                self.nodes[i - 1][j].up = self.nodes[i][j]
                self.nodes[i][j].down = self.nodes[i - 1][j]



class Node:

    right = None
    left = None
    down = None
    up = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        x = self.__dict__['x']
        y = self.__dict__['y']
        setattr(result, 'x', deepcopy(x, memodict))
        setattr(result, 'y', deepcopy(y, memodict))
        result.x = 570 - result.x
        return result
