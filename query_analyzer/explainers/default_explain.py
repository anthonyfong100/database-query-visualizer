from query_analyzer.explainers.color import bold_string


def default_explain(query_plan):
    return "The {} is performed.".format(bold_string(query_plan["Node Type"]))
