import networkx as nx
from networkx import NetworkXException
import matplotlib.pyplot as plt
from collections import defaultdict

def decompose_edges_by_len(hypergraph):
    decomposed_edges = defaultdict(list)
    for edge in hypergraph['edges']:
        decomposed_edges[len(edge)].append(edge)
    decomposition = {
        'nodes': hypergraph['nodes'],
        'edges': decomposed_edges
    }
    return decomposition


def plot_hypergraph_components(hypergraph):
    decomposed_graph = decompose_edges_by_len(hypergraph)
    decomposed_edges = decomposed_graph['edges']
    nodes = decomposed_graph['nodes']

    n_edge_lengths = len(decomposed_edges)
    
    # Setup multiplot style
    fig, axs = plt.subplots(1, n_edge_lengths, figsize=(5*n_edge_lengths, 5))
    if n_edge_lengths == 1:
        axs = [axs]  # Ugly hack
    for ax in axs:
        ax.axis('off')
    fig.patch.set_facecolor('#003049')

    # For each edge order, make a star expansion (if != 2) and plot it
    for i, edge_order in enumerate(sorted(decomposed_edges)):
        edges = decomposed_edges[edge_order]
        g = nx.DiGraph()
        g.add_nodes_from(nodes)
        if edge_order == 2:
            g.add_edges_from(edges)
        else:
            for edge in edges:
                g.add_node(tuple(edge))
                for node in edge:
                    g.add_edge(node,tuple(edge))

        # I like planar layout, but it cannot be used in general
        try:
            pos = nx.planar_layout(g)
        except NetworkXException:
            pos = nx.spring_layout(g)

        # Plot true nodes in orange, star-expansion edges in red
        extra_nodes = set(g.nodes) - set(nodes)
        nx.draw_networkx_nodes(g, pos, node_size=300, nodelist=nodes, 
                               ax=axs[i], node_color='#f77f00')
        nx.draw_networkx_nodes(g, pos, node_size=150, nodelist=extra_nodes, 
                               ax=axs[i], node_color='#d62828')

        nx.draw_networkx_edges(g, pos, ax=axs[i], edge_color='#eae2b7',
                               connectionstyle='arc3,rad=0.05', arrowstyle='-')

        # Draw labels only for true nodes
        labels = {node: str(node) for node in nodes}
        nx.draw_networkx_labels(g, pos, labels, ax=axs[i])
    plt.show()

new = []
for item in [{1, 2, 25}, {1, 3, 17}, {1, 4, 21}, {1, 20, 5}, {1, 18, 6}, {1, 10, 7}, {8, 1, 22}, {1, 11, 9}, {1, 12, 23}, {16, 1, 13}, {1, 14, 15}, {24, 1, 19}, {2, 3, 7}, {2, 19, 4}, {2, 21, 5}, {16, 2, 6}, {8, 2, 15}, {9, 2, 18}, {2, 10, 14}, {24, 2, 11}, {17, 2, 12}, {2, 13, 23}, {2, 20, 22}, {3, 4, 12}, {11, 3, 5}, {24, 3, 6}, {8, 9, 3}, {10, 3, 21}, {25, 3, 13}, {3, 14, 22}, {3, 20, 15}, {16, 19, 3}, {18, 3, 23}, {13, 4, 5}, {4, 6, 23}, {4, 20, 7}, {8, 4, 14}, {24, 9, 4}, {25, 10, 4}, {17, 11, 4}, {18, 4, 15}, {16, 4, 22}, {8, 5, 6}, {24, 5, 7}, {9, 5, 14}, {10, 18, 5}, {19, 12, 5}, {17, 5, 15}, {16, 25, 5}, {5, 22, 23}, {22, 6, 7}, {9, 12, 6}, {10, 11, 6}, {13, 6, 15}, {25, 6, 14}, {17, 20, 6}, {19, 21, 6}, {8, 16, 7}, {9, 17, 7}, {11, 23, 7}, {18, 12, 7}, {13, 14, 7}, {15, 21, 7}, {25, 19, 7}, {8, 10, 23}, {8, 19, 11}, {8, 12, 13}, {8, 17, 18}, {8, 20, 21}, {8, 24, 25}, {9, 10, 13}, {9, 19, 15}, {16, 9, 20}, {9, 21, 23}, {9, 22, 25}, {10, 12, 22}, {24, 10, 15}, {16, 17, 10}, {10, 19, 20}, {16, 11, 12}, {21, 11, 13}, {18, 11, 14}, {11, 22, 15}, {25, 11, 20}, {12, 20, 14}, {25, 12, 15}, {24, 12, 21}, {17, 19, 13}, {18, 20, 13}, {24, 13, 22}, {16, 21, 14}, {24, 17, 14}, {19, 14, 23}, {16, 23, 15}, {16, 24, 18}, {17, 21, 22}, {17, 25, 23}, {18, 19, 22}, {25, 18, 21}, {24, 20, 23}]:
#for item in [{1, 2, 7}, {1, 3, 5}, {1, 4, 6}, {2, 3, 6}, {2, 4, 5}, {3, 4, 7}, {5, 6, 7}]:
    a, b, c = item
    if 18 in [a, b, c] or 16 in [a, b, c]:
        new.append((a, b, c))


print([set(n) for n in new])

a = {'edges': new, 'nodes': [i for i in range(1, 8)]}

plot_hypergraph_components(a)