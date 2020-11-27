import os
import random
from typing import List

import networkx as nx
from config.base import project_root


def get_tree_node_pos(
    G, root=None, width=1.0, height=1, vert_gap=0.1, vert_loc=0, xcenter=0.5
):

    """
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    """
    if not nx.is_tree(G):
        raise TypeError(
            "cannot use hierarchy_pos on a graph that is not a tree"
        )

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(
                iter(nx.topological_sort(G))
            )  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    path_dict = dict(nx.all_pairs_shortest_path(G))
    max_height = 0
    for value in path_dict.values():
        max_height = max(max_height, len(value))
    vert_gap = height / max_height

    def _hierarchy_pos(
        G,
        root,
        width,
        vert_gap,
        vert_loc,
        xcenter,
        pos=None,
        parent=None,
        min_dx=0.05,
    ):
        """
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        """

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = max(min_dx, width / len(children))
            nextx = xcenter - width / 2 - max(min_dx, dx / 2)
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(
                    G,
                    child,
                    width=dx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc - vert_gap,
                    xcenter=nextx,
                    pos=pos,
                    parent=root,
                )
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def clean_up_static_dir(ignore_list: List[str]):
    static_dir = os.path.join(project_root, "static")
    for filename in os.listdir(static_dir):
        if (
            filename.startswith("graph_") and filename not in ignore_list
        ):  # not to remove other images
            os.remove(os.path.join(static_dir, filename))
