from flask import Flask, render_template, session, request
from data import posts


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("main.html", posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
