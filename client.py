from flask import Flask, redirect, render_template, request, url_for

from query_analyzer.queryrunner import QueryRunner

from sql_parser.main import findBounds

app = Flask(__name__)
query_runner = QueryRunner()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def explain():
    if request.method == "GET":
        return redirect("/")

    query = request.form["queryText"]
    bounds = findBounds(query)
    print(bounds)
    explanation = [
        "Anthony is a google intern",
        "Anthony is a fb intern",
        "Anthony is an apple intern",
    ]
    return render_template(
        "index.html", query=query, explanation=explanation, bounds=bounds
    )


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
