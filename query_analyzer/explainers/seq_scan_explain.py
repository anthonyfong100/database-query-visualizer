def seq_scan_explain(query_plan):
    sentence = "It does a sequential scan on relation "
    if "Relation Name" in query_plan:
        sentence += query_plan['Relation Name']
    if "Alias" in query_plan:
        if query_plan['Relation Name'] != query_plan['Alias']:
            sentence += " with an alias of {}".format(query_plan['Alias'])
    if "Filter" in query_plan:
        sentence += " and filtered with the condition {}".format(query_plan['Filter'].replace("::text", ""))
    sentence += "."

    return sentence