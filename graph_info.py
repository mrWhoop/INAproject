import networkx as nx
import random

G = nx.read_pajek('nets/wikispeedia.net')

# SIZE
print(f'Size: n = {len(G.nodes())}')

# VOLUME
print(f'Volume: m = {len(G.edges())}')

# MAX INDEGREE
max_node = sorted(G.in_degree, key=lambda x: x[1], reverse=True)[0]
print(f'Maximum indegree: d+_max = {max_node[1]} ({max_node[0]})')

# MAX OUTDEGREE
max_node = sorted(G.out_degree, key=lambda x: x[1], reverse=True)[0]
print(f'Maximum outdegree: d-_max = {max_node[1]} ({max_node[0]})')

# AVERAGE INDEGREE / OUTDEGREE
in_degrees = G.in_degree
in_degrees = [b for a, b in in_degrees]
print(f'Average indegree/outdegree: {sum(in_degrees)/len(in_degrees)}')

# LARGEST CONNECTED COMPONENT
scc = max(nx.strongly_connected_components(G), key=len)

print('----------------------------------')
print('Largest strongly connected component (subgraph):')

print(f'Nodes in largest strongly connected component: {len(scc)}')

G_scc = G.subgraph(scc)

print(f'Volume: m = {len(G_scc.edges())}')

print(f'Average shortest path length: {nx.average_shortest_path_length(G_scc)}')

random_node1 = random.choice(list(G_scc.nodes()))
random_node2 = random.choice(list(G_scc.nodes()))

sp = nx.shortest_path(G_scc, source=random_node1, target=random_node2)
print(' --> '.join(sp))
