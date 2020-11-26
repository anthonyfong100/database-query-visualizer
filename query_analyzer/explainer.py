from explainers.test_explainer import test_explain

# Static Explainer class to store a hashmap of node types to explainers
class Explainer(object):
    explainer_map = {
        # ."Aggregate": aggregate_explain
        "Test": test_explain
    }