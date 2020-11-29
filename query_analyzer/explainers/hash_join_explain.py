from query_analyzer.explainers.color import bold_string


def hash_join_explain(query_plan):
    result = ""
    result += f"The result from previous operation is joined using {bold_string('Hash')} {bold_string(query_plan['Join Type'])} {bold_string('Join')}"
    if "Hash Cond" in query_plan:
        result += " on the condition: {}".format(
            bold_string(query_plan["Hash Cond"].replace("::text", ""))
        )
    result += "."
    return result


if __name__ == "__main__":
    test_hash_join_plan = {
        "Join Type": "Test",
        "Hash Cond": "Test Hash Cond",
    }
    print(hash_join_explain(test_hash_join_plan))
