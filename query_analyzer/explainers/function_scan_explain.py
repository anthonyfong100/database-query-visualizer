from color import bold_string


def function_scan_explain(query_plan):
    return "The function {} is run and returns the recordset created by it.".format(
        bold_string(query_plan["Function Name"])
    )


if __name__ == "__main__":
    test_function_scan_plan = {"Function Name": "Test Function"}
    print(function_scan_explain(test_function_scan_plan))
