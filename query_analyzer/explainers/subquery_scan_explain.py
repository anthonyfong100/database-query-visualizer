from query_analyzer.explainers.color import bold_string


def subquery_scan_explain(query_plan):
    result = f"{bold_string('Subquery scan')} is done on results from sub-operations but there are no changes."
    return result
