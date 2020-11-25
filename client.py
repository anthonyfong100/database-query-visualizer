import time

from flask import Flask, redirect, render_template, request, url_for

from sql_parser.main import parse

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def explain():
    if request.method == "GET":
        return redirect("/")
    query = request.form["queryText"]
    parse(query)
    time.sleep(2)  # TODO: We can call the query parser here
    explanation = [
        "Anthony is a google intern",
        "Anthony is a fb intern",
        "Anthony is an apple intern",
    ]
    return render_template("index.html", query=query, explanation=explanation)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
