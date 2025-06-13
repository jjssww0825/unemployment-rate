import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 📌 한글 폰트 설정 (운영체제별 대응)
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux or Streamlit Cloud
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 📌 제목
st.title("20~29세 성별 청년 실업률 분석 (2014~2024)")

# 📌 CSV 파일 읽기 (인코딩 오류 대비)
try:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='utf-8')

# 📌 20~29세 필터링
df_20s = df[df['연령계층별'] == '20 - 29세']

# 📌 원본 데이터 출력
st.subheader("원본 데이터")
st.dataframe(df_20s)

# 📌 연도 컬럼 리스트 추출
year_columns = [str(year) for year in range(2014, 2025)]

# 📌 long-format 변환
df_melted = df_20s.melt(id_vars=['성별'], value_vars=year_columns,
                        var_name='연도', value_name='실업률')
df_melted['연도'] = df_melted['연도'].astype(int)

# 📌 연도 슬라이더로 필터링
st.subheader("성별 실업률 변화 추이 (2014~2024)")

year_range = st.slider("연도 범위 선택", 2014, 2024, (2014, 2024))
filtered_df = df_melted[(df_melted['연도'] >= year_range[0]) & (df_melted['연도'] <= year_range[1])]

# 📌 시각화
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filtered_df, x='연도', y='실업률', hue='성별', marker='o', ax=ax)
ax.set_title('20~29세 성별 청년 실업률 추이')
ax.set_xlabel('연도')
ax.set_ylabel('실업률 (%)')
ax.grid(True)
st.pyplot(fig)


