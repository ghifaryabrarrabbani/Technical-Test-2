import dash
import pandas as pd
from dash import html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go


### Dataset
link = 'https://raw.githubusercontent.com/ghifaryabrarrabbani/dataset/refs/heads/main/LuxuryLoanPortfolio.csv'
data = pd.read_csv(link, sep=',')

### Appication
app = dash.Dash(__name__)
app.layout = html.Div([  
    html.H1("Luxury Loan Portfolio Dashboard"),
    html.P("This dashboard shows insights on loan balances, payments, and interest rates."),

    dcc.Tabs(id="tabs-example", 
            value='tab-1', 
            children=[
                dcc.Tab(label='Dataset', value='tab-1'),
                dcc.Tab(label='Purpose of Loan Analysis', value='tab-2'),
                dcc.Tab(label='Property Value and Funded Amount Analysis', value='tab-3'),
                dcc.Tab(label='Trend of Interest Rate and Funded Amount Analysis', value='tab-4'),
    ],
    ),
    html.Div(id='tabs-content-example')
])

@app.callback(
    dash.Output('tabs-content-example', 'children'),
    dash.Input('tabs-example', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3("Dataset Preview"),
            dash_table.DataTable(
                data=data.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in data.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
            ),
            html.P("In this dashboard, there are several variables that can be analyze to gain meaningful insights. However, since the task only require 3 charts of analysis, the objective from this dashboard will be:"),
            html.P("- Focusing to determining what items people are taking loan for."),
            html.P("- Determining the LTV ratio on borrowers by funded amount and property value."),
            html.P("- Analysis between the interest rate and funded amount over the years to determining whether interest rates have significant effect oon funded amounts.")
            ])
    elif tab == 'tab-2':
        fig = px.pie(data, names='purpose', title='Purpose Distribution')
        return html.Div([dcc.Graph(figure=fig),
        html.P("Based on the plot, it shows that investment property, home, and commercial property had similar contribute in 31%, where boat only contribute 3.69% and plane only 1.61%."),
        html.P("With that information, it shows that borrower mostly applying luxury loan for primary needs, such as place to stay (home) or business interest.")])
    elif tab == 'tab-3':
        fig = px.scatter(data, x='funded_amount', y='property value', title='Funded Amout vs Property Value analysis')
        return html.Div([dcc.Graph(figure=fig),
        html.P("Based on the plot, it shows that the funded amount has similar value to the property value."),
        html.P('This indicates that the LTV(Loan to Value) ratio is close to 1, meaning the loan covers nearly the entire price of property value.'),
        html.P('With the high LTV, it can increases the lender risk because there is not any equity from the borrower, meaning the borrower can missed the payments and runaway as they have not invested much of their own money into the property.'),
        html.P('To prevent that, the LTV ratio should be lower and implementing the threshold, such as 20%. Moreover, we can also implementing stricter risk mannagement criteria and further analysis needed.')])
    elif tab == 'tab-4':
        data['funded_date'] = pd.to_datetime(data['funded_date'])
        line = data.groupby(data['funded_date'].dt.to_period('M')).agg({
            'interest rate percent': 'mean',
            'funded_amount': "sum"
        }).reset_index()
        line['funded_date'] = line['funded_date'].dt.to_timestamp()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=line['funded_date'],
            y=line['funded_amount'],
            name='Funded Amount',
            yaxis='y1'
        ))
        fig.add_trace(go.Scatter(
            x=line['funded_date'],
            y=line['interest rate percent'],
            name='Interest Rate (%)',
            yaxis='y2'
        ))
        fig.update_layout(
            title='Trend of Interest Rate and Funded Amount per Month',
            xaxis=dict(title='Funded Date'),
            yaxis=dict(title='Funded Amount'),           
            yaxis2=dict(title='Interest Rate (%)', overlaying='y', side='right'),  # kanan
        )

        return html.Div([dcc.Graph(figure=fig),
        html.P("The purpose of the line chart bto determines which to see the trend between funded amount and interest rate."),
        html.P("Most of the time, total funded amount pretty stable, however there are few months with high loan amounts."),
        html.P("The average interest also pretty stable, however there are small adjustments following spikes from funded amount"),
        html.P("With that information, it shows that the interest rate did not have a strong contributon towards the funded amount and further analysis is needed to determine the impactful factor. Moreover, investigating why there was drastic increase in 2019 also can gain more insight in the future.")])

        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
