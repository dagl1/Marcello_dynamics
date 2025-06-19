### Imports
import os
import sys
import logging
import json
import pandas as pd
from datetime import datetime, timedelta
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dash_table import DataTable
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
import re
import inspect
from back_end import DynamicModel


class FrontEnd:
    def __init__(self, app):
        self.app = app
        self.dynamic_model = DynamicModel(app=self.app)

    def plot(self):
        print("Plotting")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=np.arange(self.dynamic_model.max_duration), y=self.dynamic_model.A_array, mode='lines', name='A'))
        fig.add_trace(go.Scatter(x=np.arange(self.dynamic_model.max_duration), y=self.dynamic_model.B_array, mode='lines', name='B'))
        fig.add_trace(go.Scatter(x=np.arange(self.dynamic_model.max_duration), y=self.dynamic_model.C_array, mode='lines', name='C'))
        fig.update_layout(title='Dynamic Model Simulation', xaxis_title='Time', yaxis_title='Frequency')
        return fig

    def slider_factory(self, app, dict_):
        def create_slider_component(id, min, max, step, value, attribute_name):
            distance = max - min
            amount_of_steps = 15
            marks = {i: str(i) for i in range(min, max + 1, int(distance / amount_of_steps))}
            slider = dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label(f"{attribute_name}"),
                            dcc.Slider(
                                id=id,
                                min=min,
                                max=max,
                                step=step,
                                value=value,
                                marks=marks,
                            ),
                        ],
                        width=12
                    )
                ],
                className="mb-4",
            )
            @app.callback(
                Output('slider-container', 'children', allow_duplicate=True),
                Input(id, 'drag_value'),
                prevent_initial_call=True
            )
            def send_slider_update(value):
                self.dynamic_model.__setattr__(attribute_name, value)
                return value
            return slider

        @app.callback(
            Output('output_graph', 'figure'),
            Input('slider-container', 'children' ),
        )
        def update_graph(slider_values):
            self.dynamic_model.run()
            fig = self.plot()
            print("Updating graph")
            return fig

        slider_components = []
        for key, value in dict_.items():
            slider_component = create_slider_component(
                id=value['id'],
                min=value['min'],
                max=value['max'],
                step=value['step'],
                value=value['value'],
                attribute_name=value['attribute_name']
            )
            slider_components.append(slider_component)

        return slider_components

    def get_formulas(self):
        # get the formula after def and before return inside the update A, B and C functions
        A_lines = inspect.getsourcelines(self.dynamic_model.update_frequency_A)[0]
        B_lines = inspect.getsourcelines(self.dynamic_model.update_frequency_B)[0]
        C_lines = inspect.getsourcelines(self.dynamic_model.update_frequency_C)[0]
        A_formula = [line for line in A_lines if "def" not in line and "return" not in line]
        B_formula = [line for line in B_lines if "def" not in line and "return" not in line]
        C_formula = [line for line in C_lines if "def" not in line and "return" not in line]
        # strip everything before the first equal sign
        A_formula = A_formula[0].split('=')[1].strip()
        B_formula = B_formula[0].split('=')[1].strip()
        C_formula = C_formula[0].split('=')[1].strip()
        frequency_variables = ["self.frequency_A", "self.frequency_B", "self.frequency_C"]

        # fill in the formulas using get attr
        A_formula_values = [
            getattr(self.dynamic_model, string_.split("self.")[1]) for string_ in A_formula.split(' ') if string_.startswith('self.') and string_ not in frequency_variables
        ]
        A_formula_substitutes = [
            "{}" if string_.startswith('self.') and string_ not in frequency_variables else string_ for string_ in A_formula.split(' ')
        ]
        A_formula = " ".join(A_formula_substitutes).format(*A_formula_values)
        A_formula = A_formula.replace("self.", "")

        B_formula_values = [
            getattr(self.dynamic_model, string_.split("self.")[1]) for string_ in B_formula.split(' ') if string_.startswith('self.') and string_ not in frequency_variables
        ]
        B_formula_substitutes = [
            "{}" if string_.startswith('self.') and string_ not in frequency_variables else string_ for string_ in B_formula.split(' ')
        ]
        B_formula = " ".join(B_formula_substitutes).format(*B_formula_values)
        B_formula = B_formula.replace("self.", "")
        C_formula_values = [
            getattr(self.dynamic_model, string_.split("self.")[1]) for string_ in C_formula.split(' ') if string_.startswith('self.') and string_ not in frequency_variables
        ]
        C_formula_substitutes = [
            "{}" if string_.startswith('self.') and string_ not in frequency_variables else string_ for string_ in C_formula.split(' ')
        ]
        C_formula = " ".join(C_formula_substitutes).format(*C_formula_values)
        C_formula = C_formula.replace("self.", "")

        # if a minus sign is before a space and after a space at the beggining of a line and a number, remove the space
        # so - 5 + becomes -5 +
        # only at the start of the line
        match_pattern = re.compile("^- (\d+)")
        # only sub the first match so not the number after
        A_formula = match_pattern.sub(r"-\1", A_formula)
        B_formula = match_pattern.sub(r"-\1", B_formula)
        C_formula = match_pattern.sub(r"-\1", C_formula)

        return A_formula, B_formula, C_formula

    def create_layout(self):
        slider_dict = {
            'start_frequency_A': {"id": "start_frequency_A", "min": 0, "max": 1000, "step": 1, "value": self.dynamic_model.initial_frequency_A, "attribute_name": "initial_frequency_A"},
            'start_frequency_B': {"id": "start_frequency_B", "min": 0, "max": 1000, "step": 1, "value": self.dynamic_model.initial_frequency_B, "attribute_name": "initial_frequency_B"},
            'start_frequency_C': {"id": "start_frequency_C", "min": 0, "max": 1000, "step": 1, "value": self.dynamic_model.initial_frequency_C, "attribute_name": "initial_frequency_C"},
            'frequency_constant_A_1': {"id": "frequency_constant_A_1", "min": 0, "max": 100, "step": 1, "value": self.dynamic_model.frequency_constant_A_1, "attribute_name": "frequency_constant_A_1"},
            'frequency_constant_A_2': {"id": "frequency_constant_A_2", "min": 0, "max": 100, "step": 1, "value": self.dynamic_model.frequency_constant_A_2, "attribute_name": "frequency_constant_A_2"},
            'frequency_constant_B_1': {"id": "frequency_constant_B_1", "min": 0, "max": 100, "step": 1, "value": self.dynamic_model.frequency_constant_B_1, "attribute_name": "frequency_constant_B_1"},
            'frequency_constant_B_2': {"id": "frequency_constant_B_2", "min": 0, "max": 100, "step": 1, "value": self.dynamic_model.frequency_constant_B_2, "attribute_name": "frequency_constant_B_2"},
            'frequency_constant_C_1': {"id": "frequency_constant_C_1", "min": 0, "max": 100, "step": 1, "value": self.dynamic_model.frequency_constant_C_1, "attribute_name": "frequency_constant_C_1"},
            'frequency_constant_C_2': {"id": "frequency_constant_C_2", "min": 0, "max": 100, "step": 1, "value": self.dynamic_model.frequency_constant_C_2, "attribute_name": "frequency_constant_C_2"},
            'frequency_rule_threshold_A': {"id": "frequency_rule_threshold_A", "min": 0, "max": 1000, "step": 1, "value": self.dynamic_model.frequency_rule_threshold_A, "attribute_name": "frequency_rule_threshold_A"},
            'max_A_frequency': {"id": "max_A_frequency", "min": 0, "max": 10000, "step": 1, "value": self.dynamic_model.max_A_frequency, "attribute_name": "max_A_frequency"},
            'max_B_frequency': {"id": "max_B_frequency", "min": 0, "max": 10000, "step": 1, "value": self.dynamic_model.max_B_frequency, "attribute_name": "max_B_frequency"},
            'max_C_frequency': {"id": "max_C_frequency", "min": 0, "max": 10000, "step": 1, "value": self.dynamic_model.max_C_frequency, "attribute_name": "max_C_frequency"},
            'max_duration': {"id": "max_duration", "min": 1, "max": 10000, "step": 1, "value": self.dynamic_model.max_duration, "attribute_name": "max_duration"},
        }

        sliders = self.slider_factory(self.app, slider_dict)
        formula_names = ["Frequency A", "Frequency B", "Frequency C"]
        A_formula, B_formula, C_formula = self.get_formulas()
        formulas = [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(name),
                                    dbc.CardBody(
                                        [
                                            html.P(formula, className="card-text", id=f"{name}_formula"),
                                        ]
                                    ),
                                ],
                                className="mb-4",
                            )
                        ],
                    ),
                ]
            )
            for formula, name in zip([A_formula, B_formula, C_formula], formula_names)
        ]
        def create_formula_callback(formula):
            @self.app.callback(
                Output(f'{formula}_formula', 'children'),
                Input('slider-container', 'children'),
            )
            def update_formula(slider_values):
                print(f"Updating {formula} formula")
                A_formula, B_formula, C_formula = self.get_formulas()
                return A_formula if formula == "Frequency A" else B_formula if formula == "Frequency B" else C_formula
        for formula in formula_names:
            create_formula_callback(formula)

        Container = html.Div([
            html.Div(
                "Placeholder for slider factory",
                id='slider-container',
                style={'display': 'none'}
            ),
            dbc.Row(
                [
                    dbc.Col(
                        sliders
                        , width=6
                    ),
                    dbc.Col(
                        [
                            dbc.Row([
                                # button for saving current settings
                                # upload for loading settings
                                dbc.Col([
                                    dbc.Button("Save Settings", id="save-settings", className="mb-4"),
                                    dcc.Upload(
                                        id='upload-data',
                                        children=dbc.Button("Upload Settings", className="mb-4"),
                                    ),
                                ], width = 3),
                            ]),
                            dbc.Row(
                                [
                                    dcc.Graph(id='output_graph', figure=self.plot()),
                                ],
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        formulas
                                    )
                                ]
                            ),
                        ], width=6
                    )
                ],
                className="mb-4",
            ),
        ])

        @self.app.callback(
            Output('slider-container', 'children', allow_duplicate=True),
            Input('save-settings', 'n_clicks'),
            prevent_initial_call=True
        )

        def save_settings(n_clicks):
            # settings are all slider dict attributes
            if n_clicks is None:
                raise PreventUpdate
            settings = {}
            print(f"Saving settings to settings.json at {os.getcwd()}")
            for slider in slider_dict.values():
                settings[slider['attribute_name']] = getattr(self.dynamic_model, slider['attribute_name'])

            filename = f"settings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(settings, f)
            return n_clicks

        @self.app.callback(
            Output('slider-container', 'children', allow_duplicate=True),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            prevent_initial_call=True
        )
        def load_settings(contents, filename):
            if contents is None:
                raise PreventUpdate
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            settings = json.loads(decoded)
            for key, value in settings.items():
                setattr(self.dynamic_model, key, value)
            for slider in slider_dict.values():
                slider['value'] = getattr(self.dynamic_model, slider['attribute_name'])
            return 1
        return Container
