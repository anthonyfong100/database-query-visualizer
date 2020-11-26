import networkx as nx

from query_analyzer.explainer import Explainer
from query_analyzer.explainers.test_explain import test_explain


class Node:
    def __init__(self, query_plan):
        self.node_type = query_plan["Node Type"]
        self.cost = query_plan["Total Cost"]
        self.raw_json = query_plan
        self.explanation = self.create_explanation(query_plan)

    @staticmethod
    def create_explanation(query_plan):
        node_type = query_plan["Node Type"]
        explainer = Explainer.explainer_map.get(node_type, test_explain)
        return explainer(query_plan)


class QueryPlan:
    """
    A query plan is a directed graph made up of several Node
    """

    def __init__(self, query_json):
        self.graph = nx.DiGraph()
        self.root = Node(query_json)
        self._construct_graph(self.root)

    def _construct_graph(self, curr_node):
        self.graph.add_node(curr_node)
        for child in curr_node.raw_json["Plans"]:
            child_node = Node(child)
            self.graph.add_edge(
                curr_node, child_node
            )  # add both curr_node and child_node
            self._construct_graph(child_node)

    def calculate_total_cost(self):
        return sum([x.cost for x in self.graph.nodes])

    def display_graph(self):
        nx.draw(self.graph, with_labels=True, font_weight="bold")
