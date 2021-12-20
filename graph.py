from collections import defaultdict

class Graph():
    """
    this class represents a graph read from the graph text-file

    contains a dictionary of lists of successors
                a dictionary of lists of predecessors
                a dictionary of tuples of nodes (nodeID, nodeType)
    """

    def __init__(self):
        self.successors = defaultdict(list)
        self.predecessors = defaultdict(list)
        self.nodes = defaultdict(tuple)

    def addNode(self, node, info):
        """
        adds a node the graph with it's type
        :param node: nodeID
        :param info: nodeTyoe
        """
        self.nodes[node] = info

    def getNodes(self):
        """
        returns all node's ID
        :return: node IDs
        """
        return self.nodes.keys()

    def getNodePlayerID(self, node):
        """
        returns one node's ID
        :param node: returns one node's ID
        :return: ID of node
        """
        return self.nodes[node]

    def addSuccessor(self, node, successor):
        """
        adds a successor to node
        :param node: node where to add a successor
        :param successor: successor node
        """
        self.successors[node].append(successor)

    def getSuccessors(self, node):
        """
        returns all node's successors
        :param node: the given node
        :return: list of node's successors
        """
        return self.successors[node]

    def addPredecessor(self, node, predecessor):
        """
        adds a predecessor to node
        :param node: node where to add a predecessor
        :param predecessor: predecessor node
        """
        self.predecessors[node].append(predecessor)

    def getPredecessors(self, node):
        """
        returns all node's predecessors
        :param node: the given node
        :return: list of node's predecessors
        """
        return self.predecessors[node]