import unittest

from query_analyzer.queryplan import QueryPlan


class TestQueryPlan(unittest.TestCase):
    def setUp(self):
        self.raw_query_nested = {
            "Node Type": "Test",
            "Total Cost": 10,
            "Plans": [
                {
                    "Node Type": "B",
                    "Total Cost": 100,
                    "Plans": [
                        {"Node Type": "D", "Total Cost": 200, "Plans": []}
                    ],
                },
                {"Node Type": "C", "Total Cost": 20, "Plans": []},
            ],
        }
        self.raw_query_single = {
            "Node Type": "Test",
            "Total Cost": 10,
            "Plans": [],
        }
        self.query_plan_nested = QueryPlan(self.raw_query_nested)
        self.query_plan_single = QueryPlan(self.raw_query_single)

    def test_construct_graph(self):
        self.assertEqual(len(self.query_plan_nested.graph.nodes), 4)
        self.assertEqual(len(self.query_plan_nested.graph.edges), 3)

    def test_construct_graph_single_node(self):
        self.assertEqual(len(self.query_plan_single.graph.nodes), 1)
        self.assertEqual(len(self.query_plan_single.graph.edges), 0)

    def calculate_total_cost(self):
        self.assertEqual(self.query_plan_nested.calculate_total_cost(), 330)
        self.assertEqual(self.query_plan_single.calculate_total_cost(), 10)
