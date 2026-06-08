import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
import urllib.request

# 1. 페이지 레이아웃 전체 화면 설정 및 CSS 주입
st.set_page_config(page_title="경제 수행평가 도우미", layout="wide")

# 모던하고 깔끔한 스타일에 집중한 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #f8fafc;
    }
    .main-header {
        background-color: white;
        padding: 1.2rem 2rem;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .step-badge {
        background-color: #2563eb;
        color: white;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        margin-right: 0.5rem;
    }
    .result-badge {
        background-color: #e0e7ff;
        color: #4338ca;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
    }
    .card-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 한글 폰트 설정 (그래프 깨짐 방지)
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

# 3. OpenAI 클라이언트 설정
try:
    client = OpenAI(api_key=st.secrets["YOUR_OPENAI_API_KEY"])
except Exception:
    st.error("⚠️ Streamlit Secrets에 API 키가 정확히 등록되지 않았습니다.")

# --- 상단 헤더 영역 ---
st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0;">📊 경제 수행평가 도우미</h1>
        <p style="font-size: 0.85rem; color: #64748b; margin: 5px 0 0 0;">기사 입력 기반 실시간 수요·공급 AI 시뮬레이터</p>
    </div>
""", unsafe_allow_html=True)

# --- 메인 화면 레이아웃 분할 (좌측 5 : 우측 7) ---
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    # STEP 1: 경제 기사 입력창만 깔끔하게 배치
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown('<h3><span class="step-badge">STEP 1</span><b>경제 기사 입력</b></h3>', unsafe_allow_html=True)
    st.write("분석하고 싶은 경제 기사의 제목과 본문을 입력해 주세요.")
    
    title_input = st.text_input("📍 기사 제목", placeholder="예시: 기상이변으로 원두 생산 비상, 커피값 오르나")
    body_input = st.text_area("📍 기사 본문", placeholder="신문 기사 내용을 이곳에 붙여넣으세요. 입력 즉시 AI가 분석을 시작합니다...", height=300)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # 입력이 없을 때 보여줄 대기 화면
    if not title_input and not body_input:
        st.markdown("""
            <div class="card-box" style="text-align: center; padding: 5rem 2rem;">
                <h3 style="color: #2563eb; font-size: 1.25rem;">✨ 실시간 AI 분석 가동 준비 완료!</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 10px;">
                    왼쪽 입력창에 경제 기사를 붙여넣는 순간,<br>
                    AI가 시장 요인을 분석하여 그래프와 수행평가 리포트를 동시에 완성합니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🧠 AI가 기사 속 수요·공급 메커니즘을 정밀 분석 중입니다..."):
            try:
                # 4. OpenAI API 요청 (상품명과 변동 방향까지 데이터로 뽑아내도록 프롬프트 개조)
                prompt = f"""
                너는 경제학을 가르치는 고등학교 교사야. 다음 경제 기사를 토대로 수행평가 보고서 양식에 맞게 깊이 있게 분석해줘.
                말투는 학생들에게 말하듯 친절하고 똑 부러지는 어조(~란다, ~요)를 사용해 주렴.

                [기사 제목]: {title_input}
                [기사 본문]: {body_input}

                출력할 때 반드시 맨 첫 줄에 그래프 제어용 데이터를 아래 형식을 지켜서 작성해줘. (보고서 본문에는 포함하지 마)
                [DATA] 상품명, 수요변동(증가/감소/없음), 공급변동(증가/감소/없음)
                예시: [DATA] 커피, 없음, 감소

                그 아래에는 구분선을 긋고 보고서 내용을 채워줘:
                ---
                ### 1. 기사의 경제학적 재구성
                (기사 내용을 바탕으로 어떤 상품 시장의 이야기인지 요약 서술)

                ### 2. 수요·공급 법칙에 따른 가격 결정 과정 분석
                * **수요 측면 분석 (원인)**: (수요가 왜 변했는지 구체적 원인 분석)
                * **공급 측면 분석 (원인)**: (공급이 왜 변했는지 구체적 원인 분석)
                * **최종 시장 균형 변동 메커니즘 (결과)**: (가격과 거래량이 최종적으로 어떻게 되었는지 경제 법칙으로 증명)

                ### 3. 수행평가 제출용 시사점 및 고찰
                (이 현상이 우리 사회나 소비자 의사결정에 던지는 의미 서술)
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                full_response = response.choices[0].message.content

                # 데이터 영역과 보고서 영역 분리 파싱
                lines = full_response.split('\n')
                data_line = [line for line in lines if line.startswith("[DATA]")]
                
                # 기본값 설정
                product_name = "해당 상품"
                d_shift, s_shift = 0, 0
                
                if data_line:
                    try:
                        raw_data = data_line[0].replace("[DATA]", "").strip().split(",")
                        product_name = raw_data[0].strip()
                        d_text = raw_data[1].strip()
                        s_text = raw_data[2].strip()
                        
                        if "증가" in d_text: d_shift = 20
                        elif "감소" in d_text: d_shift = -20
                        
                        if "증가" in s_text: s_shift = 20
                        elif "감소" in s_text: s_shift = -20
                    except:
                        pass
                
                # 순수 보고서 내용만 필터링
                ai_analysis = "\n".join([line for line in lines if not line.startswith("[DATA]")])
                if "---" in ai_analysis:
                    ai_analysis = ai_analysis.split("---", 1)[1].strip()

                # 5. 가격 및 거래량 화살표 텍스트 판단
                p_result = "상승 📈" if (d_shift > 0 and s_shift <= 0) or (d_shift >= 0 and s_shift < 0) else "하락 📉" if (d_shift < 0 and s_shift >= 0) or (d_shift <= 0 and s_shift > 0) else "변동 불분명 ❓"
                q_result = "증가 📈" if (d_shift > 0 and s_shift >= 0) or (d_shift >= 0 and s_shift > 0) else "감소 📉" if (d_shift < 0 and s_shift <= 0) or (d_shift <= 0 and s_shift < 0) else "변동 불분명 ❓"

                # 예측 결과 상단 대시보드
                st.markdown(f"""
                    <div class="card-box" style="background: linear-gradient(to right, #eff6ff, #f5f3ff); border: 1px solid #bfdbfe;">
                        <span style="font-size:0.75rem; color:#64748b; font-weight:700;">AI 실시간 시장 분석 결과</span>
                        <div style="font-size:1.15rem; font-weight:800; color:#1e3a8a; margin-top:2px;">📊 {product_name} 시장 변동</div>
                        <div style="display:flex; gap:15px; margin-top:12px;">
                            <div style="background:white; padding: 0.6rem 1.2rem; border-radius:10px; box-shadow:0 1px 2px rgb(0 0 0/0.05); flex:1; text-align:center;">
                                <div style="font-size:0.7rem; color:#94a3b8; font-weight:700;">균형 가격 결과</div>
                                <div style="font-size:1.1rem; font-weight:800; color:#dc2626;">{p_result}</div>
                            </div>
                            <div style="background:white; padding: 0.6rem 1.2rem; border-radius:10px; box-shadow:0 1px 2px rgb(0 0 0/0.05); flex:1; text-align:center;">
                                <div style="font-size:0.7rem; color:#94a3b8; font-weight:700;">균형 거래량 결과</div>
                                <div style="font-size:1.1rem; font-weight:800; color:#2563eb;">{q_result}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # 6. 시각화 그래프 그리기
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown('<h3><span class="result-badge">시각화 결과</span> <b>자동 생성된 수요·공급 변동 곡선</b></h3>', unsafe_allow_html=True)
                
                q_vals = np.linspace(10, 90, 100)
                d_base = 100 - q_vals
                s_base = q_vals

                fig, ax = plt.subplots(figsize=(6, 4.2))
                
                # 원래 곡선 (연한 점선)
                ax.plot(q_vals, d_base, label="원래 수요 (D)", color="#f43f5e", linestyle="--", alpha=0.3)
                ax.plot(q_vals, s_base, label="원래 공급 (S)", color="#10b981", linestyle="--", alpha=0.3)

                # 변동 후 곡선 (진한 실선)
                ax.plot(q_vals, d_base + d_shift, label="변동 후 수요 (D')", color="#e11d48", linewidth=2.5)
                ax.plot(q_vals, s_base + s_shift, label="변동 후 공급 (S')", color="#059669", linewidth=2.5)

                # 쉬프트 화살표
                if d_shift != 0:
                    ax.annotate('', xy=(50 + d_shift, 50 + d_shift/2), xytext=(50, 50),
                                arrowprops=dict(facecolor='#e11d48', shrink=0.08, width=1.5, headwidth=6))
                if s_shift != 0:
                    ax.annotate('', xy=(50 - s_shift/2, 50 + s_shift/2), xytext=(50, 50),
                                arrowprops=dict(facecolor='#059669', shrink=0.08, width=1.5, headwidth=6))

                ax.set_xlabel("수량 (Quantity)", fontproperties=font_prop, fontsize=9)
                ax.set_ylabel("가격 (Price)", fontproperties=font_prop, fontsize=9)
                ax.set_title(f"📈 {product_name} 시장의 균형 이동 시뮬레이션", fontproperties=font_prop, fontsize=11, fontweight="bold")
                ax.legend(prop=font_prop, loc="upper right", fontsize=8)
                ax.grid(True, linestyle=':', alpha=0.4)
                
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

                # 7. AI 완성형 보고서 출력
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown('<h3><span class="result-badge" style="background-color:#e0e7ff; color:#4338ca;">수행평가 결과물</span> <b>수요·공급 분석 보고서</b></h3>', unsafe_allow_html=True)
                st.markdown('<div style="line-height:1.7; font-size:0.95rem; color:#334155;">', unsafe_allow_html=True)
                st.markdown(ai_analysis)
                st.markdown('</div></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ 에러가 발생했습니다: {e}")