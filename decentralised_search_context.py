import networkx as nx
from random import choice
import statistics

# pip install sentence-transformers
from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity


wiki = nx.read_pajek('nets/wikispeedia.net')

print(nx.info(wiki))

largest_cc = max(nx.strongly_connected_components(wiki), key=len)

print("--------------------------------")

wikiSub = wiki.subgraph(largest_cc).copy()

print(nx.info(wikiSub))

model = SentenceTransformer('bert-base-nli-mean-tokens')

def decentralisedSearchModel(start, end, graph, model):
    pathLength = 0
    path = list()
    path.append(start)

    #visitedNodes = set()
    visitedEdges = set()

    currentNode = start

    while True:
        # get current node neighbours
        neighbors = [n for n in graph.neighbors(currentNode)]

        # check if goal (end) is in the neighbourhood
        # also look for highest degree node
        highestNeighbor = neighbors[0]
        modelList = list()
        modelList.append(end.replace("_", " "))
        for neighbor in neighbors:
            if neighbor == end:
                path.append(neighbor)
                pathLength += 1
                return start, end, pathLength, path
            # build sentence list
            # if neighbor not in visitedNodes:
            if (currentNode, neighbor) not in visitedEdges:
                modelList.append(neighbor.replace("_", " "))

        # transform words

        if len(modelList) < 2:
            return None, None, None, None

        sentence_embeddings = model.encode(modelList)

        similarityResult = cosine_similarity([sentence_embeddings[0]], sentence_embeddings[1:])

        similarityResult = list(similarityResult[0])

        max_value = max(similarityResult)
        max_index = similarityResult.index(max_value) + 1

        mostSuitable = modelList[max_index]
        mostSuitable = mostSuitable.replace(" ", "_")

        # move to most suitable neighbour
        pathLength += 1
        path.append(mostSuitable)
        #visitedNodes.add(mostSuitable)
        visitedEdges.add((currentNode, mostSuitable))
        currentNode = mostSuitable

        # print(currentNode)

        if pathLength > 10000:
            return None, None, None, None

path_lengths = list()
failed = 0

for i in range(500):
    print("------")
    print(i)
    start = choice(list(wikiSub.nodes()))
    end = choice(list(wikiSub.nodes()))

    print(start, end)

    strt, ed, pathLength, path = decentralisedSearchModel(start, end, wikiSub, model)

    if pathLength is None:
        failed += 1
        print("failed")
    else:
        path_lengths.append(pathLength)
        print(pathLength)

avg = sum(path_lengths)/len(path_lengths)
print("average path: " + str(avg))
print("failed: " + str(failed))
median = statistics.median(path_lengths)
print("median: " + str(median))

# start = "Southern_Ocean"
# end = "Thrush_(bird)"
#
# print(start, end)
#
# strt, ed, pathLength, path = decentralisedSearchModel(start, end, wikiSub, model)
#
# print(pathLength)
