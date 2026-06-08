import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
import urllib.request

# 1. 한글 폰트 설정 (Streamlit Cloud 환경 대응)
@st.cache_data
def load_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    return font_path

font_path = load_font()
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False

# 2. OpenAI 클라이언트 설정 (Secrets에서 키 가져오기)
try:
    client = OpenAI(api_key=st.secrets["YOUR_OPENAI_API_KEY"])
except:
    st.error("⚠️ API 키를 설정해주세요! (Streamlit Secrets)")

# 3. 앱 화면 구성
st.set_page_config(page_title="경제 수행평가 1등급 도우미", layout="wide")

st.title("📊 경제 수행평가 1등급 도우미")
st.subheader("기사를 넣으면 수요·공급 분석부터 그래프까지 한 번에!")

with st.sidebar:
    st.header("💡 사용 방법")
    st.write("1. 분석하고 싶은 경제 기사를 복사해서 넣어주세요.")
    st.write("2. '분석 시작' 버튼을 누르면 AI 교사님이 분석을 시작합니다.")
    st.write("3. 그래프와 리포트를 확인하고 수행평가에 활용하세요!")

# 기사 입력창
news_text = st.text_area("📰 분석할 경제 기사를 여기에 붙여넣으세요:", height=250)

if st.button("🚀 경제 기사 분석 및 그래프 생성"):
    if not news_text:
        st.warning("기사를 입력해주세요!")
    else:
        with st.spinner("AI 교사님이 기사를 분석하며 그래프를 그리고 있습니다..."):
            try:
                # AI에게 분석 요청 (수요/공급 원인 및 결과 강조)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "너는 경제학 전공 교사야. 중고등학생이 이해하기 쉽게 친근한 말투로 기사를 분석해줘. 반드시 '수요 변화 원인', '공급 변화 원인', '균형 가격과 거래량의 변동 결과', '어려운 경제 용어 풀이'를 포함해줘."},
                        {"role": "user", "content": f"다음 기사를 분석해서 수요·공급 원리와 가격 변동 결과를 설명해줘:\n\n{news_text}"}
                    ]
                )
                
                analysis_result = response.choices[0].message.content

                # 임의의 수요/공급 이동 로직 (그래프용 - 기사 내용에 따라 방향 결정)
                # 실제 데이터 추출은 복잡하므로, 텍스트 분석 결과에 따라 이동 방향을 시뮬레이션
                shift_d = 20 if "수요" in analysis_result and ("증가" in analysis_result or "상승" in analysis_result) else -20 if "수요" in analysis_result and ("감소" in analysis_result or "하락" in analysis_result) else 0
                shift_s = -20 if "공급" in analysis_result and ("감소" in analysis_result or "하락" in analysis_result or "부족" in analysis_result) else 20 if "공급" in analysis_result and ("증가" in analysis_result or "과잉" in analysis_result) else 0

                # --- 📈 그래프 그리기 시작 ---
                q = np.linspace(0, 100, 100)
                # 기본 수요/공급 곡선 (직선)
                d_old = 100 - q
                s_old = q
                
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(q, d_old, label="기존 수요 (D0)", color="blue", linestyle="--", alpha=0.5)
                ax.plot(q, s_old, label="기존 공급 (S0)", color="orange", linestyle="--", alpha=0.5)

                # 변화 후 곡선
                d_new = 100 - q + shift_d
                s_new = q + shift_s
                
                ax.plot(q, d_new, label="변화 후 수요 (D1)", color="blue", linewidth=2)
                ax.plot(q, s_new, label="변화 후 공급 (S1)", color="orange", linewidth=2)

                # 화살표 표시 (변화 방향)
                if shift_d != 0:
                    ax.annotate('', xy=(50+shift_d, 50+shift_d/2), xytext=(50, 50), arrowprops=dict(facecolor='blue', shrink=0.05, width=2))
                if shift_s != 0:
                    ax.annotate('', xy=(50-shift_s/2, 50+shift_s/2), xytext=(50, 50), arrowprops=dict(facecolor='orange', shrink=0.05, width=2))

                ax.set_xlabel("수량 (Quantity)", fontproperties=font_prop)
                ax.set_ylabel("가격 (Price)", fontproperties=font_prop)
                ax.set_title("📈 수요·공급 균형 이동 분석", fontproperties=font_prop, fontsize=16)
                ax.legend(prop=font_prop)
                ax.grid(True, linestyle=':', alpha=0.6)
                # --- 📈 그래프 그리기 끝 ---

                # 화면 결과 출력 (탭으로 구분)
                tab1, tab2, tab3 = st.tabs(["📝 분석 리포트", "📈 경제 그래프", "📒 용어 사전"])
                
                with tab1:
                    st.markdown("### 🎓 AI 교사의 핵심 분석")
                    st.write(analysis_result)

                with tab2:
                    st.markdown("### 📊 수요·공급 곡선 변화")
                    st.pyplot(fig)
                    st.info("💡 점선은 변화 전, 실선은 변화 후를 의미합니다. 화살표는 이동 방향을 나타냅니다.")

                with tab3:
                    st.markdown("### 📒 기사 속 핵심 경제 용어")
                    # 용어 풀이만 따로 요청해서 보여주거나 분석 결과에서 추출하도록 유도 가능
                    st.write("리포트 하단의 용어 풀이 내용을 참고하여 수행평가 보고서를 작성하세요!")

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# 푸터
st.markdown("---")
st.caption("경제 수행평가 도우미 앱 | gpt-4o-mini 모델 사용")