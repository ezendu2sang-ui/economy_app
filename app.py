import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
import urllib.request

# 1. 페이지 레이아웃 및 디자인 설정 (전체 화면 최적화)
st.set_page_config(page_title="경제 수행평가 유레카!", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght=400;500;600;700;800&display=swap');
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
    .card-box {
        background-color: white;
        padding: 1.8rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 한글 폰트 설정 (그래프 글자 깨짐 방지)
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
        <h1 style="font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0;">🧠 경제 수행평가 유레카! (스스로 완성형)</h1>
        <p style="font-size: 0.85rem; color: #64748b; margin: 5px 0 0 0;">AI 멘토의 안내와 생생한 예시를 참고하여 나만의 멋진 기사를 완성해 보세요.</p>
    </div>
""", unsafe_allow_html=True)

# --- 메인 화면 레이아웃 분할 ---
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown('<h3><span class="step-badge">STEP 1</span><b>조사한 경제 뉴스 입력</b></h3>', unsafe_allow_html=True)
    st.write("가져온 뉴스 기사의 제목และ 본문을 입력하면 AI 멘토가 분석 가이드를 제공합니다.")
    
    title_input = st.text_input("📍 뉴스 제목", placeholder="예시: 풍작으로 양파 공급 과잉, 농가 시름 깊어져")
    body_input = st.text_area("📍 뉴스 본문", placeholder="뉴스 내용을 이곳에 붙여넣으세요...", height=350)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if not title_input and not body_input:
        st.markdown("""
            <div class="card-box" style="text-align: center; padding: 6rem 2rem;">
                <h3 style="color: #3b82f6; font-size: 1.25rem;">💡 경제 탐구 멘토링 가동 준비 완료!</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 10px;">
                    왼쪽에 뉴스를 입력하면 정답을 그대로 복사해 주는 대신,<br>
                    <b>중학생 눈높이 원리 해설 📊 그래프 분석 📖 단어 사전 ✍️ 영역별 작성 가이드 및 예시</b>를<br>
                    안전하고 정돈된 하나의 리포트로 깔끔하게 펼쳐드립니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🕵️ AI 멘토가 기사 속 시장 경제 원리를 정밀 분석 중입니다..."):
            try:
                # 가이드라인이 중간에 깨지지 않도록 프롬프트 정제 및 구분선 최소화
                prompt = f"""
                너는 중학교 사회 선생님이자 친절한 경제 멘토야. 
                학생이 가져온 경제 뉴스를 바탕으로, 현재의 수요·공급 상태와 '미래의 타당한 예측'을 명확하게 도출해서 알려주렴.
                말투는 "~란다", "~요" 같은 다정한 선생님 말투를 써줘.

                [중요 경제학 원칙]: 
                기사에서 가격 변동의 '원인'이 공급 증가라면 수요는 '없음'이어야 해. 가격 하락으로 소비자가 반응하는 것은 '수요량의 변화'이므로 수요 곡선 자체를 움직이면 안 된단다! 원인 요인 하나만 확실하게 움직여줘.

                [입력 뉴스 제목]: {title_input}
                [입력 뉴스 본문]: {body_input}

                반드시 첫 줄에 그래프 제어를 위한 데이터를 아래 형식(대괄호 및 쉼표 구분)을 칼같이 지켜서 작성해야 해.
                [DATA] 상품명, 현재수요(증가/감소/없음), 현재공급(증가/감소/없음), 미래수요(증가/감소/없음), 미래공급(증가/감소/없음)
                예시: [DATA] 양파, 없음, 증가, 증가, 없음

                그 아래에는 기사 작성에 필요한 모든 가이드를 문단이 찢어지지 않게 하나의 흐름으로 작성해줘:
                ===GUIDE_START===
                ## 📊 AI 멘토의 수행평가 안내서

                ### 1. 🔍 중학생 눈높이 원리 해설
                * **어떤 상품 시장의 이야기인가요?**: 기사 속 주인공이 되는 상품 시장 설명
                * **수요·공급 원리 쉽게 이해하기**: 현재 기사에서 수요나 공급 중 '단 하나'의 요인이 왜 움직였는지 비유를 들어 아주 쉽게 설명
                
                ### 2. 📖 기사 속 '어려운 경제 용어' 쏙쏙 사전
                기사 본문에 나오는 생소한 어휘나 경제 용어를 2개 골라 뜻을 중학생 눈높이로 쉽게 풀이

                ### 3. ✍️ 나만의 기사 작성하기! 영역별 꿀팁 가이드 및 예시
                
                #### 📌 [표제(제목) 작성 가이드]
                * **💡 참신한 표제 예시**: 핵심 요약 제목 2개

                #### 📌 [전문(3줄 요약) 작성 가이드]
                * **💡 3줄 전문 예시**: 조건에 맞춘 완성형 3줄 전문 예시

                #### 📌 [본문 작성 가이드 (그래프 필수 활용)]
                * **💡 완벽한 본문 예시**: 현재 분석과 미래 예측이 매끄럽게 연결된 줄글 본문 예시
                ===GUIDE_END===
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                full_response = response.choices[0].message.content

                # 데이터 파싱
                lines = full_response.split('\n')
                data_line = [line for line in lines if "[DATA]" in line]
                
                product_name = "상품"
                cur_d, cur_s, fut_d, fut_s = 0, 0, 0, 0
                
                if data_line:
                    try:
                        raw_str = data_line[0].split("[DATA]")[1].strip()
                        raw_data = [x.strip() for x in raw_str.split(",")]
                        product_name = raw_data[0]
                        
                        if "증가" in raw_data[1]: cur_d = 20
                        elif "감소" in raw_data[1]: cur_d = -20
                        if "증가" in raw_data[2]: cur_s = 20
                        elif "감소" in raw_data[2]: cur_s = -20
                        
                        if "증가" in raw_data[3]: fut_d = 20
                        elif "감소" in raw_data[3]: fut_d = -20
                        if "증가" in raw_data[4]: fut_s = 20
                        elif "감소" in raw_data[4]: fut_s = -20
                    except Exception as e:
                        pass
                
                # 가이드 내용 추출 (텍스트 끊김 현상 방지)
                ai_guide = full_response
                if "===GUIDE_START===" in ai_guide:
                    ai_guide = ai_guide.split("===GUIDE_START===")[1]
                if "===GUIDE_END===" in ai_guide:
                    ai_guide = ai_guide.split("===GUIDE_END===")[0]
                ai_guide = ai_guide.strip()

                # 1. 상단 해설 및 하단 가이드를 쪼개지 않고 상단 박스에 우선 깔끔하게 배치
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown(ai_guide)
                st.markdown('</div>', unsafe_allow_html=True)

                # 2. 중앙 그래프 시각화 (★텍스트 출력 버그 삭제 + 3단 균형 누적 연계 표기★)
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown('<h3><span class="result-badge">수행평가 차트 연계</span> <b>시각화 가이드: 균형점의 역사적 이동 ($P_0 \\rightarrow P_1 \\rightarrow P_2$)</b></h3>', unsafe_allow_html=True)
                
                q_vals = np.linspace(0, 100, 100)
                d_base = 100 - q_vals
                s_base = q_vals

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
                
                # 균형점 계산 헬퍼 함수
                def get_equilibrium(d_sh, s_sh):
                    q_eq = (100 + d_sh + s_sh) / 2
                    p_eq = q_eq - s_sh
                    return q_eq, p_eq

                q0, p0 = get_equilibrium(0, 0)
                q1, p1 = get_equilibrium(cur_d, cur_s)
                q2, p2 = get_equilibrium(cur_d + fut_d, cur_s + fut_s)

                # --- ① 현재 그래프 (원래 상태와 현재 상태의 대비) ---
                ax1.plot(q_vals, d_base, color="#cbd5e1", linestyle="--", alpha=0.7, label="원래 수요(D)")
                ax1.plot(q_vals, s_base, color="#cbd5e1", linestyle="--", alpha=0.7, label="원래 공급(S)")
                
                d_current = 100 - (q_vals - cur_d)
                s_current = q_vals - cur_s
                ax1.plot(q_vals, d_current, color="#e11d48", linewidth=2.2, label="현재 수요(D1)")
                ax1.plot(q_vals, s_current, color="#2563eb", linewidth=2.2, label="현재 공급(S1)")
                
                # [균형 0 표시]
                ax1.plot([0, q0], [p0, p0], color="#94a3b8", linestyle=":", linewidth=1)
                ax1.plot([q0, q0], [0, p0], color="#94a3b8", linestyle=":", linewidth=1)
                ax1.text(-7, p0-2, "$P_0$", fontsize=10, fontweight="bold", fontproperties=font_prop)
                ax1.text(q0-2, -7, "$Q_0$", fontsize=10, fontweight="bold", fontproperties=font_prop)
                ax1.scatter(q0, p0, color="#475569", s=35, zorder=5)

                # [균형 1 표시]
                if cur_d != 0 or cur_s != 0:
                    ax1.plot([0, q1], [p1, p1], color="#ea580c", linestyle=":", linewidth=1.2)
                    ax1.plot([q1, q1], [0, p1], color="#ea580c", linestyle=":", linewidth=1.2)
                    ax1.text(-7, p1-2, "$P_1$", fontsize=10, color="#ca8a04", fontweight="bold", fontproperties=font_prop)
                    ax1.text(q1-2, -7, "$Q_1$", fontsize=10, color="#ca8a04", fontweight="bold", fontproperties=font_prop)
                    ax1.scatter(q1, p1, color="#ea580c", s=45, zorder=5)
                    
                    # 이동 화살표 주석
                    if cur_d != 0:
                        x_st = 35 if cur_d > 0 else 65
                        ax1.annotate('', xy=(x_st + cur_d, 100 - x_st), xytext=(x_st, 100 - x_st),
                                     arrowprops=dict(facecolor='#e11d48', edgecolor='none', width=1.5, headwidth=6, shrink=0.02))
                    if cur_s != 0:
                        x_st = 35 if cur_s > 0 else 65
                        ax1.annotate('', xy=(x_st + cur_s, x_st), xytext=(x_st, x_st),
                                     arrowprops=dict(facecolor='#2563eb', edgecolor='none', width=1.5, headwidth=6, shrink=0.02))

                ax1.set_title(f"① 현재 {product_name} 시장의 균형 이동", fontproperties=font_prop, fontsize=11, fontweight="bold")
                ax1.set_xlim(0, 100), ax1.set_ylim(0, 100)
                ax1.set_xlabel("수량 (Q)", fontproperties=font_prop), ax1.set_ylabel("가격 (P)", fontproperties=font_prop)
                ax1.legend(prop=font_prop, loc="upper right", fontsize=8)
                ax1.grid(True, linestyle=':', alpha=0.2)

                # --- ② 미래 예측 그래프 (★0, 1, 2번 균형이 누적으로 모두 누적 표시되도록 변경★) ---
                ax2.plot(q_vals, d_base, color="#e2e8f0", linestyle=":", alpha=0.5) # 점선 가이드
                ax2.plot(q_vals, s_base, color="#e2e8f0", linestyle=":", alpha=0.5)
                ax2.plot(q_vals, d_current, color="#fca5a5", linestyle="--", alpha=0.6, label="현재 수요(D1)")
                ax2.plot(q_vals, s_current, color="#93c5fd", linestyle="--", alpha=0.6, label="현재 공급(S1)")
                
                d_future = 100 - (q_vals - cur_d - fut_d)
                s_future = q_vals - cur_s - fut_s
                ax2.plot(q_vals, d_future, color="#b91c1c", linewidth=2.5, label="미래 수요(D2)")
                ax2.plot(q_vals, s_future, color="#1d4ed8", linewidth=2.5, label="미래 공급(S2)")
                
                # [원래 균형 점선 표시]
                ax2.plot([0, q0], [p0, p0], color="#cbd5e1", linestyle=":", linewidth=0.8)
                ax2.plot([q0, q0], [0, p0], color="#cbd5e1", linestyle=":", linewidth=0.8)
                ax2.text(-7, p0-2, "$P_0$", fontsize=9, color="#94a3b8", fontproperties=font_prop)
                ax2.text(q0-2, -7, "$Q_0$", fontsize=9, color="#94a3b8", fontproperties=font_prop)
                ax2.scatter(q0, p0, color="#cbd5e1", s=25, zorder=4)

                # [현재 균형 점선 표시]
                ax2.plot([0, q1], [p1, p1], color="#94a3b8", linestyle=":", linewidth=1)
                ax2.plot([q1, q1], [0, p1], color="#94a3b8", linestyle=":", linewidth=1)
                ax2.text(-7, p1-2, "$P_1$", fontsize=10, color="#64748b", fontproperties=font_prop)
                ax2.text(q1-2, -7, "$Q_1$", fontsize=10, color="#64748b", fontproperties=font_prop)
                ax2.scatter(q1, p1, color="#64748b", s=35, zorder=4)

                # [미래 최종 균형 점선 표시]
                if fut_d != 0 or fut_s != 0:
                    ax2.plot([0, q2], [p2, p2], color="#b91c1c" if fut_d!=0 else "#1d4ed8", linestyle=":", linewidth=1.2)
                    ax2.plot([q2, q2], [0, p2], color="#b91c1c" if fut_d!=0 else "#1d4ed8", linestyle=":", linewidth=1.2)
                    ax2.text(-7, p2-2, "$P_2$", fontsize=10, color="#b91c1c" if fut_d!=0 else "#1d4ed8", fontweight="bold", fontproperties=font_prop)
                    ax2.text(q2-2, -7, "$Q_2$", fontsize=10, color="#b91c1c" if fut_d!=0 else "#1d4ed8", fontweight="bold", fontproperties=font_prop)
                    ax2.scatter(q2, p2, color="#b91c1c" if fut_d!=0 else "#1d4ed8", s=55, zorder=5)
                    
                    if fut_d != 0:
                        x_st = 35 if fut_d > 0 else 65
                        ax2.annotate('', xy=(x_st + cur_d + fut_d, 100 - x_st), xytext=(x_st + cur_d, 100 - x_st),
                                     arrowprops=dict(facecolor='#b91c1c', edgecolor='none', width=1.5, headwidth=6, shrink=0.02))
                    if fut_s != 0:
                        x_st = 35 if fut_s > 0 else 65
                        ax2.annotate('', xy=(x_st + cur_s + fut_s, x_st), xytext=(x_st + cur_s, x_st),
                                     arrowprops=dict(facecolor='#1d4ed8', edgecolor='none', width=1.5, headwidth=6, shrink=0.02))

                ax2.set_title(f"② 미래 {product_name} 시장 예측 이동", fontproperties=font_prop, fontsize=11, fontweight="bold")
                ax2.set_xlim(0, 100), ax2.set_ylim(0, 100)
                ax2.set_xlabel("수량 (Q)", fontproperties=font_prop), ax2.set_ylabel("가격 (P)", fontproperties=font_prop)
                ax2.legend(prop=font_prop, loc="upper right", fontsize=8)
                ax2.grid(True, linestyle=':', alpha=0.2)

                plt.tight_layout()
                
                # ★[버그 픽스] 상단 텍스트 표기 방지를 위해 명시적으로 출력 제어 및 close 처리★
                st.pyplot(fig)
                plt.close(fig)
                
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ 에러가 발생했습니다: {e}")