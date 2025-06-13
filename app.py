import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.font_manager as fm

# 📌 운영체제별 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux (ex. Streamlit Cloud)
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False  # 음수 깨짐 방지

# 📌 제목
st.title("20~29세 성별 청년 실업률 분석 (2014~2024)")

# 📌 CSV 파일 읽기 (인코딩 오류 대비)
try:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv("성_연령별_실업률.csv", encoding='utf-8')

# 📌 20~29세만 필터링
df_20s = df[df['연령계층별'] == '20 - 29세']

# 📌 연도 컬럼 추출 및 슬라이더
year_columns = [str(year) for year in range(2014, 2025)]
min_year, max_year = st.slider("연도 범위 선택", 2014, 2024, (2014, 2024))

# 📌 long-format 변환
df_melted = df_20s.melt(id_vars=['성별'], value_vars=year_columns,
                        var_name='연도', value_name='실업률')
df_melted['연도'] = df_melted['연도'].astype(int)

# 📌 슬라이더로 선택된 연도 필터링
df_filtered = df_melted[(df_melted['연도'] >= min_year) & (df_melted['연도'] <= max_year)]

# 📌 원본 데이터 출력
st.subheader("필터링된 원본 데이터")
st.dataframe(df_filtered)

# 📌 시각화
st.subheader("성별 실업률 변화 추이")

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_filtered, x='연도', y='실업률', hue='성별', marker='o', ax=ax, linewidth=2, linestyle='-')
ax.set_title('20~29세 성별 청년 실업률 추이')
ax.set_xlabel('연도')
ax.set_ylabel('실업률 (%)')
ax.grid(True)

st.pyplot(fig)
