# Aquaponics System Control Web Application

This is a web application that allows control of an aquaponics system. The application is built using the `Microdot` framework, which is a lightweight web framework for Python. The system state is stored in a CSV file (`state.csv`) using the `pandas` library.

## Setup and Dependencies

Before running the code, make sure you have the following dependencies installed:

- `microdot` library
- `pandas` library

You can install the libraries using pip:

```bash
pip install microdot pandas
```

## Code Explanation

The code begins by importing the necessary modules and creating an instance of the `Microdot` class, which represents the web application. It also sets the default content type to HTML.

```python
from microdot import Microdot, Response
import pandas as pd

app = Microdot()
Response.default_content_type = 'text/html'
```

Next, a CSV file (`state.csv`) is specified as the storage for the system state. The initial state is represented as a DataFrame using the `pandas` library.

```python
CSV_FILE = 'state.csv'

# Initialize the DataFrame
system_df = pd.DataFrame([{
    'water_pump': 'OFF',
    'air_pump': 'OFF',
    'light': 'OFF',
    'water_level': '0',
    'temperature': '0',
    'pH_level': '0',
}])
```

The `load_state_from_csv` function is used to load the system state from the CSV file into the DataFrame.

```python
def load_state_from_csv():
    global system_df
    system_df = pd.read_csv(CSV_FILE)
```

The `save_state_to_csv` function is used to save the current system state from the DataFrame to the CSV file.

```python
def save_state_to_csv():
    system_df.to_csv(CSV_FILE, index=False)
```

The `htmldoc` function generates the HTML content for the web page. It takes the system parameters as input and creates buttons for controlling the system components (water pump, air pump, and light). It also displays the system parameters (water level, temperature, and pH level).

```python
def htmldoc(water_pump_status, air_pump_status, light_status, water_level, temperature, pH_level):
    return f'''
        <html>
            <head>
                <title>Aquaponics System Control</title>
                <style>
                    /* CSS styles */
                </style>
            </head>
            <body>
                <h1>Aquaponics System Control</h1>
                <div class="container">
                    <!-- Buttons for controlling system components -->
                    <a href="/toggle/water_pump">
                        <button class="{water_pump_status}">
                            Water Pump: {water_pump_status}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/air_pump">
                        <button class="{air_pump_status}">
                            Air Pump: {air_pump_status}
                        </button>
                    </a>
                    <br>
                    <a href="/toggle/light">
                        <button class="{light_status}">
                            Light: {light_status}
                        </button>
                    </a>
                    <br><br>
                    <!-- Display system parameters -->
                    <div class="parameter">System Parameters:</div>
                    <ul>
                        <li>Water Level: {water_level}</li>
                        <li>Temperature: {temperature}</li>
                        <li>pH Level: {pH_level}</li>
                    </ul>
                </div>
            </body>
        </html>
    '''
```

The `generate_html_doc function loads the system state from the CSV file, retrieves the data for the system parameters, and generates the HTML document using the `htmldoc` function.

```python
def generate_html_doc():
    load_state_from_csv()
    data = system_df.iloc[0]
    return htmldoc(
        data['water_pump'],
        data['air_pump'],
        data['light'],
        data['water_level'],
        data['temperature'],
        data['pH_level'],
    )
```

The `app.route` decorator is used to define the routes for the web application. The routes specify the URL paths and the corresponding functions that handle the requests.

```python
@app.route('/')
def control(request):
    save_state_to_csv()
    return generate_html_doc()

@app.route('/toggle/<component>')
def toggle(request, component):
    system_df.at[0, component] = 'ON' if system_df.at[0, component] == 'OFF' else 'OFF'
    save_state_to_csv()
    return generate_html_doc()

@app.route('/set_parameter/<parameter>/<value>')
def set_parameter(request, parameter, value):
    system_df.at[0, parameter] = str(value)
    save_state_to_csv()
    return generate_html_doc()
```

- The `'/'` route displays the control interface for the aquaponics system. It saves the current system state to the CSV file and generates the HTML document.
- The `'/toggle/<component>'` route is used to toggle the status of a system component (water pump, air pump, or light). It updates the system state in the DataFrame, saves it to the CSV file, and generates the HTML document.
- The `'/set_parameter/<parameter>/<value>'` route is used to set the value of a system parameter (water level, temperature, or pH level). It updates the system state in the DataFrame, saves it to the CSV file, and generates the HTML document.

Finally, the web application is run on the specified port with debugging enabled.

```python
app.run(debug=True, port=8008)
```

## Usage

To run the application, execute the Python script. The application will start a web server on port 8008.

```bash
python aquaponics_app.py
```

You can then access the web application by opening a web browser and navigating to `http://localhost:8008`. The web page will display the control interface for the aquaponics system, where you can toggle the system components and set the system parameters. The system state will be saved and updated in the CSV file (`state.csv`) accordingly.
