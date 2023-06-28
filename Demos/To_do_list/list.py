
from microdot import Microdot, Response

app = Microdot()
Response.default_content_type = 'text/html'

todos = []

def htmldoc():
    todo_list = ''.join([f'<li>{todo[1]} - <a href="/toggle/{i}">{"Complete" if not todo[0] else "Uncomplete"}</a> - <a href="/delete/{i}">Delete</a></li>' for i, todo in enumerate(todos)])

    return f'''
        <html>
            <head>
                <title>To-Do List</title>
            </head>
            <body>
                <h1>To-Do List</h1>
                <form method="post" action="/add">
                    <label for="task">New Task:</label>
                    <input type="text" id="task" name="task" required>
                    <button type="submit">Add</button>
                </form>
                <ul>
                    {todo_list}
                </ul>
            </body>
        </html>
        '''

@app.route('/', methods=['GET', 'POST'])
def home(request):
    if request.method == 'POST':
        todos.append([False, request.form.get('task')])
    return htmldoc()

@app.route('/add', methods=['POST'])
def add(request):
    todos.append([False, request.form.get('task')])
    return htmldoc()

@app.route('/toggle/<index>')
def toggle(request, index):
    todos[int(index)][0] = not todos[int(index)][0]
    return htmldoc()

@app.route('/delete/<index>')
def delete(request, index):
    todos.pop(int(index))
    return htmldoc()

app.run(debug=True, port=8008)
