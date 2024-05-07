import random
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/roll_dice")
def roll_dice():
    rolled_number = random.randint(1, 6)  # Generate a random number between 1 and 6

    return jsonify({"rolled_number": rolled_number}) 

@app.route("/reroll", methods=["POST"])
def reroll():
    rolled_number = random.randint(1, 6)  # Generate a new random number between 1 and 6

    return jsonify({"rolled_number": rolled_number})

if __name__ == "__main__":
    app.run()
