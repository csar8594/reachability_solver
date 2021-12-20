import argparse
from collections import defaultdict, deque
from graph import Graph
from graphviz import render

def inputHandler():
    """
    Parses the arguments using argparse
    Sets the target set Z and the path to the graph text file
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("Z", help="The set of goal positions - separate with a comma and no blank space.")
    parser.add_argument("G", help="The input graph in .txt file.")

    return parser.parse_args()


def fileReader(filename):
    """
    Opens the file with the filename passed as a parameter in .txt format and creates a new Graph instance.
    Nodes and edges are added as successor and predecessor to build a full graph.
    :param filename: name of the graph .txt file passed as argument
    :return: the graph
    """
    with open(filename, 'r') as file:
        graph = Graph()

        for line in file:
            lineElements = line.split(" ")

            # add nodes
            node = int(lineElements[0])
            if lineElements[1] == "0":
                # player green = diamond
                graph.addNode(node, 0)
            else:
                # player red = square
                graph.addNode(node, 1)

            # add successors to node and to every successor add the node as predecessor
            for successor in lineElements[2].split(","):
                graph.addSuccessor(node, int(successor))
                graph.addPredecessor(int(successor), node)

    return graph


def exportGraphAsDot(graph, path):
    """
    Text based graph gets exported as .dot file in the current directory
    :param graph: the graph
    :param path: path and filename to the export directory
    """
    with open(path, 'w') as file:
        # define a directed graph in the .dot file
        file.write("digraph G {\n")
        for node in graph.getNodes():
            # add every node with node ID as label to the .dot file and decide on the shape
            # diamond for player green and square for player red
            output = str(node) + "[label=\"" + str(node) + "\""
            if graph.getNodePlayerID(node) == 0:
                output += ",shape=diamond"
            elif graph.getNodePlayerID(node) == 1:
                output += ",shape=square"
            output += "];\n"

            # add every node successor with an arrow transition
            for successor in graph.successors[node]:
                output += str(node) + " -> " + str(successor) + ";\n"

            file.write(output)

        file.write('}')


def exportGraphAsPng(dotfile):
    """
    Exports a given .dot file into a .png file in the current directory
    :param dotfile: the .dot file representing the input graph
    """
    render('dot', 'png', dotfile)


def outgoingEdges(graph):
    """
    Calculates the number of outgoing edges for every red node
    States in the algorithm that we have a counter kv for every red vertex
    :param graph: the graph
    :return: a dictionary containing the vertex ID as key and the number of outgoing edges as value
    """
    numOut = defaultdict(int)

    for node in graph.getNodes():
        if graph.getNodePlayerID(node) == 1:
            numOut[node] = len(graph.getSuccessors(node))

    return numOut


def reachabilitySolver(g, targetSet, playerGreen, playerRed, nodeOut, queue, visited, winRegion, winStrat):
    """

    :param g: the graph
    :param targetSet: target set Z as defined in the algorithm
    :param playerGreen: integer number representing player green diamond (=0)
    :param playerRed: integer number representing player red square (=0)
    :param nodeOut: dictionary representing the kv value for every red node from the algorithm
    :param queue: take and insert nodes to this que while going through the node
    :param visited: a list containing which region has already been checked
    :param winRegion: a list where node IDs get added if a node is a winning region for player green
    :param winStrat: a dictionary where keys are left nodes and values are right nodes
    :return: tuple containing the winning region list and the winning strategy dictionary
    """
    for node in targetSet:
        # first add the nodes from the target set Z to the queue, mark these nodes with player green and add
        # these nodes to player green's winning region
        queue.append(node)
        visited[node] = playerGreen
        winRegion.append(node)

        # if the given node is a green node then all the node's successors are part of the winning strategy
        if g.getNodePlayerID(node) == playerGreen:
            winStrat[node] = g.getSuccessors(node)[0]

    while queue:
        n = queue.popleft()

        for np in g.getPredecessors(n):
            # for every predecessor in the nodes in queue the algorithm checks if this region has already been checked
            # and if it is a green or red node

            # if green:
            # append the predecessors to the queue and to the winRegion
            # set the visited position with player green and add a transition from predecessor to node in the
            # winning strategy
            #
            # if red:
            # decrease kv until kv = 0
            # then add this node to winning region according to the algorithm, set visited to player green and add
            # the successor node to the queue

            if visited[np] == -1:
                if g.getNodePlayerID(np) == playerGreen:
                    queue.append(np)
                    visited[np] = playerGreen
                    winRegion.append(np)
                    winStrat[np] = n

                elif g.getNodePlayerID(np) == playerRed:
                    nodeOut[np] -= 1
                    if nodeOut[np] == 0:
                        queue.append(np)
                        visited[np] = playerGreen
                        winRegion.append(np)

    return (winRegion, winStrat)


def solutionPrinter(sol):
    """
    Prints the winning region and winning strategy in a readable format
    :param sol: tuple containing (winRegion, winStrat)
    """
    winReg = sol[0]
    winStrat = sol[1]
    print("Winning region of player 0: " + str(winReg))
    print("Winning strategy of player 0: ")
    for key, value in winStrat.items():
        print(" " + str(key) + " -> " + str(value))


def main():
    """
    Main function calling
        inputHandler,
        parsing the arguments,
        creating the graph and exporting it,
        calculating the number of successors (outgoing edges) kv of every red node,
        calling the reachabilitySolver and
        printing the result
    """
    args = inputHandler()

    Z = map(int, args.Z.split(","))
    graphFileName = args.G
    G = fileReader(graphFileName)
    exportGraphAsDot(G, "export")
    exportGraphAsPng("export")

    green = 0
    red = 1
    numOut = outgoingEdges(G)
    q = deque()
    visited = defaultdict(lambda: -1)
    winRegion = []
    winStrat = defaultdict(lambda: -1)

    solution = reachabilitySolver(G, Z, green, red, numOut, q, visited, winRegion, winStrat)
    solutionPrinter(solution)


if __name__ == '__main__':
    main()