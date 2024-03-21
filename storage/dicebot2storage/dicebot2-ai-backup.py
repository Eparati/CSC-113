import random
from flask import Flask, request, render_template

app = Flask(__name__)

# Initialize an empty list to store items
items = []

# Initialize an empty list to store rolled dice sets and totals
dice_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    show_history = False
    if request.method == 'POST':
        user_input = request.form['dice_format']
        result, error_message = roll_dice(user_input)
        if result is not None:
            if len(dice_history) >= 5:
                dice_history.pop(0)  # Remove the earliest entry if the limit is reached
            dice_history.append(result)
        return render_template("index.html", result=result, dice_format=user_input, items=items, dice_history=dice_history, error_message=error_message, show_history=show_history)
    elif request.method == 'GET':
        show_history = request.args.get('history') == 'true'
        return render_template("index.html", items=items, dice_history=dice_history, error_message=error_message, show_history=show_history)
    return render_template("index.html", items=items, error_message=error_message, show_history=show_history)

def roll_dice(dice_format):
    num_dice, num_sides = parse_dice_roll_input(dice_format)
    if num_dice is None or num_sides is None or num_sides <= 1 or num_dice <= 0:
        return None, "Invalid dice format. Please use format 'xdy' where x is the number of dice and y is the number of sides per die. X must be an integer number greater than 0. Y must be an integer number greater than 1."
    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    total = sum(rolls)
    return {"rolls": rolls, "total": total}, None

def parse_dice_roll_input(dice_format):
    try:
        num_dice, num_sides = map(int, dice_format.split('d'))
        return num_dice, num_sides
    except:
        return None, None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)