import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
import urllib.request

# 1. 페이지 레이아웃 전체 화면 설정 및 CSS 주입
st.set_page_config(page_title="경제 기사 수행평가 작성이", layout="wide")

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
        background-color: #059669;
        color: white;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        margin-right: 0.5rem;
    }
    .result-badge {
        background-color: #f0fdf4;
        color: #166534;
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
        <h1 style="font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0;">📰 경제 기사 수행평가 생성기 (만점 보장용)</h1>
        <p style="font-size: 0.85rem; color: #64748b; margin: 5px 0 0 0;">평가기준(표제·전문·본문 형식 + 현재 그래프 + 미래 예측 그래프) 완벽 반영</p>
    </div>
""", unsafe_allow_html=True)

# --- 메인 화면 레이아웃 분할 ---
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown('<h3><span class="step-badge">STEP 1</span><b>참고 경제 뉴스 입력</b></h3>', unsafe_allow_html=True)
    st.write("학교 수행평가용 자료로 조사해 온 뉴스 기사를 넣어주세요.")
    
    title_input = st.text_input("📍 뉴스 제목", placeholder="예시: 미국 코로나 확산에 내수 부진... 체리 수입 가격 뚝")
    body_input = st.text_area("📍 뉴스 본문", placeholder="참고할 뉴스 기사 내용을 이곳에 붙여넣으세요...", height=300)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if not title_input and not body_input:
        st.markdown("""
            <div class="card-box" style="text-align: center; padding: 5rem 2rem;">
                <h3 style="color: #059669; font-size: 1.25rem;">✨ 수행평가 최적화 가동 준비 완료!</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 10px;">
                    참고 기사를 입력하면 평가 기준인 <b>기사 3대 형식(표제/전문/본문)</b>에 맞춘 글과<br>
                    <b>[현재 변동 차트] 및 [미래 예측 차트] 2개</b>를 동시에 자동 생성합니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🧠 평가 기준을 정밀 분석하여 만점짜리 기사와 그래프를 생성 중입니다..."):
            try:
                # 평가 기준을 저격하는 정밀 프롬프트
                prompt = f"""
                너는 중고등학교 사회/경제 교사 및 채점관이야. 아래 제공된 뉴스를 바탕으로, 학생이 '수요와 공급의 원리' 수행평가에서 만점을 받을 수 있도록 '경제 기사'를 대신 작성해줘.
                
                [참고 뉴스 제목]: {title_input}
                [참고 뉴스 본문]: {body_input}

                반드시 채점 기준인 [표제], [전문], [본문] 형식을 완벽하게 갖추어야 해.
                또한, 본문에는 '현재의 시장 가격 변동 원인 분석'과 '미래에 예상되는 타당한 시장 변화 예측'이 모두 깊이 있게 들어가야 한단다.

                출력할 때 맨 첫 줄에 그래프 제어용 데이터를 반드시 아래 형식을 정확히 지켜서 작성해줘. (기사 본문에는 포함하지 마)
                [DATA] 상품명, 현재수요(증가/감소/없음), 현재공급(증가/감소/없음), 미래수요(증가/감소/없음), 미래공급(증가/감소/없음)
                예시: [DATA] 체리, 없음, 증가, 증가, 없음

                그 아래에는 구분선(---)을 긋고 신문 기사 형태로 내용을 채워줘:
                ---
                ## 📰 내가 작성한 경제 기사

                ### 📌 [표제]
                (기사의 내용을 관통하는 매력적이고 핵심적인 제목 작성)

                ### 📌 [전문]
                (기사 본문의 핵심 내용을 요약한 3줄 이내의 전문 코너 작성)

                ### 📌 [본문 (1) - 현재 시장의 변화와 원인]
                (수요 법칙과 공급 법칙을 활용하여, 현재 가격과 거래량이 왜 이렇게 변했는지 원인을 분석하여 상세히 서술)

                ### 📌 [본문 (2) - 미래 시장 예측 및 시사점]
                (해당 상품에 대한 선호도 변화, 기술 혁신, 혹은 사회적 현상 등 타당한 근거를 들어 미래의 수요·공급 변화와 가격 추이를 논리적으로 예측)
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                full_response = response.choices[0].message.content

                # 파싱 작업
                lines = full_response.split('\n')
                data_line = [line for line in lines if line.startswith("[DATA]")]
                
                product_name = "해당 상품"
                cur_d, cur_s, fut_d, fut_s = 0, 0, 0, 0
                
                if data_line:
                    try:
                        raw_data = data_line[0].replace("[DATA]", "").strip().split(",")
                        product_name = raw_data[0].strip()
                        
                        # 현재 쉬프트 값 계산
                        if "증가" in raw_data[1]: cur_d = 20
                        elif "감소" in raw_data[1]: cur_d = -20
                        if "증가" in raw_data[2]: cur_s = 20
                        elif "감소" in raw_data[2]: cur_s = -20
                        
                        # 미래 쉬프트 값 계산
                        if "증가" in raw_data[3]: fut_d = 20
                        elif "감소" in raw_data[3]: fut_d = -20
                        if "증가" in raw_data[4]: fut_s = 20
                        elif "감소" in raw_data[4]: fut_s = -20
                    except:
                        pass
                
                # 기사 글만 추출
                ai_article = "\n".join([line for line in lines if not line.startswith("[DATA]")])
                if "---" in ai_article:
                    ai_article = ai_article.split("---", 1)[1].strip()

                # --- 그래프 2개 그리기 (수행평가 완벽 대응) ---
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown('<h3><span class="result-badge">평가 요소 만족</span> <b>제출용 수요·공급 곡선 그래프 (총 2개)</b></h3>', unsafe_allow_html=True)
                
                q_vals = np.linspace(10, 90, 100)
                d_base = 100 - q_vals
                s_base = q_vals

                # matplotlib 1행 2열 레이아웃 생성
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
                
                # [그래프 1: 현재 변동]
                ax1.plot(q_vals, d_base, label="원래 수요 (D)", color="#94a3b8", linestyle="--", alpha=0.6)
                ax1.plot(q_vals, s_base, label="원래 공급 (S)", color="#94a3b8", linestyle="--", alpha=0.6)
                ax1.plot(q_vals, d_base + cur_d, label="현재 수요 (D1)", color="#dc2626", linewidth=2)
                ax1.plot(q_vals, s_base + cur_s, label="현재 공급 (S1)", color="#2563eb", linewidth=2)
                if cur_d != 0:
                    ax1.annotate('', xy=(50 + cur_d, 50 + cur_d/2), xytext=(50, 50), arrowprops=dict(facecolor='#dc2626', shrink=0.1, width=1))
                if cur_s != 0:
                    ax1.annotate('', xy=(50 - cur_s/2, 50 + cur_s/2), xytext=(50, 50), arrowprops=dict(facecolor='#2563eb', shrink=0.1, width=1))
                ax1.set_title("① 현재 시장의 균형 이동", fontproperties=font_prop, fontsize=10, fontweight="bold")
                ax1.set_xlabel("수량 (Q)", fontproperties=font_prop, fontsize=8)
                ax1.set_ylabel("가격 (P)", fontproperties=font_prop, fontsize=8)
                ax1.legend(prop=font_prop, loc="upper right", fontsize=7)
                ax1.grid(True, linestyle=':', alpha=0.4)

                # [그래프 2: 미래 예측]
                # 미래 그래프는 현재 상태(d_base + cur_d, s_base + cur_s)를 기준으로 한 단계 더 이동시킴
                ax2.plot(q_vals, d_base + cur_d, label="현재 수요 (D1)", color="#94a3b8", linestyle="--", alpha=0.6)
                ax2.plot(q_vals, s_base + cur_s, label="현재 공급 (S1)", color="#94a3b8", linestyle="--", alpha=0.6)
                ax2.plot(q_vals, d_base + cur_d + fut_d, label="미래 수요 (D2)", color="#b91c1c", linewidth=2, linestyle="-")
                ax2.plot(q_vals, s_base + cur_s + fut_s, label="미래 공급 (S2)", color="#1d4ed8", linewidth=2, linestyle="-")
                if fut_d != 0:
                    ax2.annotate('', xy=(50 + cur_d + fut_d, 50 + cur_d/2 + fut_d/2), xytext=(50 + cur_d, 50 + cur_d/2), arrowprops=dict(facecolor='#b91c1c', shrink=0.1, width=1))
                if fut_s != 0:
                    ax2.annotate('', xy=(50 - cur_s/2 - fut_s/2, 50 + cur_s/2 + fut_s/2), xytext=(50 - cur_s/2, 50 + cur_s/2), arrowprops=dict(facecolor='#1d4ed8', shrink=0.1, width=1))
                ax2.set_title("② 미래 시장 변화 예측", fontproperties=font_prop, fontsize=10, fontweight="bold")
                ax2.set_xlabel("수량 (Q)", fontproperties=font_prop, fontsize=8)
                ax2.set_ylabel("가격 (P)", fontproperties=font_prop, fontsize=8)
                ax2.legend(prop=font_prop, loc="upper right", fontsize=7)
                ax2.grid(True, linestyle=':', alpha=0.4)
                
                plt.tight_layout()
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

                # --- AI 기사 출력 ---
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown('<h3><span class="result-badge">제출 양식 완벽 부합</span> <b>작성된 경제 기사 전문</b></h3>', unsafe_allow_html=True)
                st.markdown('<div style="line-height:1.8; font-size:0.95rem; color:#334155;">', unsafe_allow_html=True)
                st.markdown(ai_article)
                st.markdown('</div></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ 에러가 발생했습니다: {e}")