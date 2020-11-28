import os
import time

import matplotlib.pyplot as plt
import networkx as nx
from config.base import project_root
from typing import List
from query_analyzer.explainer import Explainer
from query_analyzer.explainers.test_explain import test_explain
from query_analyzer.utils import get_tree_node_pos


class Node:
    def __init__(self, query_plan):
        self.node_type = query_plan["Node Type"]
        self.cost = query_plan["Total Cost"]
        self.parent_relationship = query_plan.get("Parent Relationship")
        self.relation = query_plan.get("Relation Name")
        self.alias = query_plan.get("Alias")
        self.startup_cost = query_plan.get("Startup Cost")
        self.plan_rows = query_plan.get("Plan Rows")
        self.plan_width = query_plan.get("Plan Width")
        self.filter = query_plan.get("Filter")
        self.raw_json = query_plan
        self.explanation = self.create_explanation(query_plan)

    def __str__(self):
        name_string = f"{self.node_type}\ncost: {self.cost}"
        return name_string

    @staticmethod
    def create_explanation(query_plan):
        node_type = query_plan["Node Type"]
        explainer = Explainer.explainer_map.get(node_type, test_explain)
        return explainer(query_plan)

    def has_children(self):
        return "Plans" in self.raw_json


class QueryPlan:
    """
    A query plan is a directed graph made up of several Nodes
    """

    def __init__(self, query_json):
        self.graph = nx.DiGraph()
        self.root = Node(query_json)
        self._construct_graph(self.root)

    def _construct_graph(self, curr_node):
        self.graph.add_node(curr_node)
        if curr_node.has_children():
            for child in curr_node.raw_json["Plans"]:
                child_node = Node(child)
                self.graph.add_edge(
                    curr_node, child_node
                )  # add both curr_node and child_node if not present in graph
                self._construct_graph(child_node)

    def calculate_total_cost(self):
        return sum([x.cost for x in self.graph.nodes])

    def save_graph_file(self):
        graph_name = f"graph_{str(time.time())}.png"
        filename = os.path.join(project_root, "static", graph_name)
        plot_formatter_position = get_tree_node_pos(self.graph, self.root)
        node_labels = {x: str(x) for x in self.graph.nodes}
        nx.draw(
            self.graph,
            plot_formatter_position,
            with_labels=True,
            labels=node_labels,
            font_size=6,
            node_size=300,
            node_color="skyblue",
            node_shape="s",
            alpha=1,
        )
        plt.savefig(filename)
        return graph_name

    def create_explanation(self, node: Node):
        if not node.has_children:
            return [node.explanation]
        else:
            result = []
            for child in self.graph[node]:
                result += self.create_explanation(child)
            result += [node.explanation]
            return result
