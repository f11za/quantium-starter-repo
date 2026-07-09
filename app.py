import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# initialize the Dash app
app = Dash(__name__)

# 1. load and sort the formatted data
df = pd.read_csv("formatted_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# 2. create the plotly Line Chart
fig = px.line(
    df, 
    x="date", 
    y="sales", 
    title="Pink Morsel Sales Performance (Over Time)",
    labels={"date": "Date", "sales": "Total Sales ($)"},
    template="plotly_white"
)

# customize line aesthetics to look professional
fig.update_traces(line_color="#6366f1", line_width=2)

# add a vertical reference line for the price increase date (January 15, 2021)
fig.add_vline(
    x="2021-01-15", 
    line_width=2, 
    line_dash="dash", 
    line_color="#ef4444",
    annotation_text="Price Increase (Jan 15, 2021)", 
    annotation_position="top left"
)

# 3. define the HTML Layout of the Dashboard
app.layout = html.Div(
    style={
        "fontFamily": "system-ui, -apple-system, sans-serif", 
        "backgroundColor": "#f8fafc", 
        "padding": "40px", 
        "minHeight": "100vh"
    },
    children=[
        # Executive Header
        html.Div(
            style={"textAlign": "center", "marginBottom": "40px"},
            children=[
                html.H1(
                    "Soul Foods Analytics", 
                    style={"color": "#0f172a", "fontSize": "2.5rem", "fontWeight": "800", "marginBottom": "8px"}
                ),
                html.P(
                    "Pink Morsel Sales Performance Executive Visualizer", 
                    style={"color": "#64748b", "fontSize": "1.1rem", "marginTop": "0"}
                ),
            ]
        ),
        
        # Chart Container Card
        html.Div(
            style={
                "backgroundColor": "#ffffff", 
                "borderRadius": "16px", 
                "padding": "24px", 
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05)"
            },
            children=[
                dcc.Graph(
                    id="sales-line-chart",
                    figure=fig
                )
            ]
        )
    ]
)

# run the server locally
if __name__ == "__main__":
    app.run(debug=True)