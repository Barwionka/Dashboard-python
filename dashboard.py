
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Loading the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initializing the Dash app
app = dash.Dash(__name__)

# Setting the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Creating the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Creating the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",
    style={"textAlign": "center", "color": "#503D36", "font-size": 24}
    ),#Include style for title

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[{'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],
            value='Select Statistics',
            placeholder='Select a report type',
            style={
            "width": "80%",
            "padding": "3px",
            "fontSize": "20px",
            "textAlignLast": "center"
        }
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year',
            placeholder = 'Select-year',
            style={
            "width": "80%",
            "padding": "3px",
            "fontSize": "20px",
            "textAlignLast": "center"
        }
        )),

    html.Div([
    html.Div(id='output-container', 
    className='chart-grid', style={"display":"flex"}),])
])


#Creating Callbacks
# Defining the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', 
    component_property='disabled'),
    Input(component_id='dropdown-statistics',
    component_property='value'))

def update_input_container(report_type):
    if report_type =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Defining the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', 
    component_property='children'),
    [Input(component_id='dropdown-statistics',
    component_property='value'), 
    Input(component_id='select-year',
    component_property='value')])


def update_output_container(report_type, selected_year):
    if report_type == 'Recession Period Statistics':
        # Filtering the data for recession periods
        recession_data = data[data['Recession'] == 1]
#Creating and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculating the average number of vehicles sold by vehicle type       
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                 
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Automobile sales depending on vehicle type"))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
                figure=px.pie(exp_rec, 
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type During Recession"
                )
        )
# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data,
        x='unemployment_rate',
        y='Automobile_Sales',
        labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
        title='Effect of Unemployment Rate on Vehicle Type and Sales'))


        return [
             html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],style={'display': 'flex'})
            ]

# Creating and displaying graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots
    # Check for Yearly Statistics.                             
    elif (selected_year and report_type=='Yearly Statistics') :
        yearly_data = data[data['Year'] == selected_year]
                              

                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title = 'Yearly Automobile Sales Trend'))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        mas=data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile Sales'))

  # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)))

    # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data,
                          names='Vehicle_Type',
                          values='Advertising_Expenditure',
                          title=f'Total Advertisement Expenditure by Vehicle Type in {selected_year}'))

#Returning the graphs for displaying Yearly data
        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
        ]
    else:
        return None
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

