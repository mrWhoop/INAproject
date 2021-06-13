import networkx as nx
from random import choice

wiki = nx.read_pajek('nets/wikispeedia.net')

print(nx.info(wiki))

largest_cc = max(nx.strongly_connected_components(wiki), key=len)

print("--------------------------------")

wikiSub = wiki.subgraph(largest_cc).copy()

print(nx.info(wikiSub))

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
  while S:
    i = S.pop()
    if i == finish:
      path = backtrack(m, start, finish)[::-1]
      exists = path_exists(G, path)
      print(exists)
      return start, end, len(path), path
    for j in nx.neighbors(G, i):
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
        print("Fail", "\n----------------\n")
    else:
        path_lengths.append(pathLength)
        print(pathLength, "\n----------------\n")

avg = sum(path_lengths)/len(path_lengths)
print("average path: " + str(avg))
print("failed: " + str(failed))
