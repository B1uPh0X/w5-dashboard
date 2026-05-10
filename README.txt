````markdown
# NHL Performance Analytics Dashboard

## Overview

This project is an interactive Streamlit dashboard that analyzes NHL team and player performance using live data from the NHL Web API.

The dashboard was designed to evaluate:

- Offensive efficiency
- Defensive consistency
- Team competitiveness
- Individual player productivity
- Scoring trends across the league

The application allows users to interactively explore NHL statistics through multiple visualizations and dashboard controls.


# Analytical Objective

The primary objective of this dashboard is to analyze NHL performance trends throughout the season in order to identify:

- Teams with strong offensive and defensive balance
- Potential playoff contenders
- High-performing individual players
- Relationships between scoring production and overall success

The dashboard emphasizes actionable insights rather than simple descriptive statistics.


# Features

## Dashboard Components

The dashboard includes:

### Tabs
- Team Overview
- Player Analytics

### Interactive Elements
- Sidebar filters
- Team selector dropdown
- Minimum points slider
- Metric cards (`st.metric`)
- Interactive Plotly visualizations

### Visualization Types
- Bar charts
- Scatter plots
- Line charts
- Heatmaps
- Radar charts

# Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Seaborn
- Matplotlib
- Requests


# Data Source

This project uses live NHL data retrieved from the NHL Web API.

## NHL API Base URL

```text
https://api-web.nhle.com/v1/
```

## Documentation References

- https://github.com/Zmalski/NHL-API-Reference
- https://medium.com/@vtashlikovich/nhl-api-what-data-is-exposed-and-how-to-analyse-it-with-python-745fcd6838c2


# Data Collection Method

Data is retrieved dynamically through HTTP requests using the `requests` Python library.

The dashboard accesses:

- Current NHL standings
- Team statistics
- Player scoring leader statistics

The API data is automatically refreshed whenever the Streamlit application reloads.

## Updating Data

Because the application uses live NHL API endpoints, statistics automatically update throughout the season.

No manual CSV updates are required.


## Future Maintenance Process

If NHL API endpoints change in the future:

1. Update endpoint URLs in `streamlit-dashboard.py`
2. Modify JSON parsing logic if response structures change
3. Redeploy the Streamlit application



## Install Dependencies

```bash
pip install -r requirements.txt
```


# Running the Application

Run locally with:

```bash
streamlit run app.py
```

The application will launch in your browser.


# Deployment

This dashboard is deployed using Streamlit Community Cloud.

## Deployment Link

```text
https://w5-dashboard-suhjlk8mt892kv9dfykv78.streamlit.app/
```


# Repository Link

```text
https://github.com/B1uPh0X/w5-dashboard
```


# Dashboard Insights

## Team Analysis

The dashboard reveals that teams with strong goal differentials consistently perform better in the standings.
Successful teams generally combine, high offensive production, lower goals allowed, and strong overall balance.
Scatter plot analysis highlights teams that may rely too heavily on offense while lacking defensive consistency.


## Player Analysis

Player leader visualizations show clear separation between elite scorers and the remainder of the league.
Radar chart and heatmap comparisons help identify, Offensive specialists, balanced contributors, and consistent high-performing players
These insights demonstrate how individual production contributes to overall team success.



