def path_exists(l):
  for i, j in zip(l, l[1:]):
    if j not in G[i]:
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


def bfs(G, start, finish):
  S = []
  N = set(range(len(G)))
  N.remove(start)
  S.append(start)
  m = dict()
  v = 0
  while S:
    i = S.pop()
    if i == finish:
      path = backtrack(m, start, finish)[::-1]
      exists = path_exists(path)
      print(exists)
      return path
    for j in G[i]:
      if j in N:
        v += 1
        N.remove(j)
        S.append(j)
        m[j] = i
  print(v)

G, n, m = None, 0, 0
with open("nets/wikispeedia.net", 'r') as file:
  n = int(file.readline().split()[1])
  G = [[] for _ in range(n)]

  for line in file:
    if line.startswith("*"):
      break

  m = 0
  for line in file:
    i, j = (int(x) - 1 for x in line.split()[:2])
    G[i].append(j)
    #G[j].append(i)
    m += 1


print(bfs(G, 525, 888))
print()
print(bfs(G, 211, 4555))
print()
print(bfs(G, 3332, 678))
print()