import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Set Streamlit page layout
st.set_page_config(page_title="Netflix Analysis", layout="wide")

# Title
st.title("📺 Netflix Data Analysis Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df.fillna({'country': 'Unknown', 'director': 'Unknown', 'cast': 'Unknown'}, inplace=True)

    # Convert dates
    df['date_added'] = pd.to_datetime(df['date_added'], format='mixed')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    return df

df = load_data()

# Show raw data option
if st.checkbox("Show Raw Dataset"):
    st.dataframe(df.head(20))

# --- Top Genres ---
st.subheader("🎬 Top 10 Genres on Netflix")
df['genre'] = df['listed_in'].str.split(', ')
genre_explode = df.explode('genre')
genre_count = genre_explode['genre'].value_counts().reset_index()
genre_count.columns = ['Genre', 'Count']

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=genre_count.head(10), x='Count', y='Genre', palette='Blues_d', ax=ax)
st.pyplot(fig)

# --- Year-wise Trend ---
st.subheader("📈 Trend of Netflix Content Releases Over Years")
yearly = df['release_year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(x=yearly.index, y=yearly.values, ax=ax)
ax.set_xlabel("Release Year")
ax.set_ylabel("Number of Titles")
ax.grid(True)
st.pyplot(fig)

# --- Country-wise Distribution ---
st.subheader("🌍 Top 10 Countries with Most Netflix Titles")
top_countries = df['country'].value_counts().head(10).reset_index()
top_countries.columns = ['Country', 'Count']
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_countries, x='Country', y='Count', palette='viridis', ax=ax)
ax.set_xlabel("Country")
ax.set_ylabel("Count")
st.pyplot(fig)

# --- Movie Duration Distribution ---
st.subheader("⏳ Movie Duration Distribution")
movies = df[df['type'] == 'Movie'].copy()
movies['duration'] = movies['duration'].str.replace(' min', '').astype(float)
fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(movies['duration'].dropna(), bins=30, kde=True, ax=ax)
ax.set_xlabel("Duration (minutes)")
st.pyplot(fig)

# --- TV Show Seasons ---
st.subheader("📺 TV Show Season Count Distribution")
tv_shows = df[df['type'] == 'TV Show'].copy()
tv_shows['duration'] = tv_shows['duration'].str.replace(' Season', '').str.replace('s', '').astype(float)
fig, ax = plt.subplots(figsize=(10, 4))
sns.countplot(data=tv_shows, x='duration', order=tv_shows['duration'].value_counts().index[:10], ax=ax)
ax.set_xlabel("Number of Seasons")
st.pyplot(fig)

# Download cleaned dataset
st.subheader("📂 Download Cleaned Dataset")
df.to_csv("netflix_cleaned.csv", index=False)
st.download_button("Download CSV", data=df.to_csv(index=False), file_name="netflix_cleaned.csv", mime="text/csv")
