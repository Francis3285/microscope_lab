import numpy as np
from microdot import Microdot, Response
app = Microdot()
Response.default_content_type = 'text/html'

def htmldoc():
    coin_text = 'Heads' if coin_state == 0 else 'Tails'

    return f'''
        <html>
            <head>
                <title>Click to Flip Coin</title>
            </head>
            <body style="background-color:oldlace; padding:25px;">
                <div>
                    <h1>Click Coin to Flip</h1>
                    <svg width = '200' viewBox = '0 0  200 200'>
                        <a href = "/toggle">
                            <circle style = "fill:#A4965B" cx = "100" cy = "100" r = "90"/>
                            <text x = "50%" y="50%" font-size = "30" text-anchor = "middle" dy = ".3em">{coin_text}</text>
                        </a>
                    </svg>
                </div>
            </body>
        </html>
        '''
    return html
coin_state = 0

@app.route('/')
def home(request):
    return htmldoc()
