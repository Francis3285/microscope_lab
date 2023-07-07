survival_analysis_procedures = {
    "Dataset": {
        "info": "When undertaking a survival analysis project, it is advisable to discuss the structure of your dataset using the following guidelines.",
        "formats": {
            "Description": "The dataset used for survival analysis.",
            "Source": "The source of the dataset, such as a research study or public data repository.",
            "Variables": "A list of variables (columns) present in the dataset, along with their descriptions.",
            "Target_Variable": "The variable of interest, often representing the event of interest or survival time.",
            "Censoring": "Information about censoring in the dataset, including the type (right, left, interval) and any related variables."
        }
    },
    "Data Preprocessing": {
        "info": "Data processing entails the preparation and transformation of raw data into an appropriate format for analysis. In the context of a survival analysis project, the data processing should adhere to the following format.",
        "formats": {
            "Description": "Steps taken to prepare the dataset for survival analysis.",
            "Missing_Values": "Handling missing values, such as imputation or exclusion.",
            "Feature_Engineering": "Creating new features or transforming existing features based on domain knowledge.",
            "Scaling": "Scaling or normalizing numerical variables, if necessary.",
            "Censoring_Handling": "Dealing with censoring, such as removing censored observations or using appropriate statistical methods."
        }
    },
    "Exploratory Data Analysis": {
        "info": "Exploratory Data Analysis  involves examining and summarizing the main characteristics, patterns, and relationships present in a dataset to gain initial insights and formulate hypotheses. In the context of a survival analysis project, the exploratory data analysis should adhere to the following format.",
        "formats": {
            "Description": "Analyzing and visualizing the dataset to gain insights.",
            "Summary_Statistics": "Calculating summary statistics of the variables, such as mean, median, and percentiles.",
            "Survival_Curves": "Plotting survival curves based on the target variable and relevant covariates.",
            "Hazard_Analysis": "Exploring hazard rates and hazard functions.",
            "Covariate_Analysis": "Investigating the relationship between covariates and survival outcomes."
        }
    },
    "Modeling": {
        "info": "Modeling in a project refers to the process of developing mathematical or statistical representations of real-world phenomena or systems. In the context of a survival analysis project, the modeling should adhere to the following format.",
        "formats": {
            "Description": "Building survival models to predict survival outcomes.",
            "Model_Selection": "Selecting appropriate survival models based on the data and research question (e.g., Cox proportional hazards model, accelerated failure time model).",
            "Covariate_Selection": "Choosing relevant covariates to include in the models.",
            "Model_Fitting": "Fitting the selected models to the data using appropriate estimation methods.",
            "Model_Evaluation": "Evaluating the performance of the models using metrics like concordance index (C-index) or log-likelihood."
        }
    },
    "Model Interpretation": {
        "info": "Model interpretation in a survival analysis project involves understanding the relationships between predictor variables and survival outcomes and it should adhere to the following format",
        "formats": {
            "Description": "Interpreting the results and making inferences.",
            "Hazard_Ratios": "Calculating hazard ratios and their corresponding confidence intervals for the covariates.",
            "Variable_Importance": "Assessing the importance of each covariate in predicting survival outcomes.",
            "Survival_Prediction": "Predicting survival probabilities for new individuals based on the fitted models.",
            "Sensitivity_Analysis": "Performing sensitivity analysis to assess the robustness of the results."
        }
    },
    "Conclusion": {
        "info": "When concluding a project in survival analysis, it is recommended to adhere to the following format.",
        "formats": {
            "Description": "Summarizing the findings and conclusions drawn from the survival analysis project.",
            "Implications": "Discussing the implications of the results in the context of the research question or application domain.",
            "Limitations": "Acknowledging any limitations of the analysis, such as data quality issues or assumptions made in the models.",
            "Future_Work": "Proposing directions for future research or improvements to the analysis.",
            "References": "Citing relevant sources, including research papers, textbooks, or software packages used in the project."
        }
    }
}

from microdot import Microdot, Response
import urllib.parse

app = Microdot()
Response.default_content_type = 'text/html'

current_state = {}

css_style = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #D8D9DA;
    margin: 0;
    padding: 0;
}

h1 {
    color: #283747;
    text-align: center;
    font-size: 20px;
    padding: 20px;
}

a {
    color: #283747;
    text-decoration: none;
}

button {
    display: block;
    width: 200px;
    height: 50px;
    margin: 20px auto;
    background-color: #283747;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
}

button:hover {
    background-color: #2F2F30;
}

.format-box {
    width: 60%;
    margin: 20px auto;
    padding: 20px;
    border-radius: 5px;
    background-color: white;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    text-align: center;
    font-size: 20px;
}
</style>
"""

def present_options(request, info, formats):
    options_html = ''.join(
        f'<a href="/handle_format/{urllib.parse.quote(option)}"><button>{option}</button></a>' for option in formats.keys())
    current_state['current_format'] = formats  # Store the current state
    return f'<h1>{info}</h1><br>{options_html}'

def process_format(request, formats):
    if callable(formats):
        result = formats(request)
    elif isinstance(formats, str):
        result = formats
    elif isinstance(formats, dict):
        if "info" in formats and "formats" in formats:
            result = present_options(request, formats['info'], formats['formats'])
        else:
            result = process_format(request, formats['formats'])
    return f'<div class="format-box">{result}</div>'


@app.route('/')
def begin_procedure(request):
    current_state.clear()
    return css_style + present_options(request, "This dictionary provides a structure for organizing various aspects of a survival analysis project. Each section contains key information and subtopics relevant to that stage of the project.", survival_analysis_procedures)
    
    
    
@app.route('/handle_format/<format>', methods=['GET', 'POST'])
def handle_format_request(request, format):
    format = urllib.parse.unquote(format)
    next_step = current_state['current_format'].get(format)  # Get the actions for the current format
    if next_step:
        return css_style + process_format(request, next_step)



app.run(debug=True, port=8008)
