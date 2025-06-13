import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from sklearn.linear_model import LinearRegression
import numpy as np

# ✅ 한글 폰트 설정 - NanumGothic 고정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False  # 음수 깨짐 방지

# ✅ 제목
st.title("20~29세 성별 청년 실업률 분석 및 예측 (2014~2024)")

# ✅ 데이터 불러오기
try:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='utf-8')

# ✅ 20~29세 데이터 필터링
df_20s = df[df['연령계층별'] == '20 - 29세']
year_columns = [str(year) for year in range(2014, 2025)]

# ✅ wide → long 변환
df_melted = df_20s.melt(id_vars=['성별'], value_vars=year_columns,
                        var_name='연도', value_name='실업률')
df_melted['연도'] = df_melted['연도'].astype(int)

# ✅ 슬라이더로 연도 범위 필터링
st.subheader("실업률 변화 추이")
year_range = st.slider("연도 범위 선택", 2014, 2024, (2014, 2024))
filtered_df = df_melted[(df_melted['연도'] >= year_range[0]) & (df_melted['연도'] <= year_range[1])]

# ✅ 시각화 및 선형 회귀 예측
fig, ax = plt.subplots(figsize=(10, 6))
예측결과 = {}

for gender in ['남자', '여자']:
    gender_df = df_melted[df_melted['성별'] == gender]
    train_df = gender_df[gender_df['연도'] < 2024]

    X_train = train_df[['연도']]
    y_train = train_df['실업률']

    model = LinearRegression()
    model.fit(X_train, y_train)

    예측_2024 = model.predict([[2024]])[0]
    예측결과[gender] = 예측_2024

    X_line = pd.DataFrame({'연도': list(X_train['연도']) + [2024]})
    y_line = model.predict(X_line)

    sns.lineplot(x=X_line['연도'], y=y_line, label=f"{gender} (예측)", ax=ax)

# ✅ 실제 데이터 시각화 (점선 제거)
sns.lineplot(data=filtered_df, x='연도', y='실업률', hue='성별', marker='o', ax=ax)

ax.set_title("20~29세 성별 실업률 변화 및 예측")
ax.set_xlabel("연도")
ax.set_ylabel("실업률 (%)")
ax.grid(True)

st.pyplot(fig)

# ✅ 예측 수치 출력
st.subheader("2024년 실업률 예측")
col1, col2 = st.columns(2)
col1.metric("남자 예측", f"{예측결과['남자']:.2f}%")
col2.metric("여자 예측", f"{예측결과['여자']:.2f}%")
