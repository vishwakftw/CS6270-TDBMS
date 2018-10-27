from ..graph_properties import get_adjacency_matrix, get_absolute_diagonal_degree_matrix

import numpy as np
import networkx as nx
import scipy.sparse as ssp

def pagerank(G, signed=True, symmetric=False, alpha=0.8, max_iter=100):
    """
    Function to get the PageRank centrality scores for each node in a signed network.

    Arguments:
        G : graph to compute PageRank on
        signed : Consider a signed network. Default: True
        symmetric : Consider a symmetric network. Default: False
        alpha : teleportation parameter for PageRank to cover for dangling edges.
                Default: 0.8
        max_iter : maximum number of iterations to perform the power iteration to obtain
                   an approximation of the steady state vector
                   Default: 100

    Returns:
        A dictionary with keys as nodes and values as PageRank values
    """
    # By default, the graph is assumed to be signed and asymmetric
    if not signed:
        for u, v, d in G.edges(data=True):
            w['weight'] = abs(w['weight'])
    if symmetric:
        nodes = list(G.nodes())
        for i in range(len(nodes)):
            for j in range(i, len(nodes)):
                if G.has_edge(nodes[i], nodes[j]):
                    if G.has_edge(nodes[j], nodes[i]):
                        # This happens due to A + A.T
                        G[nodes[i]][nodes[j]]['weight'] += G[nodes[j]][nodes[i]]['weight']
                        G[nodes[j]][nodes[i]]['weight'] += G[nodes[i]][nodes[j]]['weight']
                    else:
                        G.add_edge(nodes[j], nodes[i], weight=G[nodes[i]][nodes[j]]['weight'])

    return nx.link_analysis.pagerank_scipy(G, alpha=alpha, max_iter=max_iter)

def negativerank(G, beta, alpha=0.8, max_iter=100):
    """
    Function to get the Negative rank of a nodes in a graph.
    Negative rank is given by:
        Signed Spectral Rank - eta * Page Rank

    Arguments:
        G : graph to compute PageRank and its variants on
        beta : parameter for Negative Rank
        alpha : teleportation parameter for PageRank to cover for dangling edges.
                Default: 0.8
        max_iter : maximum number of iterations to perform the power iteration to obtain
                   an approximation of the steady state vector
                   Default: 100

    Returns:
        A dictionary with keys as nodes and values as PageRank values
    """
    # PageRank vals
    PR = pagerank(G, alpha=alpha, max_iter=max_iter)
    SR = pagerank(G, signed=True, alpha=alpha, max_iter=max_iter)
    NR = {}
    for key in SR.keys():
        NR[key] = SR[key] - beta * PR[key]
    return NR
