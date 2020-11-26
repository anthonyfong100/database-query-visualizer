from explainers.test_explain import test_explain
from explainers.aggregate_explain import aggregate_explain

# Static Explainer class to store a hashmap of node types to explainers
class Explainer(object):
    explainer_map = {
        "Aggregate": aggregate_explain
        "Test": test_explain
    }