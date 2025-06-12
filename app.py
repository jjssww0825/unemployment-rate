import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Streamlit Cloud에서는 한글 깨질 수 있어 로컬에서는 동작 확인 필요)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우
# plt.rcParams['font.family'] = 'AppleGothic'  # Mac인 경우 주석 해제

# 제목
st.title("20~29세 성별 청년 실업률 분석 (2014~2024)")

# 데이터 불러오기
df = pd.read_csv("성_연령별_실업률.csv", encoding='cp949')

# 20~29세만 필터링
df_20s = df[df['연령계층별'] == '20 - 29세']

# 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df_20s)

# 연도 컬럼만 선택
year_columns = [str(year) for year in range(2014, 2025)]

# 데이터 전처리: wide -> long
df_melted = df_20s.melt(id_vars=['성별'], value_vars=year_columns,
                        var_name='연도', value_name='실업률')
df_melted['연도'] = df_melted['연도'].astype(int)

# 시각화
st.subheader("성별 실업률 변화 추이 (2014~2024)")

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_melted, x='연도', y='실업률', hue='성별', marker='o', ax=ax)
ax.set_title('20~29세 성별 청년 실업률 추이')
ax.set_xlabel('연도')
ax.set_ylabel('실업률 (%)')
ax.grid(True)
st.pyplot(fig)
