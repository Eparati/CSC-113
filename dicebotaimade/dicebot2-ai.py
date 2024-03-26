import random
import re
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
    try:
        match = re.match(r'(\d+)d(\d+)([+\-]\d+)?', dice_format)
        if match:
            num_dice = int(match.group(1))
            dice_sides = int(match.group(2))
            modifier = match.group(3)
            rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
            total = sum(rolls)
            if modifier:
                total += int(modifier)
            result = {'rolls': rolls, 'total': total}
            return result, None
        else:
            return None, 'Invalid dice format. Please enter the format as XdY[+/-Z].'
    except Exception as e:
        return None, str(e)

def parse_dice_roll_input(dice_format):
    try:
        num_dice, num_sides = map(int, dice_format.split('d'))
        return num_dice, num_sides
    except:
        return None, None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)