import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
bees_data= pd.read_csv("Dataset/intro_bees.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Bee Colony Impact Dashboard"),
    
    # Dropdown for selecting the year
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in sorted(bees_data['Year'].unique())],
        value=2019  # default value
    ),

    # Dropdown for selecting the period
    html.Label("Select Period:"),
    dcc.Dropdown(
        id='period-dropdown',
        options=[{'label': period, 'value': period} for period in sorted(bees_data['Period'].unique())],
        value='JAN THRU MAR'  # default value
    ),
    
    # Dropdown for selecting the state
    html.Label("Select State:"),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': state, 'value': state} for state in sorted(bees_data['State'].unique())],
        value='Alabama'  # default value
    ),
    
    # Bar chart
    dcc.Graph(id='bar-chart'),
    
    # Data table
    html.H3("Filtered Data:"),
    dcc.Graph(id='data-table')
])

# Callback to update the bar chart based on the selected year, period, and state
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('data-table', 'figure')],
    [Input('year-dropdown', 'value'),
     Input('period-dropdown', 'value'),
     Input('state-dropdown', 'value')]
)
def update_charts(selected_year, selected_period, selected_state):
    # Filter the data based on the selections
    filtered_data = bees_data[
        (bees_data['Year'] == selected_year) &
        (bees_data['Period'] == selected_period) &
        (bees_data['State'] == selected_state)
    ]
    
    # Bar chart of 'Pct of Colonies Impacted' by 'Affected by'
    bar_fig = px.bar(
        filtered_data, 
        x='Affected by', 
        y='Pct of Colonies Impacted', 
        title=f'Percentage of Colonies Impacted in {selected_state} ({selected_year}, {selected_period})'
    )
    
    # Table of filtered data
    table_fig = px.scatter(filtered_data, x='Affected by', y='Pct of Colonies Impacted')
    
    return bar_fig, table_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
