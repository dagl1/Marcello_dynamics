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


class DynamicModel:
    def __init__(self, **kwargs):
        self.app = kwargs.get('app', None)
        if self.app is None:
            raise ValueError("App instance is required.")
        self.initial_frequency_A = kwargs.get('initial_frequency_A', 100)
        self.initial_frequency_B = kwargs.get('initial_frequency_B', 100)
        self.initial_frequency_C = kwargs.get('initial_frequency_C', 100)
        self.max_A_frequency = kwargs.get('max_A_frequency', 1000)
        self.max_B_frequency = kwargs.get('max_B_frequency', 1000)
        self.max_C_frequency = kwargs.get('max_C_frequency', 1000)
        self.max_duration = kwargs.get('max_duration', 1000)
        self.frequency_constant_A_1 = kwargs.get('frequency_constant_A_1', 5)
        self.frequency_constant_A_2 = kwargs.get('frequency_constant_A_2', 25)
        self.frequency_constant_B_1 = kwargs.get('frequency_constant_B_1', 5)
        self.frequency_constant_B_2 = kwargs.get('frequency_constant_B_2', 20)
        self.frequency_constant_C_1 = kwargs.get('frequency_constant_C_1', 10)
        self.frequency_constant_C_2 = kwargs.get('frequency_constant_C_2', 35)
        self.frequency_rule_threshold_A = kwargs.get('frequency_rule_threshold_A', 800)
        self.A_array = np.zeros(self.max_duration*10)
        self.B_array = np.zeros(self.max_duration*10)
        self.C_array = np.zeros(self.max_duration*10)
        self.start()


    def start(self):
        self.frequency_A = self.initial_frequency_A
        self.frequency_B = self.initial_frequency_B
        self.frequency_C = self.initial_frequency_C
        self.A_array[0] = self.frequency_A
        self.B_array[0] = self.frequency_B
        self.C_array[0] = self.frequency_C

    def if_above_max_or_below_zero(self, value, max_value):
        if value > max_value:
            return max_value
        elif value < 0:
            return 0
        else:
            return value

    def update_frequency_A(self):
        self.frequency_A = self.frequency_constant_A_1 + self.frequency_A - (self.frequency_C * self.frequency_constant_A_2 * 0.01)
        self.frequency_A = self.if_above_max_or_below_zero(self.frequency_A, self.max_A_frequency)

    def update_frequency_B(self):
        self.frequency_B = - self.frequency_constant_B_1 + self.frequency_B + (self.frequency_A * self.frequency_constant_B_2 * 0.01)
        if self.frequency_A > self.frequency_rule_threshold_A:
            self.frequency_B = self.frequency_B/10
        self.frequency_B = self.if_above_max_or_below_zero(self.frequency_B, self.max_B_frequency)

    def update_frequency_C(self):
        self.frequency_C = self.frequency_constant_C_1 + self.frequency_C - (self.frequency_B * self.frequency_constant_C_2 * 0.01)
        self.frequency_C = self.if_above_max_or_below_zero(self.frequency_C, self.max_C_frequency)

    def update_arrays(self, iteration):
        self.A_array[iteration] = self.frequency_A
        self.B_array[iteration] = self.frequency_B
        self.C_array[iteration] = self.frequency_C

    def update(self, iteration):
        self.update_frequency_A()
        self.update_frequency_B()
        self.update_frequency_C()
        self.update_arrays(iteration)

    def run(self):
        self.start()
        for i in range(1, self.max_duration):
            self.update(i)
        return self.A_array, self.B_array, self.C_array

