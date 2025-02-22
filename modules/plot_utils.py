# -*- coding: utf-8 -*-
"""Plotly related utility functions."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from scipy.signal import savgol_filter
import io

def create_timeseries_plot(df, x_col, y_col, title, x_title, y_title):
    """Creates a simple timeseries plot using Plotly."""
    fig = px.line(df, x=x_col, y=y_col, title=title)
    fig.update_layout(xaxis_title=x_title, yaxis_title=y_title)
    return fig

def apply_savitzky_golay_filter(df, y_col, window_length, polyorder):
    """Applies a Savitzky-Golay filter to the specified column in the DataFrame."""
    return savgol_filter(df[y_col], window_length, polyorder)

def plot_timeseries(self):
    print('plot1 started')
    self.df_ajust()
    
    # Prepare to plot
    myFile = io.StringIO()
    if self.QCheckBox_sav_filter.isChecked() and self.df_run_filter():
        df = self.df_aux
        try:
            self.fig = go.Figure()
            self.fig.add_trace(go.Scatter(x=df['date'], y=df['average_index'], mode='lines', name=self.series_indice.currentText(), line=dict(color='green')))
            self.fig.add_trace(go.Scatter(x=df['date'], y=df['savitzky_golay_filtered'], mode='lines', name=f"{self.series_indice.currentText()} filtered", line=dict(color='purple')))
        except Exception as e:
            self.pop_aviso(f"An error occurred while plotting: {e}")
            self.QCheckBox_sav_filter.setChecked(False)
    else:
        df = self.df_aux
        self.fig = go.Figure()
        self.fig.add_trace(go.Scatter(x=df['date'], y=df['average_index'], mode='lines', name=self.series_indice.currentText(), line=dict(color='green')))
   
    self.fig.update_layout(
        xaxis_title='Date', 
        yaxis_title=self.series_indice.currentText(), 
        title=f"Time Series - {self.series_indice.currentText()} - {self.vector_layer_combobox.currentText()}               Image count: {len(df)}"
    )

    self.fig.update_traces(hovertemplate='date = %{x|%Y-%m-%d}<br>average_ndvi = %{y:.2f}<extra></extra>')
    
    # Configurations for the Plotly plot
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': [
            "toImage", "sendDataToCloud", "zoom2d", "pan2d", "select2d",
            "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d",
            "pan3d", "orbitRotation", "tableRotation", "resetCameraLastSave",
            "resetCameraDefault3d", "hoverClosest3d", "zoomInGeo", 
            "zoomOutGeo", "resetGeo", "hoverClosestGeo", "hoverClosestGl2d",
            "hoverClosestPie", "toggleHover", "toggleSpikelines", "resetViews"
        ]
    }

    if isinstance(self.df_nasa, pd.DataFrame):
        # Add bar plot (set below the line explicitly)
        self.fig.add_trace(go.Bar(
            x=self.df_nasa.index, 
            y=self.df_nasa['PRECTOTCORR'], 
            name='Monthly Precipitation', 
            yaxis='y2', 
            marker_color='blue',
            opacity=0.4
        ))

        # Ensure correct layout and layering
        self.fig.update_layout(
            yaxis=dict(
                title=self.series_indice.currentText(),
            ),
            yaxis2=dict(
                title='Precipitation (mm)',
                overlaying='y',
                side='right',
            ),
            xaxis=dict(title='Date'),
        )

    
    # Update layout and render the plot
    self.fig.write_html(myFile, config=config)
    html = myFile.getvalue()  
    self.webView.setHtml(html)

    self.tabWidget.setCurrentIndex(9)
    # self.showNormal()
    QApplication.restoreOverrideCursor()

    self.plot1 = True
