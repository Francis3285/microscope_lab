# To-Do List Web Application

This is a simple web application that allows users to create a to-do list. The application is built using the `Microdot` framework, which is a lightweight web framework for Python.


## Code Explanation

The code begins by importing the necessary modules and creating an instance of the `Microdot` class, which represents the web application.

```python
from microdot import Microdot, Response

app = Microdot()
Response.default_content_type = 'text/html'
```

Next, a list called `todos` is created to store the to-do items.

```python
todos = []
```

The `htmldoc` function generates the HTML content for the web page. It creates an HTML form for adding new tasks and displays the existing tasks in an unordered list.

```python
def htmldoc():
    # Generate the HTML content for the to-do list
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
```

The `app.route` decorator is used to define the routes for the web application. The routes specify the URL paths and the corresponding functions that handle the requests.

```python
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
```

- The `/` route handles both `GET` and `POST` requests. When a `POST` request is made (i.e., submitting the form), a new task is appended to the `todos` list.
- The `/add` route specifically handles `POST` requests and adds a new task to the `todos` list.
- The `/toggle/<index>` route is used to toggle the completion status of a task. It updates the `todos` list by changing the completion status of the specified task.
- The `/delete/<index>` route is used to delete a task. It removes the specified task from the `todos` list.

Finally, the web application is run on the specified port with debugging enabled.

```python
app.run(debug=True, port=8008)
```

## Usage

To run the application, execute the Python script. The application will start a web server on port 8008.

```bash
python todo_app.py
```

You can then access the web application by opening a web browser and navigating to `http://localhost:8008`. The web page will display the to-do list, and you can add, toggle, or delete tasks using the provided links and form.
