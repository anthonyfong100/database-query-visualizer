from query_analyzer.explainers.color import bold_string


def unique_explain(query_plan):
    result = f"Using the sorted data from the sub-operations, a scan is done on each row and only {bold_string('unique')} values are preserved."
    return result
