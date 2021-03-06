import networkx as nx
from random import choice
from statistics import median

wiki = nx.read_pajek('nets/wikispeedia.net')
print(nx.info(wiki))
largest_cc = max(nx.strongly_connected_components(wiki), key=len)

print("--------------------------------")

wikiSub = wiki.subgraph(largest_cc).copy()
print(nx.info(wikiSub))
#print("Avg. shortest path:", nx.average_shortest_path_length(wikiSub))

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

def bfs_nx(G, start, finish):
  S = []
  N = set(G.nodes())
  N.remove(start)
  S.append(start)
  m = dict()
  v = 0
  count = 0
  while S:
    i = S.pop(0)
    count += 1
    if i == finish:
      path = backtrack(m, start, finish)[::-1]
      print("Path:", path)
      print("Path length:", len(path))
      exists = path_exists(G, path)
      print("Path exists: ", exists)
      print("Step count:", count)
      return start, end, count, path
    for j in G.neighbors(i):
      if j in N:
        v += 1
        N.remove(j)
        S.append(j)
        m[j] = i
  return None, None, None, None

path_lengths = list()
failed = 0

for i in range(500):
    print(i)
    start = choice(list(wikiSub.nodes()))
    end = choice(list(wikiSub.nodes()))

    print(start, end)

    strt, ed, pathLength, path = bfs_nx(wikiSub, start, end)

    if pathLength is None:
        failed += 1
    else:
        path_lengths.append(pathLength)
    print("\n----------------\n")

avg = sum(path_lengths)/len(path_lengths)
print("\naverage path length: " + str(avg))
print("\nmedian path length: " + str(median(path_lengths)))
print("failed: " + str(failed))