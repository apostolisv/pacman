
class Board:

    nodes = []

    def __init__(self):
        self.nodes.extend([[''] for _ in range(20)])
        self.create_nodes()

    def create_nodes(self):
        for j in range(20):
            for i in range(8):
                node = Node(15+35*i, 565 - j * 29)
                if isinstance(self.nodes[j][-1], Node):
                    self.nodes[j][-1].right = node
                    node.left = self.nodes[j][-1]
                self.nodes[j].append(node)


class Node:

    right = None
    left = None
    down = None
    up = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
