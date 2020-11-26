from explainers.test_explainer import test_explain
from explainer import Explainer

class Tree:
    def __init__(self, query_plan):
        self.root = TreeNode(query_plan)

    def calculate_total_cost(self):
        return self.calculate_cost(self.root)

    def calculate_cost(self, node):
        cost = node.cost
        for child in node.children: cost+=self.calculate_cost(child)
        return cost

class TreeNode:
    def __init__(self, query_plan):
        self.node_type = query_plan["Node Type"]
        self.cost = query_plan["Total Cost"]
        self.explanation = self.create_explanation(query_plan)
        self.children = self.generate_children(query_plan)

    def generate_children(self, query_plan):
        child_nodes = [TreeNode(child) for child in query_plan["Plans"]]
        return child_nodes

    @staticmethod
    def create_explanation(query_plan):
        node_type = query_plan["Node Type"]
        explainer = Explainer.explainer_map.get(node_type, test_explain)
        return explainer(query_plan)

if __name__ == "__main__":
    test_query_plan = {
        "Node Type": "Test",
        "Total Cost": 10,
        "Plans": [
           {
            "Node Type": "B",
            "Total Cost": 100,
            "Plans": []
           },
           {
            "Node Type": "C",
            "Total Cost": 20,
            "Plans": []
           },
        ]
    }
    tree = Tree(test_query_plan)
    assert tree.root.node_type == test_query_plan["Node Type"]
    assert len(tree.root.children) == len(test_query_plan["Plans"])
    assert tree.root.children[0].node_type == "B"
    assert tree.calculate_total_cost() == 130
    assert tree.root.explanation == "Test"