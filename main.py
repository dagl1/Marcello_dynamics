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
from front_end import FrontEnd
if __name__ == '__main__':
    print("Running main.py")
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    app.title = "Slider Factory Example"

    app.config.suppress_callback_exceptions = True
    full_page = FrontEnd(app)
    app.layout = full_page.create_layout()

    app.run(debug=True)

