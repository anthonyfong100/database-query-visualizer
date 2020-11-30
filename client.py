from flask import Flask, redirect, render_template, request, url_for

import config.base
from query_analyzer.queryrunner import query_runner
from query_analyzer.utils import clean_up_static_dir
from sql_parser.main import parse
from sql_parser.permutate import permutate

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def explain():
    if request.method == "GET":
        return redirect("/")

    query = request.form["queryText"]
    res = parse(query)

    if res["error"]:
        err = "Invalid query. Ensure that no columns with non-numerical data types have the VARY prefix"

        if res["err_msg"]:
            err = res["err_msg"]

        html_context = {
            "query": err,
            "explanation_1": [err],
            "explanation_2": [err],
            "explanation_3": [err],
            "bounds": [err],
        }

        return render_template("index.html", **html_context)

    bounds = res["bounds"]
    queryFormatted = res["query"]
    queries = permutate(bounds, queryFormatted)
    top_plans_by_cost = query_runner.topKplans(
        queries, topK=3, key=lambda x: x.calculate_total_cost()
    )

    graph_file_name = [None for ix in range(3)]
    total_costs = [None for ix in range(3)]
    explanations = [None for ix in range(3)]
    for ix, plan in enumerate(top_plans_by_cost):
        graph_file_name[ix] = plan.save_graph_file()
        explanations[ix] = plan.create_explanation(plan.root)
        total_costs[ix] = int(plan.calculate_total_cost())

    clean_up_static_dir(graph_file_name)

    html_context = {
        "query": query,
        "bounds": bounds,
        "graph_1": graph_file_name[0],
        "graph_2": graph_file_name[1],
        "graph_3": graph_file_name[2],
        "explanation_1": explanations[0],
        "explanation_2": explanations[1],
        "explanation_3": explanations[2],
        "total_cost_1": total_costs[0],
        "total_cost_2": total_costs[1],
        "total_cost_3": total_costs[2],
    }

    return render_template("index.html", **html_context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
