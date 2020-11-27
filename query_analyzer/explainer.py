from query_analyzer.explainers.aggregate_explain import aggregate_explain
from query_analyzer.explainers.test_explain import test_explain
from query_analyzer.explainers.cte_explain import cte_explain
from query_analyzer.explainers.function_scan_explain import function_scan_explain
from query_analyzer.explainers.index_scan_explain import index_scan_explain, index_only_scan_explain
from query_analzyer.explainers.group_explain import group_explain


class Explainer(object):
    # Static Explainer class to store a hashmap of node types to explain functions
    explainer_map = {
        "Aggregate": aggregate_explain,
        "CTE Scan": cte_explain,
        "FunctionScan": function_scan_explain,
        "Group": group_explain,
        "Index Scan": index_scan_explain,
        "Index Only Scan": index_only_scan_explain,
        "Test": test_explain,
    }
