import networkx as nx

def isolated(G, i):
    for j in G[i]:
        if j != i:
            return False
    return True

def component(G, N, i):
    C = []
    S = []
    N.remove(i)
    S.append(i)
    while S:
        i = S.pop()
        C.append(i)
        for j in G[i]:
            if j in N:
                N.remove(j)
                S.append(j)
    return C

def componentCorrectWay(G, N, i):
    C = set()
    S = []
    N.remove(i)
    S.append(i)
    while S:
        i = S.pop()
        C.add(i)
        for j in G[i][1]:
            if j in N:
                N.remove(j)
                S.append(j)
    return C

def componentReverseWay(G, N, i):
    C = set()
    S = []
    N.remove(i)
    S.append(i)
    while S:
        i = S.pop()
        C.add(i)
        for j in G[i][0]:
            if j in N:
                N.remove(j)
                S.append(j)
    return C

def strongComponents(G):
    C = []
    N = set(range(len(G)))
    ORIG_LEN = len(G)
    while N:
        I = next(iter(N))
        CW = componentCorrectWay(G, N.copy(), I)
        SCC = componentReverseWay(G, CW, I)
        N = N.difference(SCC)
        C.append(SCC)
        print("\rProgress: {:.2f}%".format(100-len(N)/ORIG_LEN*100), end='')
    return C

def components(G):
    C = []
    N = set(range(len(G)))
    while N:
        C.append(component(G, N, next(iter(N))))
    return C

print(nx.number_strongly_connected_components(nx.DiGraph(nx.read_pajek("nets/wikispeedia.net"))))

G, n, m = None, 0, 0
with open("nets/wikispeedia.net", 'r') as file:

    n = int(file.readline().split()[1])
    G = [([],[]) for _ in range(n)]

    for line in file:
        if line.startswith("*"):
            break

    m = 0
    for line in file:
        i, j = (int(x) - 1 for x in line.split()[:2])
        G[i][1].append(j)
        G[j][0].append(i)
        m += 1

# n0, n1, delta = 0, 0, 0
# for i in range(n):
#     if isolated(G, i):
#         n0 += 1
#     elif len(G[i]) == 1:
#         n1 += 1
#     if len(G[i]) > delta:
#         delta = len(G[i])

C = strongComponents(G)

print()
print("{:>10s} | '{:s}'".format('Graph', "Wikispeedia"))
# print("{:>10s} | {:,d} ({:,d}, {:,d})".format('Nodes', n, n0, n1))
print("{:>10s} | {:,d}".format('Edges', m))
# print("{:>10s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, delta))
print("{:>10s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
print("{:>10s} | {:.1f}% ({:,d})".format('LSCC', 100 * max(len(c) for c in C) / n, len(C)))
print()
