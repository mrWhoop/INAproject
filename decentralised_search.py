import networkx as nx
from random import choice
import statistics

wiki = nx.read_pajek('nets/wikispeedia.net')

print(nx.info(wiki))

largest_cc = max(nx.strongly_connected_components(wiki), key=len)

print("--------------------------------")

wikiSub = wiki.subgraph(largest_cc).copy()

print(nx.info(wikiSub))

start = choice(list(wikiSub.nodes()))
end = choice(list(wikiSub.nodes()))

def decentralisedSearchNode(start, end, graph):
    pathLength = 0
    path = list()
    path.append(start)

    visitedNodes = set()

    currentNode = start

    while True:
        # get current node neighbours
        neighbors = [n for n in graph.neighbors(currentNode)]

        # check if goal (end) is in the neighbourhood
        # also look for highest degree node
        highestNeighbor = neighbors[0]
        for neighbor in neighbors:
            if neighbor == end:
                path.append(neighbor)
                pathLength += 1
                return start, end, pathLength, path
            if graph.degree[highestNeighbor] < graph.degree[neighbor]:
                if neighbor not in visitedNodes:
                    highestNeighbor = neighbor

        # move to highest degree neighbour
        pathLength += 1
        path.append(highestNeighbor)
        visitedNodes.add(highestNeighbor)
        currentNode = highestNeighbor

        if pathLength > 10000:
            return None, None, None, None

def decentralisedSearchEdge(start, end, graph):
    pathLength = 0
    path = list()
    path.append(start)

    visitedEdges = set()

    currentNode = start

    while True:
        # get current node neighbours
        neighbors = [n for n in graph.neighbors(currentNode)]

        # check if goal (end) is in the neighbourhood
        # also look for highest degree node
        highestNeighbor = neighbors[0]
        for neighbor in neighbors:
            if neighbor == end:
                path.append(neighbor)
                pathLength += 1
                return start, end, pathLength, path
            if graph.degree[highestNeighbor] < graph.degree[neighbor]:
                if (currentNode, neighbor) not in visitedEdges:
                    highestNeighbor = neighbor

        # move to highest degree neighbour
        pathLength += 1
        path.append(highestNeighbor)
        visitedEdges.add((currentNode, highestNeighbor))
        currentNode = highestNeighbor

        if pathLength > 10000:
            return None, None, None, None


print("do not traverse the same nodes")

path_lengths = list()
failed = 0

for i in range(500):
    print(i)
    start = choice(list(wikiSub.nodes()))
    end = choice(list(wikiSub.nodes()))

    print(start, end)

    strt, ed, pathLength, path = decentralisedSearchNode(start, end, wikiSub)

    if pathLength is None:
        failed += 1
        print("Fail", "\n----------------\n")
    else:
        path_lengths.append(pathLength)
        print(pathLength, "\n----------------\n")

avg = sum(path_lengths)/len(path_lengths)
print("average path: " + str(avg))
print("failed: " + str(failed))
median = statistics.median(path_lengths)
print("median: " + str(median))

print("do not traverse the same edges")

path_lengths = list()
failed = 0

for i in range(500):
    print(i)
    start = choice(list(wikiSub.nodes()))
    end = choice(list(wikiSub.nodes()))

    print(start, end)

    strt, ed, pathLength, path = decentralisedSearchEdge(start, end, wikiSub)

    if pathLength is None:
        failed += 1
    else:
        path_lengths.append(pathLength)

avg = sum(path_lengths)/len(path_lengths)
print("average path: " + str(avg))
print("failed: " + str(failed))
median = statistics.median(path_lengths)
print("median: " + str(median))
