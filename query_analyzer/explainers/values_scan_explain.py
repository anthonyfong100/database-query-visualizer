from query_analyzer.explainers.color import bold_string


def values_scan_explain(query_plan):
    result = f"A {bold_string('values scan')} is done using the given values from the query."
    return result
