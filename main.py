import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Water Quality Dashboard - Biscayne Bay",
    layout="wide"
)

# --- 1. OVERVIEW SECTION ---
st.title("Water Quality Dashboard")
st.header("CIS 3590 - Internship-Ready Software Development")
st.subheader("Prof. Gregory Reis | Developer: Amanda T")

st.divider()

st.markdown("""
### Overview
Welcome to the **Biscayne Bay Water Quality Dashboard**. This interactive web application is designed to help environmental scientists, researchers, and developers analyze marine sensor data over time. 

Use the **sidebar** to upload your own custom CSV dataset or explore the default Biscayne Bay dataset provided. Navigate through the tabs below to view raw data, interactive charts, and geospatial maps along with key insights.
""")

st.sidebar.header("📁 Data Management")
st.sidebar.info("Upload a custom CSV file with water quality data or use the default dataset.")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom dataset loaded successfully!")
else:
    df = pd.read_csv("biscayneBay_waterquality.csv")
    st.sidebar.info("Using default Biscayne Bay dataset.")


tab_overview, tab_data, tab_charts, tab_maps, tab_agile = st.tabs([
    " Overview & Summary",
    " Data Display",
    " Insights & Charts",
    " Spatial Maps",
    " Agile & Project Info"
])

with tab_overview:
    st.subheader("Quick Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Total Parameters Tracked", len(df.columns))
    col3.metric("Location Coordinates", f"{df['Latitude'].nunique()} stations")

    st.markdown("""
    #### Key Highlights:
    * **Data Integrity:** Automatically parsed and cleaned using Pandas.
    * **Interactivity:** Filter parameters dynamically using Plotly charts and sidebar controls.
    * **Scalability:** Supports custom CSV uploads for any water monitoring station.
    """)

with tab_data:
    st.subheader("Raw Data & Statistical Analysis")
    st.markdown("Explore the raw dataset records and underlying descriptive statistics below:")

    all_columns = df.columns.tolist()
    selected_columns = st.multiselect(
        "Select columns to display in the table:",
        options=all_columns,
        default=all_columns[:min(5, len(all_columns))]
    )

    if selected_columns:
        st.dataframe(df[selected_columns], use_container_width=True)
    else:
        st.warning("Please select at least one column to display the table.")

    st.caption("Descriptive Statistics Summary")
    st.dataframe(df.describe(), use_container_width=True)

with tab_charts:
    st.subheader(" Interactive Data Visualizations")
    st.markdown("Analyze environmental trends, correlations, and 3D depth topography.")

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    default_param = "Temperature (c)" if "Temperature (c)" in numeric_cols else numeric_cols[0]

    parameter = st.selectbox("Select a parameter for Time-Series Analysis", options=numeric_cols,
                             index=numeric_cols.index(default_param))

    fig1 = px.line(
        df,
        x="Time",
        y=parameter,
        title=f"Trend Analysis: {parameter} over Time",
        labels={parameter: parameter, "Time": "Timestamp"}
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(f"This line chart illustrates how **{parameter}** fluctuates across recorded timestamps.")

    col_a, col_b = st.columns(2)
    with col_a:
        if "Temperature (c)" in df.columns and "Salinity (ppt)" in df.columns:
            fig2 = px.scatter(
                df,
                x="Temperature (c)",
                y="Salinity (ppt)",
                title="Correlation: Temperature vs Salinity",
                color="Temperature (c)"
            )
            st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        if all(col in df.columns for col in ["Longitude", "Latitude", "Total Water Column (m)"]):
            fig3 = px.scatter_3d(
                df,
                x="Longitude",
                y="Latitude",
                z="Total Water Column (m)",
                color="Temperature (c)",
                title="3D Bay Floor Topography"
            )
            fig3.update_scenes(zaxis_autorange="reversed")
            fig3.update_traces(marker_size=3)
            st.plotly_chart(fig3, use_container_width=True)

with tab_maps:
    st.subheader(" Geospatial Distribution Map")
    st.markdown("Explore spatial readings across geographic coordinates in Biscayne Bay.")

    if "Latitude" in df.columns and "Longitude" in df.columns:
        first_map = px.scatter_map(
            df,
            lat="Latitude",
            lon="Longitude",
            title="Water Quality Station Readings on Map",
            center={"lat": df["Latitude"].mean(), "lon": df["Longitude"].mean()},
            zoom=12,
            color="Temperature (c)" if "Temperature (c)" in df.columns else None,
            color_continuous_scale="viridis"
        )
        st.plotly_chart(first_map, use_container_width=True)
        st.caption("Map points are color-coded by temperature readings across sampled GPS coordinates.")
    else:
        st.error("Latitude and Longitude columns are required for map visualization.")

with tab_agile:
    st.subheader(" Agile Development & Workflow")
    st.markdown("""
    This project was built following **Agile software development principles**:
    * **Sprint Planning:** Broken down into iterative phases (Sprint 1: Data ingestion & basic UI, Sprint 2: Interactive Plotly charts & filtering, Sprint 3: Deployment & refinement).
    * **Version Control:** Managed via GitHub repository commits and pull requests.
    * **User Stories Implemented:**
        * *As an environmental researcher, I want to upload custom CSV datasets so I can analyze my own water sensor data.*
        * *As a student, I want clear tabs and textual explanations so the dashboard is easy to navigate and interpret.*
    """)