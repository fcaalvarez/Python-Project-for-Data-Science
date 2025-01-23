#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from dash import dcc, html
import plotly.express as px
import os
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
#dropdown_options
   # {'label': '...........', 'value': 'Yearly Statistics'},
    #{'label': 'Recession Period Statistics', 'value': '.........'}

# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
#TASK 2.1 Add title to the dashboard
app.layout = html.Div(
    html.H1('Automobile Sales Statistics Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24})
            ,
     #TASK 2.2: Add two dropdown menus
#Dropdown 1 (Statistics)
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    #Dropdown 2 (Years)
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year',
            placeholder='Select-year',
            )
        )),
    
    #TASK 2.3: Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),])


#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'), 
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_report_type):
    if selected_report_type == 'Yearly Statistics':
        return False  # dropdown year on
    else:
        return True  # dropdown year off

@app.callback(
    Output('output-container', 'children'), 
    [Input('dropdown-statistics', 'value'),  
     Input('select-year', 'value')]  
)


#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'), 
        Input(component_id='select-year', component_property='value')
    ]
)

def update_output_container(selected_report_type, selected_year):
    if selected_report_type == 'Recession Period Statistics': # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        

#TASK 2.5: Create and display graphs for Recession Report Statistics
# Plot 1: Automobile sales fluctuation during recession periods
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Fluctuation over Recession Period')
        )

        # Plot 2: Average sales by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type")
        )

        # Plot 3: Advertising expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Expenditure Share by Vehicle Type During Recessions')
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['Vehicle_Type', 'Unemployment_Rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                x='Unemployment_Rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'Unemployment_Rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        # Return the graphs for the recession report
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]
    
    # If the report type is "Yearly Statistics"
    elif report_type == 'Yearly Statistics' and selected_year:
        # Filter the data by the selected year
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly automobile sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales')
        )

        # Plot 2: Total monthly automobile sales
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales')
        )

        # Plot 3: Average vehicles sold in the selected year
        avr_vdata = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                x='Year',
                y='Automobile_Sales',
                title=f'Average Vehicles Sold in the Year {selected_year}')
        )

        # Plot 4: Total advertisement expenditure by vehicle type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle')
        )

        # Return the graphs for the yearly statistics report
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]
    
    # If no valid report type is selected
    return html.Div("Please select a report type and year.")

port=int(os.getenv('PORT', 8060))
# run server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=port)