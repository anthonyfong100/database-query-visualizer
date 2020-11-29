from query_analyzer.explainers.color import bold_string


def hash_explain(query_plan):
    result = f"The {bold_string('hash')} function makes a memory {bold_string('hash')} with rows from the source."
    return result
