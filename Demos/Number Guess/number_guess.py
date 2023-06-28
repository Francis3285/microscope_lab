from microdot import Microdot, Response
import random

app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc(guesses, message, color):
    return f'''
        <html>
            <head>
                <title>High Low Guessing Game</title>
            </head>
            <body>
                <div>
                    <h1>High Low Guessing Game</h1>
                    <p>{message}</p>
                    <form method="post" action="/">
                        <label for="guess">Guess a number between 1 and 100:</label>
                        <input type="number" name="guess" id="guess" min="1" max="100" required>
                        <button type="submit">Submit</button>
                    </form>
                    <p>Guesses: {guesses}</p>
                    <svg width="100" height="100" viewBox="0 0 512 512">
                        <circle style="fill:#{color}" cx="255.995" cy="255.995" r="200"/>
                    </svg>
                    <form method="post" action="/new_game">
                        <button type="submit">New Game</button>
                    </form>
                </div>
            </body>
        </html>
        '''

random_number = random.randint(1, 100)
guesses = 0

@app.route('/', methods=['GET', 'POST'])
def home(request):
    global random_number, guesses

    if request.method == 'POST':
        guess = int(request.form.get('guess'))

        if guess < random_number:
            message = 'Too low!'
            color = '853737' # Red
        elif guess > random_number:
            message = 'Too high!'
            color = '907A4A' # Yellow
        else:
            message = 'Correct!'
            color = '4E7039' # Green

        guesses += 1

    else:
        message = 'Guess a number between 1 and 100.'
        color = '515262' # Grey

    return htmldoc(guesses, message, color)

@app.route('/new_game', methods=['POST'])
def new_game(request):
    global random_number, guesses
    random_number = random.randint(1, 100)
    guesses = 0
    return htmldoc(guesses, 'Guess a number between 1 and 100.', '515262') # Grey

app.run(debug=True, port=8008)
