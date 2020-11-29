from query_analyzer.explainers.color import bold_string


def nested_loop_explain(query_plan):
    result = f"The join results between the {bold_string('nested loop')} scans of the suboperations are returned as new rows."
    return result
