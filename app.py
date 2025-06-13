
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from sklearn.linear_model import LinearRegression
import numpy as np

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False

# 제목
st.title("20~29세 성별 청년 실업률 분석 및 예측 (2014~2024)")

# CSV 불러오기
try:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='utf-8')

df_20s = df[df['연령계층별'] == '20 - 29세']
year_columns = [str(year) for year in range(2014, 2025)]

# 데이터 melt
df_melted = df_20s.melt(id_vars=['성별'], value_vars=year_columns,
                        var_name='연도', value_name='실업률')
df_melted['연도'] = df_melted['연도'].astype(int)

# 연도 필터 슬라이더
st.subheader("실업률 변화 추이")
year_range = st.slider("연도 범위 선택", 2014, 2024, (2014, 2024))
filtered_df = df_melted[(df_melted['연도'] >= year_range[0]) & (df_melted['연도'] <= year_range[1])]

# 선형 회귀 예측 (남자, 여자 각각)
predictions = {}
fig, ax = plt.subplots(figsize=(10, 6))

for gender in ['남자', '여자']:
    gender_df = df_melted[df_melted['성별'] == gender]
    train = gender_df[gender_df['연도'] < 2024]
    test = gender_df[gender_df['연도'] == 2024]

    X_train = train[['연도']]
    y_train = train['실업률']
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 2024 예측
    y_pred_2024 = model.predict([[2024]])[0]
    predictions[gender] = y_pred_2024

    # 예측 선 그리기
    years_extended = np.append(train['연도'], 2024)
    y_extended = np.append(y_train, y_pred_2024)
    sns.lineplot(x=years_extended, y=y_extended, label=f"{gender} (예측)", marker='o', ax=ax)

# 실제 데이터 플롯
sns.lineplot(data=filtered_df, x='연도', y='실업률', hue='성별', style='성별', dashes=False, markers=True, ax=ax)

ax.set_title("20~29세 성별 청년 실업률 및 예측 (Linear Regression)")
ax.set_xlabel("연도")
ax.set_ylabel("실업률 (%)")
ax.grid(True)
st.pyplot(fig)

# 결과 출력
st.subheader("2024년 실업률 예측 (Linear Regression)")
col1, col2 = st.columns(2)
col1.metric("남자 예측 실업률", f"{predictions['남자']:.2f}%")
col2.metric("여자 예측 실업률", f"{predictions['여자']:.2f}%")
