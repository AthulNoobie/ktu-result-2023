from dash import Dash,html,dcc,dash_table,no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from os.path import join

with open(join("data","id_name.txt"), 'r') as f1, open(join("data","temp.txt"), 'r') as f2:
    ktu_id = f1.readlines()
    name = f2.readlines()
    id_name = dict()
    for i in range(66):
        id_name[ktu_id[i].strip()] = name[i].strip()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='ktu results 2023',update_title='loading...')

with open(join('data','result.csv'), 'r') as f:
    data = f.readlines()

def extract_results(ktu_id_value):
    results = []
    count = 0
    index = 0
    for line in data:
        if 'Course' in line:
            count += 1
            if count == int(ktu_id_value[-2:]):
                student_results = data[index+1:index+6]
                for result in student_results:
                    results.append(result.strip().split(','))
                break 
        index += 1
    return results
class MainApplication:
    def __init__(self,test):
        self.__app = test
        self.set_layout()

    @property
    def app(self):
        return self.__app
    
    def set_layout(self):
        self.app.layout= html.Div([    html.Div(style={'position': 'relative', 'height': '75px', 'width': '100%', 'background-color': '#B1D4E0'}),
    html.P("APJ Abdul Kalam Technological University",
            style={'position': 'absolute', 'left': '40px', 'top': '6px', 'color': 'blue','font-style':'sans-serif','font-size':'14px'}),
    html.Img(src='https://upload.wikimedia.org/wikipedia/en/1/12/APJ_Abdul_Kalam_Technological_University_logo.png',
             alt='ktu logo', style={'width': 'auto', 'position': 'absolute', 'top': '10px', 'left': '15px',
                                    'height': '30px'}),

    html.Div([
        html.Label(["Year: ", html.Span("*", style={'color': 'red'})], style={'font-famil': 'sans-serif'}),
        dcc.Dropdown(id="year",
                     options=[
                         {'label': '2019', 'value': '2019'},
                         {'label': '2020', 'value': '2020'},
                         {'label': '2021', 'value': '2021'},
                         {'label': '2022', 'value': '2022'},
                         {'label': '2023', 'value': '2023'}
                     ],
                     value='2023', style={'width': '139px', 'margin-left': '1px', 'background-color': '#FFFDAF'}),
        html.Div(id='output-year')
    ], style={'position': 'absolute', 'top': '200px', 'display': 'flex', 'align-items': 'center',
              'margin-top': '20px','margin-left':'10px'}),

    html.Div([
        html.Label(['Semester: ', html.Span("*", style={'color': 'red'})], style={'font-family': 'sans-seif', 'font-size': '15px'}),
        dcc.Dropdown(id="sem",
                     options=[
                         {'label': 'S1', 'value': 'S1'},
                         {'label': 'S2', 'value': 'S2'},
                         {'label': 'S3', 'value': 'S3'},
                         {'label': 'S4', 'value': 'S4'},
                         {'label': 'S5', 'value': 'S5'},
                         {'label': 'S6', 'value': 'S6'},
                         {'label': 'S7', 'value': 'S7'},
                         {'label': 'S8', 'value': 'S8'}
                     ],
                     value='S1', style={'width': '110px', 'margin-left': '2px', 'background-color': '#FFFDAF'}),
        html.Div(id='output-sem')
    ], style={'position': 'absolute', 'display': 'flex', 'align-items': 'center',
               'margin-top': '70px','margin-left':'10px'}),

    html.Div([
        html.Label(["KTU ID:", html.Span("*", style={'color': 'red'})], style={'font-family': 'sans-serif', 'font-size': '15px'}),
        dcc.Input(id='ktu_id', style={'background-color': '#FFFDAF', 'width': '135px','margin-left':'1px'})
    ], style={'margin-top': '16px','margin-left':'10px'}),
    
    html.Div([
        dcc.Location(id='url', refresh=False),
        html.Button("Submit", id="submit-button", n_clicks=0, style={'width': '75px'})
    ], style={'position': 'absolute', 'margin-top': '160px', 'margin-left': '77px'}),

    html.Div(id='output-container', style={'margin-top': '200px'}),
    html.Div("contact:support@ktu.ac.in", style={'position': 'absolute', 'top': '40px', 'right': '10px','font-size':'9px','color':'red'}),
    html.Div([
        html.A("|Student|", href="#", style={'color': 'blue', 'margin-right': '2px', 'border': '0px solid black', 'padding': '1px'}),
        html.A("|Exam|", href="#", style={'color': 'blue', 'margin-right': '2px', 'border': '0px solid black', 'padding': '1px'}),
        html.A("|Suraksha|", href="#", style={'color': 'blue', 'margin-right': '2px', 'border': '0px solid black', 'padding': '1px'}),
        html.A("Academics|", href="#", style={'color': 'blue', 'margin-right': '2px', 'border': '0px solid black', 'padding': '1px'}),
        html.A("|Events|", href="#", style={'color': 'blue', 'border': '0px solid black', 'padding': '0px'}),
    ], style={'position': 'absolute', 'top': '50px', 'right': '15px'}),
    html.A("Login", href="https://app.ktu.edu.in/", style={'color': 'blue','top':'0px','right':'4px','position':'absolute'})])

@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('ktu_id', 'value'),
     State('year', 'value'),
     State('sem', 'value')]
)
def update_output(n_clicks, ktu_id_value, year_value, sem_value):
    if n_clicks > 0:
        if ktu_id_value:
            if ktu_id_value in id_name:
                if sem_value == 'S1' and year_value == '2023':
                    student_name = id_name[ktu_id_value]
                    student_results = extract_results(ktu_id_value)
                    if student_results:
                        result_table = dash_table.DataTable(
                            id='result-table',
                            columns=[{'name': 'Course', 'id': 'Course'},
                                     {'name': 'Grade', 'id': 'Grade'},
                                     {'name': 'Credit', 'id': 'Credit'},
                                     {'name': 'Remark', 'id': 'Remark'}],
                            data=[{'Course': result[0], 'Grade': result[1], 'Credit': result[2], 'Remark': result[3]} for result in student_results]
                        )
                        return [f"Student Name: {student_name}", result_table]
                    else:
                        return "No results found for the student"
                else:
                    return "Student not found"
            else:
                return "Student not found"
        else:
            return "Student not found"
    return no_update

@app.callback(
    [Output('ktu_id', 'disabled'),
     Output('year', 'disabled'),
     Output('sem', 'disabled')],
    [Input('submit-button', 'n_clicks')],
)
def disable_inputs(n_clicks):
    if n_clicks > 0:
        return True, True, True
    else:
        return False, False, False

Application = MainApplication(app)
app = Application.app.server

if __name__ == "__main__":
    Application.app.run(port=8080, dev_tools_ui=True, debug=True, host="127.0.0.1")
