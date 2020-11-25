class Tree:
    def __init__(self, query_plan):
        self.root = TreeNode(query_plan)
class TreeNode:
    def __init__(self, query_subplan):
        self.node_type = query_subplan["Node Type"]
        self.query_subplan = query_subplan
        self.child_nodes = self.generate_children()
    def generate_children(self):
        child_nodes = [TreeNode(child) for child in self.query_subplan["Plans"]]
        return child_nodes 


if __name__ == "__main__":
    test_query_plan = {
        "Node Type": "A",
        "Plans": [
           {
            "Node Type": "B",
            "Plans": []
           },
           {
            "Node Type": "C",
            "Plans": []
           },
        ]
    }
    tree = Tree(test_query_plan)
    assert tree.root.node_type == test_query_plan["Node Type"]
    assert len(tree.root.child_nodes) == len(test_query_plan["Plans"])
    assert tree.root.child_nodes[0].node_type == "B"
