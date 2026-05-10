import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt



st.set_page_config(
    page_title="NHL Analytics Dashboard",
    layout="wide"
)

st.title("🏒 NHL Analytics Dashboard")

st.markdown("""
### Analytical Objective

This dashboard analyzes NHL team and player performance using live NHL API data.
The objective is to identify offensive efficiency, defensive consistency,
and player productivity trends throughout the NHL season.
""")

BASE_URL = "https://api-web.nhle.com/v1"


@st.cache_data
def load_team_data():

    url = f"{BASE_URL}/standings/now"

    response = requests.get(url)
    data = response.json()

    teams = []

    for team in data['standings']:

        teams.append({
            "Team": team['teamName']['default'],
            "Points": team['points'],
            "Wins": team['wins'],
            "Losses": team['losses'],
            "Goals For": team['goalFor'],
            "Goals Against": team['goalAgainst'],
            "Goal Differential": team['goalDifferential'],
            "Games Played": team['gamesPlayed']
        })

    return pd.DataFrame(teams)



@st.cache_data
def load_player_data():

    url = f"{BASE_URL}/skater-stats-leaders/current?categories=goals,assists,points&limit=20"

    response = requests.get(url)
    data = response.json()

    players = []

    if "goals" in data:

        for player in data["goals"]:

            players.append({
                "Player": f"{player['firstName']['default']} {player['lastName']['default']}",
                "Team": player.get("teamAbbrev", ""),
                "Goals": player.get("value", 0),
                "Category": "Goals"
            })



    if "assists" in data:

        for player in data["assists"]:

            players.append({
                "Player": f"{player['firstName']['default']} {player['lastName']['default']}",
                "Team": player.get("teamAbbrev", ""),
                "Assists": player.get("value", 0),
                "Category": "Assists"
            })

    if "points" in data:

        for player in data["points"]:

            players.append({
                "Player": f"{player['firstName']['default']} {player['lastName']['default']}",
                "Team": player.get("teamAbbrev", ""),
                "Points": player.get("value", 0),
                "Category": "Points"
            })

    return pd.DataFrame(players)

team_df = load_team_data()
player_df = load_player_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Filters")

selected_team = st.sidebar.selectbox(
    "Select Team",
    ["All Teams"] + sorted(team_df["Team"].unique())
)

min_points = st.sidebar.slider(
    "Minimum Team Points",
    int(team_df["Points"].min()),
    int(team_df["Points"].max()),
    int(team_df["Points"].min())
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = team_df[
    team_df["Points"] >= min_points
]

if selected_team != "All Teams":
    filtered_df = filtered_df[
        filtered_df["Team"] == selected_team
    ]

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

st.subheader("League Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Highest Points",
        int(team_df["Points"].max())
    )

with c2:
    st.metric(
        "Best Goal Differential",
        int(team_df["Goal Differential"].max())
    )

with c3:
    st.metric(
        "League Avg Goals For",
        round(team_df["Goals For"].mean(), 2)
    )

with c4:
    st.metric(
        "League Avg Goals Against",
        round(team_df["Goals Against"].mean(), 2)
    )

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2 = st.tabs([
    "📊 Team Overview",
    "⛸️ Player Analytics"
])

# ===================================================
# TAB 1
# ===================================================

with tab1:

    st.header("Team Performance Overview")

    # -----------------------------------------------
    # BAR CHART
    # -----------------------------------------------

    st.subheader("Top Teams by Points")

    fig_bar = px.bar(
        filtered_df.sort_values("Points", ascending=False),
        x="Team",
        y="Points",
        color="Goal Differential",
        title="NHL Team Standings"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # -----------------------------------------------
    # SCATTER PLOT
    # -----------------------------------------------

    st.subheader("Goals For vs Goals Against")

    fig_scatter = px.scatter(
        filtered_df,
        x="Goals Against",
        y="Goals For",
        size="Points",
        color="Goal Differential",
        hover_name="Team",
        title="Offensive vs Defensive Efficiency"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # -----------------------------------------------
    # LINE CHART
    # -----------------------------------------------

    st.subheader("Goal Differential by Team")

    line_df = filtered_df.sort_values("Goal Differential")

    fig_line = px.line(
        line_df,
        x="Team",
        y="Goal Differential",
        markers=True,
        title="Goal Differential Trends"
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # -----------------------------------------------
    # ANALYSIS
    # -----------------------------------------------

    st.markdown("""
    ### Team Insights

    Teams with strong goal differentials consistently occupy the top tier
    of the standings. The scatter plot reveals that elite teams combine
    strong offensive production with disciplined defensive play.

    Several high-scoring teams also concede large numbers of goals,
    suggesting defensive weaknesses that could become problematic during
    playoff competition.
    """)

# ===================================================
# TAB 2
# ===================================================

with tab2:

    st.header("Player Analytics")

    # -----------------------------------------------
    # PLAYER BAR CHART
    # -----------------------------------------------

    goals_df = player_df[
        player_df["Category"] == "Goals"
    ]

    st.subheader("Top Goal Scorers")

    fig_goals = px.bar(
        goals_df,
        x="Player",
        y="Goals",
        color="Goals",
        title="NHL Goal Leaders"
    )

    st.plotly_chart(fig_goals, use_container_width=True)

    # -----------------------------------------------
    # HEATMAP
    # -----------------------------------------------

    st.subheader("Player Leader Heatmap")

    heatmap_df = goals_df[["Player", "Goals"]]

    heatmap_df = heatmap_df.set_index("Player")

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        heatmap_df,
        annot=True,
        cmap="coolwarm",
        linewidths=0.5,
        ax=ax
    )

    st.pyplot(fig)

    # -----------------------------------------------
    # RADAR CHART
    # -----------------------------------------------

    st.subheader("Top Player Comparison")

    top_players = goals_df.head(5)

    radar = go.Figure()

    for _, row in top_players.iterrows():

        radar.add_trace(go.Scatterpolar(
            r=[row["Goals"]],
            theta=["Goals"],
            fill='toself',
            name=row["Player"]
        ))

    radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=True
    )

    st.plotly_chart(radar, use_container_width=True)

    # -----------------------------------------------
    # ANALYSIS
    # -----------------------------------------------

    st.markdown("""
    ### Player Insights

    Elite scorers separate themselves through sustained offensive production
    over the course of the season. The heatmap highlights substantial gaps
    between top-tier goal scorers and the remainder of the league.

    High-volume scorers often correlate strongly with team success,
    particularly for teams competing for playoff positioning.
    """)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown("""
### Data Sources

- NHL Web API
- Live standings and player leader statistics

Dashboard built with:
- Streamlit
- Plotly
- Pandas
- Seaborn
""")