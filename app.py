import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

# initialize the Dash app
app = Dash(__name__)

# 1. load and sort data
df = pd.read_csv("formatted_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date")

# 2. define Layout with custom stylized elements
app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        "backgroundColor": "#f1f5f9",
        "minHeight": "100vh",
        "padding": "40px 20px"
    },
    children=[
        # main Dashboard Container Card
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "backgroundColor": "#ffffff",
                "borderRadius": "24px",
                "padding": "40px",
                "boxShadow": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
            },
            children=[
                # executive Header Section
                html.Div(
                    style={
                        "borderBottom": "2px solid #f1f5f9",
                        "paddingBottom": "24px",
                        "marginBottom": "32px",
                    },
                    children=[
                        html.H1(
                            "OmniMorsel Analytics Portal",
                            style={"color": "#0f172a", "fontSize": "2.25rem", "fontWeight": "900", "margin": "0 0 8px 0"}
                        ),
                        html.P(
                            "Executive performance track for Soul Foods Pink Morsel line item pricing strategy.",
                            style={"color": "#64748b", "fontSize": "1.05rem", "margin": "0"}
                        ),
                    ]
                ),

                # control Panel Region Selector Box
                html.Div(
                    style={
                        "backgroundColor": "#f8fafc",
                        "borderRadius": "16px",
                        "padding": "20px 24px",
                        "marginBottom": "32px",
                        "border": "1px solid #e2e8f0"
                    },
                    children=[
                        html.Label(
                            "Filter Analysis Region",
                            style={"display": "block", "fontWeight": "700", "color": "#334155", "marginBottom": "12px", "textTransform": "uppercase", "fontSize": "0.75rem", "letterSpacing": "0.05em"}
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": " Global (All)", "value": "all"},
                                {"label": " North Region", "value": "north"},
                                {"label": " East Region", "value": "east"},
                                {"label": " South Region", "value": "south"},
                                {"label": " West Region", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            style={"display": "flex", "gap": "24px", "fontWeight": "500", "color": "#475569"},
                        )
                    ]
                ),

                # interactive Data Graph
                html.Div(
                    children=[
                        dcc.Graph(id="sales-line-chart")
                    ]
                )
            ]
        )
    ]
)

# 3. reactive Data Callback Linkage
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    # filter dataset conditionally based on selection
    if selected_region == "all":
        filtered_df = df
        chart_title = "Pink Morsel Sales Performance - Global Analysis"
    else:
        filtered_df = df[df["region"].str.lower() == selected_region.lower()]
        chart_title = f"Pink Morsel Sales Performance - {selected_region.capitalize()} Region"

    # create figure object
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title=chart_title,
        labels={"date": "Timeline Range", "sales": "Gross Revenue Metric ($)"},
        template="plotly_white"
    )

    # apply aesthetic polish matching our layout colors
    fig.update_traces(line_color="#4f46e5", line_width=2.5)
    
    # retain our business benchmark line logic across queries
    fig.add_vline(
        x="2021-01-15",
        line_width=2,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Price Threshold Adjust (Jan 15, 2021)",
        annotation_position="top left"
    )
    
    fig.update_layout(
        title={"font": {"size": 18, "color": "#0f172a", "weight": "bold"}},
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

# run deployment runtime context
if __name__ == "__main__":
    app.run(debug=True)