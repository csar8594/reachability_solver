from collections import defaultdict

class Graph():

    def __init__(self):
        self.successors = defaultdict(list)
        self.predecessors = defaultdict(list)
        self.nodes = defaultdict(tuple)

    def getNodes(self):
        return self.nodes.keys()

    def getNodesDescriptors(self):
        return self.nodes

    def getNodePlayerID(self, node):
        return self.nodes[node]

    def addNode(self, node, info):
        self.nodes[node] = info

    def removeNode(self, node):
        del self.nodes[node]

    def getSuccessors(self, node):
        return self.successors[node]

    def addSuccessor(self, node, successor):
        self.successors[node].append(successor)

    def delSuccessor(self, node, successor):
        self.successors[node].remove(successor)

    def getPredecessors(self, node):
        return self.predecessors[node]

    def addPredecessor(self, node, predecessor):
        #print("PRED")
        self.predecessors[node].append(predecessor)

    def delPredecessor(self, node, predecessor):
        self.predecessors[node].remove(predecessor)

    def __str__(self):
        txt = ""

        for node in self.nodes:
            txt += str(node) + " " + str(self.nodes[node]) + "\n" + str(node) + " -> "
            for succ in self.successors[node]:
                txt += str(succ) + ", "
            txt += "\n"

        return txt