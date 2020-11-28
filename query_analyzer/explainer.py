from .explainers.aggregate_explain import aggregate_explain
from .explainers.append_explain import append_explain
from .explainers.cte_explain import cte_explain
from .explainers.function_scan_explain import (
    function_scan_explain,
)
from .explainers.group_explain import group_explain
from .explainers.hash_explain import hash_explain
from .explainers.hash_join_explain import hash_join_explain
from .explainers.index_scan_explain import (
    index_only_scan_explain,
    index_scan_explain,
)
from .explainers.limit_explain import limit_explain
from .explainers.materializer_explain import materialize_explain
from .explainers.merge_join_explain import merge_join_explain
from .explainers.nested_loop_explain import nested_loop_explain
from .explainers.seq_scan_explain import seq_scan_explain
from .explainers.setop_explain import setop_explain
from .explainers.sort_explain import sort_explain
from .explainers.subquery_scan_explain import (
    subquery_scan_explain,
)
from .explainers.test_explain import test_explain
from .explainers.unique_explain import unique_explain
from .explainers.values_scan_explain import values_scan_explain


class Explainer(object):
    # Static Explainer class to store a hashmap of node types to explain functions
    explainer_map = {
        "Aggregate": aggregate_explain,
        "Append": append_explain,
        "CTE Scan": cte_explain,
        "Function Scan": function_scan_explain,
        "Group": group_explain,
        "Index Scan": index_scan_explain,
        "Index Only Scan": index_only_scan_explain,
        "Limit": limit_explain,
        "Materialize": materialize_explain,
        "Unique": unique_explain,
        "Merge Join": merge_join_explain,
        "SetOp": setop_explain,
        "Subquery Scan": subquery_scan_explain,
        "Test": test_explain,
        "Values Scan": values_scan_explain,
        "Seq Scan": seq_scan_explain,
        "Merge Join": merge_join_explain,
        "Nested Loop": nested_loop_explain,
        "Sort": sort_explain,
    }


if __name__ == "__main__":
    print(Explainer.explainer_map)
