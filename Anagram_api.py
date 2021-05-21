import json
import random as r
import flask
from flask import request, render_template, jsonify

letters = "abcdefghijklmnopqrstuvwxyz"
matched_words = []

with open("words_dictionary.json") as f:
    categorized_words = json.load(f)

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def anagram_maker(option, word):
    result = ""
    if option == 1:
        for i in range(1, len(word) + 1):
            if len(word) == 1:
                result += word[0]
            else:
                temp = word[r.randint(1, len(word) - 1)]
                result += temp
                temp_2 = word.replace(temp, "", 1)
                word = temp_2
        result = "The scrambled word is: " + result
        return result
    # elif option == 2:


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        if "option" and "input" in request.form:
            option = int(request.form["option"])
            word = str(request.form["input"])
            if len(word)==0:
                return render_template("index.html", result="There is no input", word="")
            result = anagram_maker(option, word)
            return render_template("index.html", result=result, word="")
        else:
            return render_template("index.html", result="Invalid options,please try again", word="")
    else:
        return render_template("index.html", var="")


@app.route("/api/v1/anagram", methods=["POST", "GET"])
def api():
    if "option" and "input" in request.args:

        if request.method == "GET":
            option = int(request.args["option"])
            word = str(request.args["input"])
            if request.args["option"].isdigit():
                return anagram_maker(option, word)
            else:
                return "Error: the option argument is not a number"
        elif request.method == "POST":
            option = int(request.args["option"])
            word = str(request.args["input"])
            if request.args["option"].isdigit():
                return anagram_maker(option, word)
            else:
                return "Error: the option argument is not a number"
        else:
            return "Error: Incorrect method,please use either post or get"
    else:
        return "Error: The arguments are not provided."


app.run()
