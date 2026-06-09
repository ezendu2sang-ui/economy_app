import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
import urllib.request

# 1. 페이지 레이아웃 및 디자인 설정
st.set_page_config(page_title="경제 수행평가 유레카!", layout="wide")

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
        background-color: #3b82f6;
        color: white;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        margin-right: 0.5rem;
    }
    .result-badge {
        background-color: #eff6ff;
        color: #1e40af;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
    }
    .dictionary-badge {
        background-color: #fef3c7;
        color: #92400e;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
    }
    .guide-badge {
        background-color: #f5f3ff;
        color: #5b21b6;
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
        <h1 style="font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0;">🧠 경제 수행평가 유레카! (스스로 학습형)</h1>
        <p style="font-size: 0.85rem; color: #64748b; margin: 5px 0 0 0;">기사를 분석하고 원리를 이해하여 나만의 수행평가 기사를 완성해 보세요.</p>
    </div>
""", unsafe_allow_html=True)

# --- 메인 화면 레이아웃 분할 ---
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown('<h3><span class="step-badge">STEP 1</span><b>조사한 경제 뉴스 입력</b></h3>', unsafe_allow_html=True)
    st.write("가져온 뉴스 기사의 제목과 본문을 입력하면 AI 멘토가 원리를 설명해 줍니다.")
    
    title_input = st.text_input("📍 뉴스 제목", placeholder="예시: 기상이변으로 원두 생산 비상, 커피값 오르나")
    body_input = st.text_area("📍 뉴스 본문", placeholder="뉴스 내용을 이곳에 붙여넣으세요...", height=300)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if not title_input and not body_input:
        st.markdown("""
            <div class="card-box" style="text-align: center; padding: 5rem 2rem;">
                <h3 style="color: #3b82f6; font-size: 1.25rem;">💡 경제 탐구 가이드 가동 준비 완료!</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 10px;">
                    왼쪽에 뉴스를 입력하면 정답을 통째로 주는 대신,<br>
                    <b>중학생 눈높이 해설 ➡️ 어려운 용어 사전 ➡️ 변동 그래프 2개 ➡️ 직접 쓰기 꿀팁</b> 순서로<br>
                    공부하며 생각할 수 있는 멋진 가이드를 열어드립니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🕵️ AI 멘토가 기사 속 시장 경제 원리를 분석하는 중입니다..."):
            try:
                # 학생이 스스로 생각하게 만드는 가이드형 프롬프트
                prompt = f"""
                너는 중학교 사회 선생님이자 친절한 경제 멘토야. 
                학생이 가져온 경제 뉴스를 분석해서 스스로 수행평가(경제 기사 작성)를 완성할 수 있도록 '학습 가이드라인'을 제공해 주렴.
                절대로 완성된 기사를 통째로 작성해 주지 말고, 원리를 이해시키는 데 집중해줘. 말투는 "~란다", "~요" 같은 다정한 선생님 말투를 써줘.

                [입력 뉴스 제목]: {title_input}
                [입력 뉴스 본문]: {body_input}

                출력할 때 맨 첫 줄에 그래프 제어용 데이터를 반드시 아래 형식을 정확히 지켜서 작성해줘. (가이드 본문에는 포함하지 마)
                [DATA] 상품명, 현재수요(증가/감소/없음), 현재공급(증가/감소/없음), 미래수요(증가/감소/없음), 미래공급(증가/감소/없음)
                예시: [DATA] 커피, 없음, 감소, 증가, 없음

                그 아래에는 구분선(---)을 긋고 아래 목차대로 내용을 채워줘:
                ---
                ### 1. 🔍 중학생 눈높이 원리 해설
                * **어떤 시장 이야기인가요?**: (기사 속 상품 시장이 무엇인지 설명)
                * **현재의 수요와 공급 변동**: (수요나 공급 중 무엇이 왜 움직였는지 중학생이 이해하기 쉽게 비유를 들어 설명)
                * **가격과 거래량은 어떻게 되었나요?**: (수요·공급 법칙에 따라 균형 가격과 거래량이 변한 원리를 설명)
                
                ### 2. 📖 기사 속 '어려운 경제 용어' 쏙쏙 사전
                (기사 본문이나 해설에 나온 어려운 경제 단어나 한자어 용어를 2~3개 골라 뜻을 아주 쉽게 풀이해줘)

                ### 3. ✍️ 나만의 기사 작성하기! 꿀팁 가이드
                (수행평가 양식인 표제, 전문, 본문을 잘 쓰기 위한 힌트나 질문을 던져줘)
                * **[표제(제목) 힌트]**: (뉴스 제목을 그대로 베끼지 않고 '수요·공급' 단어가 연상되도록 참신하게 짓는 팁 제안)
                * **[전문(요약) 힌트]**: (전문 3줄에 꼭 들어가야 할 핵심 포인트 짚어주기)
                * **[본문 작성 가이드]**: (현재 원인 분석과 미래 예측을 글로 풀어낼 때 서술해야 하는 논리적 흐름이나 질문 던져주기)
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                full_response = response.choices[0].message.content

                # 데이터 파싱
                lines = full_response.split('\n')
                data_line = [line for line in lines if line.startswith("[DATA]")]
                
                product_name = "해당 상품"
                cur_d, cur_s, fut_d, fut_s = 0, 0, 0, 0
                
                if data_line:
                    try:
                        raw_data = data_line[0].replace("[DATA]", "").strip().split(",")
                        product_name = raw_data[0].strip()
                        
                        if "증가" in raw_data[1]: cur_d = 20
                        elif "감소" in raw_data[1]: cur_d = -20
                        if "증가" in raw_data[2]: cur_s = 20
                        elif "감소" in raw_data[2]: cur_s = -20
                        
                        if "증가" in raw_data[3]: fut_d = 20
                        elif "감소" in raw_data[3]: fut_d = -20
                        if "증가" in raw_data[4]: fut_s = 20
                        elif "감소" in raw_data[4]: fut_s = -20
                    except:
                        pass
                
                # 가이드 텍스트 분리
                ai_guide = "\n".join([line for line in lines if not line.startswith("[DATA]")])
                if "---" in ai_guide:
                    ai_guide = ai_guide.split("---", 1)[1].strip()

                # 텍스트 영역별 분할 파싱 (사전, 가이드 박스 디자인화용)
                parts = ai_guide.split("###")
                part_explain = ""
                part_dict = ""
                part_write_guide = ""
                
                for p in parts:
                    if "1. 🔍" in p or "1. " in p: part_explain = p
                    elif "2. 📖" in p or "2. " in p: part_dict = p
                    elif "3. ✍️" in p or "3. " in p: part_write_guide = p

                # 4. 해설 영역 출력
                if part_explain:
                    st.markdown('<div class="card-box">', unsafe_allow_html=True)
                    st.markdown(f"### {part_explain.strip()}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # 5. 그래프 2개 시각화 영역 출력
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown('<h3><span class="result-badge">수행평가 핵심</span> <b>생각을 돕는 수요·공급 곡선 (2가지 상황)</b></h3>', unsafe_allow_html=True)
                st.write("AI 멘토가 그린 그래프를 보며 시장 균형이 어떻게 움직였는지 관찰해 보세요.")
                
                q_vals = np.linspace(10, 90, 100)
                d_base = 100 - q_vals
                s_base = q_vals

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
                
                # [그래프 1: 현재 상황]
                ax1.plot(q_vals, d_base, color="#94a3b8", linestyle="--", alpha=0.5, label="원래 수요(D)")
                ax1.plot(q_vals, s_base, color="#94a3b8", linestyle="--", alpha=0.5, label="원래 공급(S)")
                ax1.plot(q_vals, d_base + cur_d, color="#dc2626", linewidth=2, label="현재 수요(D1)")
                ax1.plot(q_vals, s_base + cur_s, color="#2563eb", linewidth=2, label="현재 공급(S1)")
                if cur_d != 0:
                    ax1.annotate('', xy=(50 + cur_d, 50 + cur_d/2), xytext=(50, 50), arrowprops=dict(facecolor='#dc2626', shrink=0.1, width=1))
                if cur_s != 0:
                    ax1.annotate('', xy=(50 - cur_s/2, 50 + cur_s/2), xytext=(50, 50), arrowprops=dict(facecolor='#2563eb', shrink=0.1, width=1))
                ax1.set_title(f"① 현재 {product_name} 시장의 변동", fontproperties=font_prop, fontsize=10, fontweight="bold")
                ax1.set_xlabel("수량 (Q)", fontproperties=font_prop, fontsize=8)
                ax1.set_ylabel("가격 (P)", fontproperties=font_prop, fontsize=8)
                ax1.legend(prop=font_prop, loc="upper right", fontsize=7)
                ax1.grid(True, linestyle=':', alpha=0.3)

                # [그래프 2: 미래 예측 상황]
                ax2.plot(q_vals, d_base + cur_d, color="#94a3b8", linestyle="--", alpha=0.5, label="현재 수요(D1)")
                ax2.plot(q_vals, s_base + cur_s, color="#94a3b8", linestyle="--", alpha=0.5, label="현재 공급(S1)")
                ax2.plot(q_vals, d_base + cur_d + fut_d, color="#b91c1c", linewidth=2, label="미래 수요(D2)")
                ax2.plot(q_vals, s_base + cur_s + fut_s, color="#1d4ed8", linewidth=2, label="미래 공급(S2)")
                if fut_d != 0:
                    ax2.annotate('', xy=(50 + cur_d + fut_d, 50 + cur_d/2 + fut_d/2), xytext=(50 + cur_d, 50 + cur_d/2), arrowprops=dict(facecolor='#b91c1c', shrink=0.1, width=1))
                if fut_s != 0:
                    ax2.annotate('', xy=(50 - cur_s/2 - fut_s/2, 50 + cur_s/2 + fut_s/2), xytext=(50 - cur_s/2, 50 + cur_s/2), arrowprops=dict(facecolor='#1d4ed8', shrink=0.1, width=1))
                ax2.set_title(f"② 미래 {product_name} 시장 예측", fontproperties=font_prop, fontsize=10, fontweight="bold")
                ax2.set_xlabel("수량 (Q)", fontproperties=font_prop, fontsize=8)
                ax2.set_ylabel("가격 (P)", fontproperties=font_prop, fontsize=8)
                ax2.legend(prop=font_prop, loc="upper right", fontsize=7)
                ax2.grid(True, linestyle=':', alpha=0.3)

                plt.tight_layout()
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

                # 6. 용어 사전 출력
                if part_dict:
                    st.markdown('<div class="card-box" style="background-color: #fffbeb; border: 1px solid #fef3c7;">', unsafe_allow_html=True)
                    st.markdown(f"### {part_dict.strip()}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # 7. 기사 작성 가이드 출력
                if part_write_guide:
                    st.markdown('<div class="card-box" style="background-color: #faf5ff; border: 1px solid #f3e8ff;">', unsafe_allow_html=True)
                    st.markdown(f"### {part_write_guide.strip()}")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ 에러가 발생했습니다: {e}")