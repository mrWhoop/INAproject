import networkx as nx
from random import choice
from sentence_transformers import SentenceTransformer
from statistics import median
from sklearn.metrics.pairwise import cosine_similarity

wiki = nx.read_pajek('nets/wikispeedia.net')
print(nx.info(wiki))
largest_cc = max(nx.strongly_connected_components(wiki), key=len)

print("--------------------------------")

wikiSub = wiki.subgraph(largest_cc).copy()
print(nx.info(wikiSub))
#print("Avg. shortest path:", nx.average_shortest_path_length(wikiSub))

model = SentenceTransformer('bert-base-nli-mean-tokens')

def path_exists(G, path):
  for i, j in zip(path, path[1:]):
    if j not in nx.neighbors(G, i):
      return False
  return True

def backtrack(m, i, j):
  r = [j]
  while True:
    if j == i:
      return r
    parent = m[j]
    r.append(parent)
    j = parent

def bfs_nx(G, start, finish, width):
  S = []
  N = set()
  S.append(start)
  m = dict()
  count = 0
  while S:
    i = S.pop(0)
    count += 1
    #print(count)
    if count > 1000:
        print("To much steps!")
        return None, None, None, None

    if i == finish:
      print("Found!")
      path = backtrack(m, start, finish)[::-1]
      print("Path:", path)
      print("Path length:", len(path))
      exists = path_exists(G, path)
      print("Path exists: ", exists)
      print("Step count:", count)
      return start, finish, count, path

    # get current node neighbours
    # neighbors = [n for n in G.neighbors(i)]

    # check if goal (end) is in the neighbourhood
    modelList = list()
    modelList.append(finish.replace("_", " "))
    for j in G.neighbors(i):
        # build sentence list
        # if neighbor not in N:
        if (i, j) not in N:
            modelList.append(j.replace("_", " "))

    # transform words

    if len(modelList) < 2:
        continue

    sentence_embeddings = model.encode(modelList)

    similarityResult = cosine_similarity([sentence_embeddings[0]], sentence_embeddings[1:])

    similarityResult = list(similarityResult[0])
    value_pairs = list(zip(modelList[1:], similarityResult))
    u = sorted(value_pairs, key=lambda x: -x[1])
    promising = [i[0] for i in u][:width]

    for j in promising:
      j = j.replace(" ", "_")
      if (i, j) not in N:
        N.add((i, j))
        S.append(j)
        if j not in m:
            m[j] = i

  print("Empty stack!")
  return None, None, None, None

path_lengths = list()
failed = 0
width = 1
print("width:", width)
for i in range(500):
    print(i)
    start = choice(list(wikiSub.nodes()))
    end = choice(list(wikiSub.nodes()))

    print(start, end)

    strt, ed, pathLength, path = bfs_nx(wikiSub, start, end, width)

    if pathLength is None:
        failed += 1
    else:
        path_lengths.append(pathLength)
    print("\n----------------\n")

avg = sum(path_lengths)/len(path_lengths)
print("\naverage path length: " + str(avg))
print("\nmedian path length: " + str(median(path_lengths)))
print("failed: " + str(failed))