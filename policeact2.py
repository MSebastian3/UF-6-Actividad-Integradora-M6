import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import base64
import altair as alt

# Página completa
st.set_page_config(layout="wide")

# Set custom styles using HTML
# Custom CSS styles are applied to the entire page
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: bold;
    }
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-image {
        max-width: 400px;
        max-height: 200px;
        width: auto;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load and display the logo image with adjusted size
logo_path = 'logo.png'
logo_image = Image.open(logo_path)
logo_image_b64 = base64.b64encode(open(logo_path, 'rb').read()).decode('utf-8')
st.markdown(
    f'<div class="logo-container"><img class="logo-image" src="data:image/png;base64,{logo_image_b64}"></div>',
    unsafe_allow_html=True,
)

# Set the title of the web application
st.title("Police Incident Reports from 2018 to 2020 in San Francisco")

# Read the CSV file into a DataFrame
df = pd.read_csv('Police_Department_Incident_Reports__2018_to_Present.csv')

# Display an introduction about the data
st.markdown(
    "The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location, and resolution."
)

# Create a subset DataFrame with selected columns from the original DataFrame
mapa = pd.DataFrame()
mapa["Incident Date"] = df["Incident Date"]
mapa["Incident Year"] = df["Incident Year"]
mapa["Incident Day of Week"] = df["Incident Day of Week"]
mapa["Incident Category"] = df["Incident Category"]
mapa["Incident Subcategory"] = df["Incident Subcategory"]
mapa["Police District"] = df["Police District"]
mapa["Analysis Neighborhood"] = df["Analysis Neighborhood"]
mapa["Supervisor District"] = df["Supervisor District"]
mapa["lat"] = df["Latitude"]
mapa["lon"] = df["Longitude"]
mapa = mapa.dropna()

# Assign the subset DataFrame to a new variable for further filtering
subset_data2 = mapa

# Filters
# Use a sidebar for interactive filtering options
with st.sidebar:
    incident_date_input = st.multiselect('Incident Date', mapa['Incident Date'].unique())
    incident_subcategory_input = st.multiselect('Incident Subcategory', mapa['Incident Subcategory'].unique())
    analysis_neighborhood_input = st.multiselect('Analysis Neighborhood', mapa['Analysis Neighborhood'].unique())
    police_district_input = st.multiselect('Police District', mapa['Police District'].unique())
    supervisor_district_input = st.multiselect('Supervisor District', mapa['Supervisor District'].unique())

# Apply the selected filters to the subset DataFrame
subset_data = subset_data2

if len(incident_date_input) > 0:
    subset_data = subset_data2[subset_data2['Incident Date'].isin(incident_date_input)]

if len(incident_subcategory_input) > 0:
    subset_data = subset_data[subset_data['Incident Subcategory'].isin(incident_subcategory_input)]

if len(analysis_neighborhood_input) > 0:
    subset_data = subset_data[subset_data['Analysis Neighborhood'].isin(analysis_neighborhood_input)]

if len(police_district_input) > 0:
    subset_data = subset_data[subset_data['Police District'].isin(police_district_input)]

if len(supervisor_district_input) > 0:
    subset_data = subset_data[subset_data['Supervisor District'].isin(supervisor_district_input)]

# Display the filtered data
subset_data

# Display important information using Markdown
st.markdown('<h2 style="font-size: 24px; font-weight: bold;">It is important to mention that any police district can answer any incident, and the neighborhood in which it happened is not related to the police district.</h2>', unsafe_allow_html=True)

# Dataset information
# Uncomment the following lines if you want to display general information about the dataset
# agree = st.button('Click to see General Information')
# if agree:

subset_data3=mapa
# Top neighborhoods
neighborhood_counts = subset_data3['Analysis Neighborhood'].value_counts().sort_values(ascending=False)
num_neighborhoods = st.number_input('Number of top neighborhoods to display', min_value=1, max_value=len(neighborhood_counts), value=10, step=1)
top_neighborhoods = neighborhood_counts.head(num_neighborhoods)

top_neighborhoods_df = pd.DataFrame({'Neighborhood': top_neighborhoods.index, 'Count': top_neighborhoods.values})
top_neighborhoods_df['Neighborhood'] = pd.Categorical(top_neighborhoods_df['Neighborhood'], categories=top_neighborhoods.index, ordered=True)

st.markdown(f'<h2 style="font-size: 24px; font-weight: bold;">Top {num_neighborhoods} Analysis Neighborhoods with the Most Crimes</h2>', unsafe_allow_html=True)

# Define color range
rango_color = ["#000080", "#800000"]

# Create bar chart for top neighborhoods
chart_neighborhoods = alt.Chart(top_neighborhoods_df).mark_bar().encode(
    x=alt.X('Neighborhood', sort=None),
    y='Count',
    color=alt.Color('Count', scale=alt.Scale(range=rango_color))
).properties(
    width=1000,
    height=600
)

st.altair_chart(chart_neighborhoods)

# Incident categories
incident_counts = subset_data3['Incident Category'].value_counts().sort_values(ascending=False)
num_incident_categories = st.number_input('Number of top incident categories to display', min_value=1, max_value=len(incident_counts), value=10, step=1)
top_incident_categories = incident_counts.head(num_incident_categories)

top_incident_categories_df = pd.DataFrame({'Incident Category': top_incident_categories.index, 'Count': top_incident_categories.values})
top_incident_categories_df['Incident Category'] = pd.Categorical(top_incident_categories_df['Incident Category'], categories=top_incident_categories.index, ordered=True)

st.markdown(f'<h2 style="font-size: 24px; font-weight: bold;">Top {num_incident_categories} Types of Crimes Committed</h2>', unsafe_allow_html=True)

# Create bar chart for top incident categories
chart_incident_categories = alt.Chart(top_incident_categories_df).mark_bar().encode(
    x=alt.X('Incident Category', sort=None),
    y='Count',
    color=alt.Color('Count', scale=alt.Scale(range=rango_color))
).properties(
    width=1000,
    height=600
)

st.altair_chart(chart_incident_categories)


# Map
st.markdown('<h2 style="font-size: 24px; font-weight: bold;">Crime locations in San Francisco</h2>', unsafe_allow_html=True)
st.map(subset_data)

# Display the number of instances out of total instances
num_instances = len(subset_data)
total_instances_percentage = (num_instances / len(df)) * 100

st.markdown(f"The number of crimes registered with the filters applied is {num_instances}, which represents {total_instances_percentage:.2f}% of the total crimes registered")

# Filtered graphs
# Uncomment the following lines if you want to display filtered graphs
# agree = st.button('Click to see Graphs with the filters')
# if agree:

# Display a heading for crimes occurred per day of the week
st.markdown('<h2 style="font-size: 24px; font-weight: bold;">Crimes occurred per day of the week</h2>', unsafe_allow_html=True)
# Create a bar chart to visualize the count of crimes per day of the week using the subset_data DataFrame
st.bar_chart(subset_data['Incident Day of Week'].value_counts())

# Display a heading for crimes occurred per date
st.markdown('<h2 style="font-size: 24px; font-weight: bold;">Crimes occurred per date</h2>', unsafe_allow_html=True)
# Create a line chart to visualize the count of crimes per date using the subset_data DataFrame
st.line_chart(subset_data['Incident Date'].value_counts())

# Display a heading for the type of crimes committed
st.markdown('<h2 style="font-size: 24px; font-weight: bold;">Type of crimes committed</h2>', unsafe_allow_html=True)
# Create a bar chart to visualize the count of crimes per incident category using the subset_data DataFrame
st.bar_chart(subset_data['Incident Category'].value_counts())

# Display a heading for the subtype of crimes committed
st.markdown('<h2 style="font-size: 24px; font-weight: bold;">Subtype of crimes committed</h2>', unsafe_allow_html=True)
# Create a bar chart to visualize the count of crimes per incident subcategory using the subset_data DataFrame
st.bar_chart(subset_data['Incident Subcategory'].value_counts())
