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
    def __init__(self, query_subplan):
        self.node_type = query_subplan["Node Type"]
        self.cost = query_subplan["Total Cost"]
        self.query_subplan = query_subplan
        self.children = self.generate_children()

    def generate_children(self):
        child_nodes = [TreeNode(child) for child in self.query_subplan["Plans"]]
        return child_nodes


if __name__ == "__main__":
    test_query_plan = {
        "Node Type": "A",
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