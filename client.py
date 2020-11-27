from flask import Flask, redirect, render_template, request, url_for

import config.base
from query_analyzer.queryrunner import QueryRunner
from query_analyzer.utils import clean_up_static_dir

# from sql_parser.main import parse

app = Flask(__name__)
query_runner = QueryRunner()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def explain():
    if request.method == "GET":
        return redirect("/")

    explanation = [
        "Anthony is a google intern",
        "Anthony is a fb intern",
        "Anthony is an apple intern",
    ]

    query = """select
        s_name,
        count(*) as numwait
    from
        supplier,
        lineitem l1,
        orders,
        nation
    where
        s_suppkey = l1.l_suppkey
        and o_orderkey = l1.l_orderkey
        and o_orderstatus = 'F'
        and exists (
            select
                *
            from
                lineitem l2
            where
                l2.l_orderkey = l1.l_orderkey
                and l2.l_suppkey <> l1.l_suppkey
        )
        and not exists (
            select
                *
            from
                lineitem l3
            where
                l3.l_orderkey = l1.l_orderkey
                and l3.l_suppkey <> l1.l_suppkey
                and l3.l_receiptdate > l3.l_commitdate
        )
        and s_nationkey = n_nationkey
        and n_name = 'SAUDI ARABIA'
    group by
        s_name
    order by
        numwait desc,
        s_name"""

    queries = [query, query, query]
    bounds = "12"
    query = queries[0]

    top_plans_by_cost = query_runner.topKplans(
        queries, topK=3, key=lambda x: x.calculate_total_cost()
    )

    graph_file_name = []
    for plan in top_plans_by_cost:
        graph_file_name.append(plan.save_graph_file())

    clean_up_static_dir(graph_file_name)

    html_context = {
        "query": query,
        "explanation": explanation,
        "bounds": bounds,
        "graph_1": graph_file_name[0],
        "graph_2": graph_file_name[1],
        "graph_3": graph_file_name[2],
    }

    return render_template("index.html", **html_context)


@app.route("/test_explain", methods=["GET"])
def test_explain():
    print("test explain endpoint hit")
    query = """select
    s_name,
    count(*) as numwait
from
    supplier,
    lineitem l1,
    orders,
    nation
where
    s_suppkey = l1.l_suppkey
    and o_orderkey = l1.l_orderkey
    and o_orderstatus = 'F'
    and exists (
        select
            *
        from
            lineitem l2
        where
            l2.l_orderkey = l1.l_orderkey
            and l2.l_suppkey <> l1.l_suppkey
    )
    and not exists (
        select
            *
        from
            lineitem l3
        where
            l3.l_orderkey = l1.l_orderkey
            and l3.l_suppkey <> l1.l_suppkey
            and l3.l_receiptdate > l3.l_commitdate
    )
    and s_nationkey = n_nationkey
    and n_name = 'SAUDI ARABIA'
group by
    s_name
order by
    numwait desc,
    s_name"""
    return query_runner.explain(query).root.raw_json


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
