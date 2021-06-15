import networkx as nx
import random

G = nx.read_pajek('nets/wikispeedia.net')
scc = max(nx.strongly_connected_components(G), key=len)

G_scc = G.subgraph(scc)

avg_path = 0
num_iter = 500

for i in range(num_iter):
    print()
    random_node1 = random.choice(list(G_scc.nodes()))
    random_node2 = random.choice(list(G_scc.nodes()))

    print(random_node1, random_node2)

    visited = set()
    stack = []

    visited.add(random_node1)
    stack.append(random_node1)
    path = []
    path.append(random_node1)

    while stack:
        node = stack[-1]
        if random_node2 in list(G_scc.successors(node)):
            path.append(node)
            path.append(random_node2)
            break
        if node not in visited:
            path.append(node)
            visited.add(node)
            rem = True
        successors = list(G_scc.successors(node))
        if successors:
            random.shuffle(successors)

        for next in successors:
            if next not in visited:
                stack.append(next)
                rem = False
                break
        if rem:
            path.append(stack[-1])
            stack.pop()

    print(f"Search length: {len(path)}")
    avg_path += len(path)
print(path)
print(f"Average length: {avg_path/num_iter}")
