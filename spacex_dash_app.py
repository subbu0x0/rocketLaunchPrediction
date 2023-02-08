# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df.groupby(['Launch Site'], as_index=False).first()['Launch Site']

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': launch_sites[0], 'value': launch_sites[0]},
                                    {'label': launch_sites[1], 'value': launch_sites[1]},
                                    {'label': launch_sites[2], 'value': launch_sites[2]},
                                    {'label': launch_sites[3], 'value': launch_sites[3]}
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,max=10000,step=1000,
                                value=[min_payload,max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    [Output(component_id='success-pie-chart',component_property='figure'),
    Output(component_id='success-payload-scatter-chart', component_property='figure')],
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")]
    )
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

def get_pie_chart(entered_site,payload_value):
    filtered_df = spacex_df.groupby(['Launch Site'], as_index=False).agg({'class': ['count', 'sum']})
    filtered_df.columns = ['Launch Site', 'count', 'success']
    filtered_df['fails'] = filtered_df['count'] - filtered_df['success']
    filtered_df.set_index('Launch Site',inplace=True)
    labels = ['Success','Failures']
    if entered_site == 'ALL':
        figure = px.pie(filtered_df, values='success', 
        names=launch_sites, 
        title='Total Successful Launches at all Sites')
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version')
        fig.update_traces(marker={'size': 12})
        fig.update_layout(xaxis=dict(range=payload_value),
        title="Correlation between Payload and Success For All sites")
        return figure,fig
    elif entered_site == launch_sites[0]:
        temp = spacex_df[spacex_df['Launch Site'] ==launch_sites[0]]
        fig = px.scatter(temp, x='Payload Mass (kg)', y='class', color='Booster Version')
        fig.update_traces(marker={'size': 12})
        fig.update_layout(xaxis=dict(range=payload_value),
        title="Correlation between Payload and Success For "+launch_sites[0])
        values = filtered_df.loc[launch_sites[0],['success','fails']]
        figure = px.pie(values=values,names=labels,
        title="Spacex Launch data for "+launch_sites[0])
        return figure,fig
    elif entered_site == launch_sites[1]:
        temp = spacex_df[spacex_df['Launch Site'] ==launch_sites[1]]
        fig = px.scatter(temp, x='Payload Mass (kg)', y='class', color='Booster Version')
        fig.update_traces(marker={'size': 12})
        fig.update_layout(xaxis=dict(range=payload_value),
        title="Correlation between Payload and Success For "+launch_sites[1])
        values = filtered_df.loc[launch_sites[1],['success','fails']]
        figure = px.pie(values=values,names=labels,
        title="Spacex Launch data for "+launch_sites[1])
        return figure,fig
    elif entered_site == launch_sites[2]:
        temp = spacex_df[spacex_df['Launch Site'] ==launch_sites[2]]
        fig = px.scatter(temp, x='Payload Mass (kg)', y='class', color='Booster Version')
        fig.update_traces(marker={'size': 12})
        fig.update_layout(xaxis=dict(range=payload_value),
        title="Correlation between Payload and Success For "+launch_sites[2])
        values = filtered_df.loc[launch_sites[2],['success','fails']]
        figure = px.pie(values=values,names=labels,
        title="Spacex Launch data for "+launch_sites[2])
        return figure,fig
    elif entered_site == launch_sites[3]:
        temp = spacex_df[spacex_df['Launch Site'] ==launch_sites[3]]
        fig = px.scatter(temp, x='Payload Mass (kg)', y='class', color='Booster Version')
        fig.update_traces(marker={'size': 12})
        fig.update_layout(xaxis=dict(range=payload_value),
        title="Correlation between Payload and Success For "+launch_sites[3])
        values = filtered_df.loc[launch_sites[3],['success','fails']]
        figure = px.pie(values=values,names=labels,
        title="Spacex Launch data for "+launch_sites[3])
        return figure,fig
# Run the app
if __name__ == '__main__':
    app.run_server()
