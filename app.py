import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# TITLE
# -----------------------------
st.title("🚲 Washington D.C. Bike Rentals Dashboard")
st.markdown("Interactive analysis of bike rental patterns based on time and weather.")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour

    season_map = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
    df['season_name'] = df['season'].map(season_map)

    weather_map = {
        1: 'Clear/Partly cloudy',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow/Fog'
    }
    df['weather_desc'] = df['weather'].map(weather_map)

    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

year = st.sidebar.selectbox("Select Year", sorted(df['year'].unique()))
working = st.sidebar.radio("Day Type", ["All", "Working", "Non-Working"])
season = st.sidebar.multiselect(
    "Select Season",
    df['season_name'].unique(),
    default=df['season_name'].unique()
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = df[df['year'] == year]

if working == "Working":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif working == "Non-Working":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

filtered_df = filtered_df[filtered_df['season_name'].isin(season)]

# -----------------------------
# PLOT 1 — HOURLY RENTALS
# -----------------------------
st.subheader("📈 Mean Rentals by Hour")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_df, x="hour", y="count", ax=ax)
st.pyplot(fig)

# -----------------------------
# PLOT 2 — MONTHLY RENTALS
# -----------------------------
st.subheader("📅 Mean Rentals by Month")
fig, ax = plt.subplots()
sns.barplot(data=filtered_df, x="month", y="count", ax=ax)
st.pyplot(fig)

# -----------------------------
# PLOT 3 — WEATHER
# -----------------------------
st.subheader("🌦 Mean Rentals by Weather")
fig, ax = plt.subplots()
sns.pointplot(
    data=filtered_df,
    x="weather_desc",
    y="count",
    errorbar=('ci', 95),
    ax=ax
)
plt.xticks(rotation=20)
st.pyplot(fig)

# -----------------------------
# OBSERVATIONS
# -----------------------------
st.markdown("""
### 🔍 Key Insights
- Rentals peak during commuting hours.
- Clear weather results in higher bike usage.
- Working days show stronger rental patterns.
""")
# -----------------------------
# PLOT 4 — SEASON vs RENTALS
# -----------------------------
st.subheader("🍂 Mean Rentals by Season")
fig, ax = plt.subplots()
sns.barplot(
    data=filtered_df,
    x="season_name",
    y="count",
    ax=ax
)
st.pyplot(fig)
# -----------------------------
# PLOT 5 — WORKING vs NON-WORKING DAYS
# -----------------------------
st.subheader("🏢 Rentals: Working vs Non-Working Days")
fig, ax = plt.subplots()
sns.barplot(
    data=filtered_df,
    x="workingday",
    y="count",
    ax=ax
)
ax.set_xticklabels(["Non-Working Day", "Working Day"])
st.pyplot(fig)
