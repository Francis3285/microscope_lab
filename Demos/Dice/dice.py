from microdot import Microdot, Response
import random
app = Microdot()
Response.default_content_type = 'text/html'

def random_color():
    return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def htmldoc(dice_faces, background_colors):
    dice_faces_svg = {
        1: '''
            <circle cx="100" cy="100" r="10" fill="black" />
        ''',
        2: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        3: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        4: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        5: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        6: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="100" r="10" fill="black" />
            <circle cx="150" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        '''
    }

    dice_svgs = ''
    for i in range(len(dice_faces)):
        x_offset = 220 * i
        dice_svgs += f'''
            <svg x="{x_offset}" width="200" height="200" viewBox="0 0 200 200">
                <rect x="10" y="10" width="180" height="180" rx="20" ry="20" fill="#{background_colors[i]}" />
                {dice_faces_svg[dice_faces[i]]}
            </svg>
        '''

    return f'''
        <html>
            <head>
                <title>SVG Dice Roll</title>
            </head>
            <body>
                <div>
                    <h1>Click the Buttons to Roll Dice</h1>
                    <div>
                        {dice_svgs}
                    </div>
                    <div>
                        <a href="/roll/1"><button>Roll 1 Dice</button></a>
                        <a href="/roll/2"><button>Roll 2 Dice</button></a>
                        <a href="/roll/3"><button>Roll 3 Dice</button></a>
                        <a href="/roll/4"><button>Roll 4 Dice</button></a>
                        <a href="/roll/5"><button>Roll 5 Dice</button></a>
                        <a href="/roll/6"><button>Roll 6 Dice</button></a>
                    </div>
                </div>
            </body>
        </html>
    '''

@app.route('/')
def home(request):
    return htmldoc([1], ['F0E68C'])

@app.route('/roll/<num_dice>')
def roll_dice(request, num_dice):
    num_dice = int(num_dice)
    dice_faces = [random.randint(1, 6) for _ in range(num_dice)]
    background_colors = [random_color() for _ in range(num_dice)]
    return htmldoc(dice_faces, background_colors)


app.run(debug=True, port=8008)
