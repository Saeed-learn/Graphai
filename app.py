import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages

# Set the page layout
st.set_page_config(layout="wide")

st.title("Enhanced Graph Generator")

# Sidebar for data input
st.sidebar.header("1. Data Input")

# Option for data entry: Upload or Manual Entry
data_entry_option = st.sidebar.radio("Choose Data Input Method", ["Upload CSV", "Enter Manually"])

# Data upload or entry
if data_entry_option == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
else:
    # Data entry grid
    st.sidebar.write("Enter Data Manually")
    num_rows = st.sidebar.number_input("Number of Rows", min_value=1, value=5)
    num_cols = st.sidebar.number_input("Number of Columns", min_value=1, value=3)
    df = pd.DataFrame(columns=[f"Column {i+1}" for i in range(num_cols)], index=range(num_rows))
    df = st.sidebar.data_editor(df)  # Updated to use `data_editor` instead of `experimental_data_editor`

if 'df' in locals():
    st.write("## Data Preview", df)
    columns = df.columns.tolist()

    # Sidebar for graph settings
    st.sidebar.header("2. Graph Settings")
    graph_type = st.sidebar.selectbox("Select Graph Type", ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", "Pie Chart"])

    x_col = st.sidebar.selectbox("Choose X-axis column", columns)
    y_col = st.sidebar.selectbox("Choose Y-axis column", columns) if graph_type != "Pie Chart" else None
    additional_y_col = st.sidebar.selectbox("Choose additional Y-axis column", columns) if graph_type == "Line Plot" else None

    # Plot customization options
    color_picker = st.sidebar.color_picker("Choose a color for the plot", "#1f77b4")
    marker_style = st.sidebar.selectbox("Marker Style", ["o", "s", "^", "D", "None"])
    line_style = st.sidebar.selectbox("Line Style", ["solid", "dashed", "dashdot", "dotted"])
    grid_option = st.sidebar.checkbox("Show Grid", True)

    # Labels and title
    plot_title = st.sidebar.text_input("Plot Title", "My Plot")
    x_label = st.sidebar.text_input("X-axis Label", "X-axis")
    y_label = st.sidebar.text_input("Y-axis Label", "Y-axis")

    # Interactive Plotly Graph
    st.header("Generated Graph")
    if graph_type == "Line Plot":
        fig = px.line(df, x=x_col, y=[y_col, additional_y_col] if additional_y_col else y_col, title=plot_title)
    elif graph_type == "Bar Plot":
        fig = px.bar(df, x=x_col, y=y_col, title=plot_title)
    elif graph_type == "Scatter Plot":
        fig = px.scatter(df, x=x_col, y=y_col, title=plot_title)
    elif graph_type == "Histogram":
        fig = px.histogram(df, x=y_col, title=plot_title)
    elif graph_type == "Pie Chart":
        fig = px.pie(df, names=x_col, title=plot_title)

    # Customize plotly figure layout
    fig.update_layout(
        title=plot_title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        showlegend=True,
    )
    fig.update_traces(marker=dict(color=color_picker, symbol=marker_style))
    if grid_option:
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

    st.plotly_chart(fig)

    # Download options
    st.sidebar.header("3. Download Options")
    output_format = st.sidebar.selectbox("Download Format", ["SVG", "PNG", "JPG", "PDF"])

    def download_plot():
        buffer = BytesIO()
        if output_format == "PDF":
            with PdfPages(buffer) as pdf:
                plt.figure()
                fig.write_image(buffer, format="pdf")
                pdf.savefig()  # saves the current figure into a pdf page
            buffer.seek(0)
        else:
            fig.write_image(buffer, format=output_format.lower())
        return buffer

    st.download_button(
        label=f"Download plot as {output_format}",
        data=download_plot(),
        file_name=f"custom_plot.{output_format.lower()}",
        mime=f"application/{output_format.lower() if output_format != 'PDF' else 'pdf'}",
    )
else:
    st.info("Awaiting CSV file upload or data entry.")
