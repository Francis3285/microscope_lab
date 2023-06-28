from microdot import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc(counter):
    return f'''
        <html>
            <head>
                <title>Counter Demo</title>
            </head>
            <body>
                <div>
                    <h1>Counter: {counter}</h1>
                    <a href="/change/{counter}/1"><button>Increment</button></a>
                    <a href="/change/{counter}/-1"><button>Decrement</button></a>
                </div>
            </body>
        </html>
        '''

@app.route('/')
def home(request):
    return htmldoc(0)

@app.route('/change/<current_counter>/<step>')
def change(request, current_counter, step):
    counter = int(current_counter) + int(step)
    return htmldoc(counter)

app.run(debug=True, port=8008)
