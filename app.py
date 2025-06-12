import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 제목
st.title("20~29세 성별 청년 실업률 분석 (2014~2024)")

# 데이터 불러오기
df = pd.read_csv("성_연령별_실업률.csv")

# 데이터 확인
st.subheader("원본 데이터")
st.dataframe(df)

# 필요한 컬럼만 추출
# ↓ 이 부분은 실제 데이터 컬럼명을 기반으로 코드를 수정해야 함
# 예시:
# df = df[df["연령대"] == "20~29세"]
# df = df[df["성별"].isin(["남자", "여자"])]
# df = df[df["시점"].between(2014, 2024)]

# 추후 시각화를 위한 전처리 계속 작성
