from microdot import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc():

    reds     = ["853737","ff6465"]
    yellows  = ["907A4A","ffd782"]
    greens   = ["4E7039","a5eb78"]

    red     =     reds[lights[0]]
    yellow  =  yellows[lights[1]]
    green   =   greens[lights[2]]

    return f'''
        <html>
            <head>
                <title>Francis Traffic Light</title>
            </head>
            <body>
                <div>
                    <h1>Francis's Traffic Light</h1>
                    <svg width="100" height="100" viewBox="0 0 512 512">
                      <path style="fill:#515262" d="M324.683 41.53H187.317c-28.304 0-51.249 22.946-51.249 51.249V460.75c0 28.305 22.946 51.249 51.249 51.249h137.366c28.304 0 51.249-22.946 51.249-51.249V92.779c0-28.303-22.945-51.249-51.249-51.249z"/>
                      <a href="/toggle/0">
                          <circle style="fill:#{red}" cx="255.995" cy="133.818" r="48.281"/>
                      </a>
                      <a href="/toggle/1">
                          <circle style="fill:#{yellow}" cx="255.995" cy="276.765" r="48.281"/>
                      </a>
                      <a href="/toggle/2">
                          <circle style="fill:#{green}" cx="255.995" cy="419.712" r="48.281"/>
                      </a>
                    </svg>
                </div>
            </body>
        </html>
        '''

lights = [0,0,0]

@app.route('/')
def hello(request):
    return htmldoc()


@app.route('/toggle/<light_index>')
def toggle_light(request, light_index):
    light_index = int(light_index)
    lights[light_index] = 1 - lights[light_index]
    return htmldoc()

app.run(debug=True, port=8008)
