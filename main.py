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


# sliders factory for 6 sliders
# graph that updates when changing slider
# graph is 3 line timeseries plots of simulated data

class DynamicModel:
    def __init__(self, **kwargs):
        self.initial_frequency_A = kwargs.get('initial_frequency_A', 1)
        self.initial_frequency_B = kwargs.get('initial_frequency_B', 1)
        self.initial_frequency_C = kwargs.get('initial_frequency_C', 1)
        self.max_A_frequency = kwargs.get('max_A_frequency', 1000)
        self.max_B_frequency = kwargs.get('max_B_frequency', 1000)
        self.max_C_frequency = kwargs.get('max_C_frequency', 1000)
        self.max_duration = kwargs.get('max_duration', 1000)
        self.A_array = np.zeros(self.max_duration)
        self.B_array = np.zeros(self.max_duration)
        self.C_array = np.zeros(self.max_duration)

    def start(self):
        self.frequency_A = self.initial_frequency_A
        self.frequency_B = self.initial_frequency_B
        self.frequency_C = self.initial_frequency_C
        self.A_array[0] = self.frequency_A
        self.B_array[0] = self.frequency_B
        self.C_array[0] = self.frequency_C

    def update_frequency_A(self):
        self.frequency_A = self.frequency_A - self.frequency_C * 0.4
        if self.frequency_A < 0:
            self.frequency_A = 0

    def update_frequency_B(self):
        self.frequency_B = self.frequency_B - self.frequency_A * 0.4
        if self.frequency_A > 500:
            self.frequency_B = self.frequency_B - self.frequency_A * 0.4
        if self.frequency_B < 0:
            self.frequency_B = 0

    def update_frequency_C(self):
        self.frequency_C = self.frequency_C - self.frequency_B * 0.4
        if self.frequency_C < 0:
            self.frequency_C = 0

    def update_arrays(self, iteration):
        self.A_array[iteration] = self.frequency_A
        self.B_array[iteration] = self.frequency_B
        self.C_array[iteration] = self.frequency_C

    def update(self, iteration):
        self.update_frequency_A()
        self.update_frequency_B()
        self.update_frequency_C()
        self.update_arrays(iteration)

    def run(self, duration):
        self.start()
        for i in range(1, duration):
            self.update(i)
        return self.A_array, self.B_array, self.C_array

    def plot(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=np.arange(self.max_duration), y=self.A_array, mode='lines', name='A'))
        fig.add_trace(go.Scatter(x=np.arange(self.max_duration), y=self.B_array, mode='lines', name='B'))
        fig.add_trace(go.Scatter(x=np.arange(self.max_duration), y=self.C_array, mode='lines', name='C'))
        fig.update_layout(title='Dynamic Model Simulation', xaxis_title='Time', yaxis_title='Frequency')
        return fig


if __name__ == '__main__':
    print("Running main.py")
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    app.title = "Slider Factory Example"

    app.layout = html.Div([
        html.H1("Slider Factory Example"),
        html.Div(id='output-container'),
        html.Div(id='graph-container'),
        html.Div(id='slider-container'),
        html.Button('Submit', id='submit-button', n_clicks=0),
        dcc.Store(id='store-data'),
    ])


    def slider_factory():
        def slider_component(id, min, max, step, value):
            return dcc.Slider(
                id=id,
                min=min,
                max=max,
                step=step,
                value=value,
                marks={i: str(i) for i in range(min, max + 1)},
            )
        return slider_component

