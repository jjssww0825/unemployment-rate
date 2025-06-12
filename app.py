import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Font settings: remove Korean fonts since we're using English
plt.rcParams['axes.unicode_minus'] = False

# 📌 Title
st.title("Youth Unemployment Rate by Gender (Aged 20–29, 2014–2024)")

# 📌 Load CSV (handle encoding errors)
try:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='utf-8')

# 📌 Filter for age group 20–29
df_20s = df[df['연령계층별'] == '20 - 29세']

# 📌 Show raw data
st.subheader("Raw Data")
st.dataframe(df_20s)

# 📌 Extract year columns
year_columns = [str(year) for year in range(2014, 2025)]

# 📌 Convert to long format
df_melted = df_20s.melt(id_vars=['성별'], value_vars=year_columns,
                        var_name='Year', value_name='Unemployment Rate')
df_melted['Year'] = df_melted['Year'].astype(int)

# Translate gender to English
df_melted['Gender'] = df_melted['성별'].map({'남자': 'Male', '여자': 'Female'})
df_melted.drop(columns='성별', inplace=True)

# 📌 Visualization
st.subheader("Unemployment Rate Trend by Gender (2014–2024)")

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_melted, x='Year', y='Unemployment Rate', hue='Gender', marker='o', ax=ax)
ax.set_title('Unemployment Rate Trend (Aged 20–29)')
ax.set_xlabel('Year')
ax.set_ylabel('Unemployment Rate (%)')
ax.grid(True)
st.pyplot(fig)


