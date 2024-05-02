import random
import re
from flask import Flask, request, render_template

app = Flask(__name__)

dice_history = []
characters = []

@app.route('/', methods=['GET', 'POST'])
def dice_roller():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_character':
            new_character = request.form.get('new_character')
            if new_character:
                characters.append(new_character)
        elif action == 'delete_character':
            delete_character = request.form.get('delete_character')
            if delete_character in characters:
                characters.remove(delete_character)
        else:
            dice_format = request.form.get('dice_format')
            roll_source = request.form.get('roll_source')
            if dice_format and roll_source:
                result, error_message = roll_dice(dice_format, roll_source)
                return render_template('index.html', dice_format=dice_format, result=result, error_message=error_message, dice_history=dice_history, characters=characters)
    return render_template('index.html', dice_history=dice_history, characters=characters)

def roll_dice(dice_format, roll_source):
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
            result = {'rolls': rolls, 'total': total, 'source': roll_source, 'dice_format': dice_format}
            dice_history.append(result)
            return result, None
        else:
            return None, 'Invalid dice format. Please enter the format as XdY[+/-Z].'
    except Exception as e:
        return None, str(e)

if __name__ == '__main__':
    app.run()