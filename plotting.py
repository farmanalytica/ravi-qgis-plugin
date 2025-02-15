# plotting.py
import io
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter

def apply_savgol_filter(df, window_length, polyorder):
    """
    Apply the Savitzky-Golay filter to smooth the 'average_index' column.
    Returns a new DataFrame with an added 'savitzky_golay_filtered' column.
    """
    try:
        df = df.copy()
        if window_length > len(df):
            window_length = len(df)
        df['savitzky_golay_filtered'] = savgol_filter(df['average_index'], window_length=window_length, polyorder=polyorder)
        return df
    except Exception as e:
        print("Error applying Savitzky-Golay filter:", e)
        return df

def generate_time_series_plot(df, index_name, layer_name):
    """
    Generate an interactive Plotly time series plot from the DataFrame.
    Returns the HTML as a string.
    """
    myFile = io.StringIO()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['average_index'], mode='lines', name=index_name, line=dict(color='green')))
    if 'savitzky_golay_filtered' in df.columns:
        fig.add_trace(go.Scatter(x=df['date'], y=df['savitzky_golay_filtered'],
                                 mode='lines', name=f"{index_name} filtered", line=dict(color='purple')))
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=index_name,
        title=f"Time Series - {index_name} - {layer_name} | Image count: {len(df)}"
    )
    fig.update_traces(hovertemplate='date = %{x|%Y-%m-%d}<br>value = %{y:.2f}<extra></extra>')
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': [
            "toImage", "sendDataToCloud", "zoom2d", "pan2d", "select2d",
            "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian"
        ]
    }
    fig.write_html(myFile, config=config)
    return myFile.getvalue()