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
    st.write("가져온 뉴스 기사의 제목과 본문을 입력하면 AI 멘토가 분석 가이드를 제공합니다.")
    
    title_input = st.text_input("📍 뉴스 제목", placeholder="예시: 기상이변으로 원두 생산 비상, 커피값 오르나")
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
                # 그래프 연동 및 예시 도출 극대화 프롬프트
                prompt = f"""
                너는 중학교 사회 선생님이자 친절한 경제 멘토야. 
                학생이 가져온 경제 뉴스를 바탕으로, 현재의 수요·공급 상태와 '미래의 타당한 예측'을 명확하게 도출해서 알려주렴.
                말투는 "~란다", "~요" 같은 다정한 선생님 말투를 써줘.

                [입력 뉴스 제목]: {title_input}
                [입력 뉴스 본문]: {body_input}

                반드시 첫 줄에 그래프 제어를 위한 데이터를 아래 형식(대괄호 및 쉼표 구분)을 칼같이 지켜서 작성해야 해. 
                미래 예측은 기사 내용에 직접 없더라도 선호도 변화, 기술 변화, 소득 변화 등 타당한 경제학적 근거를 바탕으로 상상하여 예측 데이터를 무조건 만들어줘.
                [DATA] 상품명, 현재수요(증가/감소/없음), 현재공급(증가/감소/없음), 미래수요(증가/감소/없음), 미래공급(증가/감소/없음)
                예시: [DATA] 커피, 없음, 감소, 증가, 없음

                그 아래에는 구분선(---)을 긋고 아래 양식을 토대로 생생한 가이드라인과 예시를 모두 작성해줘:
                ---
                ## 📊 AI 멘토의 수행평가 안내서

                ### 1. 🔍 중학생 눈높이 원리 해설
                * **어떤 상품 시장의 이야기인가요?**: (기사 속 주인공이 되는 상품 시장 설명)
                * **수요·공급 원리 쉽게 이해하기**: (현재 기사에서 수요나 공급 중 어떤 요인이 왜 움직였는지 비유를 들어 아주 쉽게 설명)
                
                ### 2. 📖 기사 속 '어려운 경제 용어' 쏙쏙 사전
                (기사 본문에 나오는 생소한 어휘나 경제 용어를 2개 골라 뜻을 중학생 눈높이로 쉽게 풀이)

                ### 3. ✍️ 나만의 기사 작성하기! 영역별 꿀팁 가이드 & 예시
                
                #### 📌 [표제(제목) 작성 가이드]
                * **작성 안내**: 단순히 뉴스의 원래 제목을 받아 적으면 감점 요인이 된단다! 기사 내용을 잘 관통하면서, **'수요'나 '공급'이라는 단어가 직접 연상되거나 포함되도록** 참신하게 제목을 지어보렴.
                * **💡 참신한 표제 예시**: 
                  (여기에 이 기사를 바탕으로 '수요'나 '공급'이라는 핵심 단어가 포함된 멋진 기사 제목 예시를 2개 제안해줘)

                #### 📌 [전문(3줄 요약) 작성 가이드]
                * **작성 안내**: 전문은 바쁜 독자들을 위해 기사 전체를 읽지 않아도 핵심을 알 수 있게 요약하는 코너야. 반드시 **[1) 현재 시장의 변동 원인, 2) 그로 인한 현재 가격과 거래량 결과, 3) 미래에 예상되는 추가 변화나 최종 가격 예측]**의 3가지 요소가 각각 한 줄씩 논리적인 인과관계로 들어가야 완점 점수를 받는단다.
                * **💡 3줄 전문 예시**: 
                  (위의 3가지 조건을 철저히 지켜서 이 기사에 딱 맞는 완성형 3줄 전문 예시를 보기 좋게 작성해줘)

                #### 📌 [본문 작성 가이드 (그래프 필수 활용)]
                * **작성 안내**: 본문을 작성할 때는 아래에 AI 멘토가 그려준 **[① 현재 그래프]와 [② 미래 예측 그래프]를 본문에 꼭 첨부하고 설명**해야 해! 글 속에는 곡선이 오른쪽이나 왼쪽 중 어느 방향으로 움직였는지(이동) 언급해 주렴. 
                특히, **"현재는 [어떤 요인] 때문에 수요·공급이 변해 가격이 [상승/하락]하는 결과가 나타났지만, 미래에는 새로운 [수요/공급 변동 요인(선호도, 대체재 등)]이 작동하여 최종적으로 시장 가격과 거래량이 [어떻게] 될 것이다"**라는 과학적인 원인과 결과를 줄글로 멋지게 서술해야 한단다.
                * **💡 완벽한 본문 예시**: 
                  (학생들이 보고 서술 흐름을 모방하여 공부할 수 있도록, 현재 분석과 미래 예측이 경제학적 인과관계로 매끄럽게 연결된 훌륭한 본문 글 예시를 완성도 있게 작성해줘)
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                full_response = response.choices[0].message.content

                # 데이터 파싱 고도화
                lines = full_response.split('\n')
                data_line = [line for line in lines if line.strip().startswith("[DATA]")]
                
                product_name = "해당 상품"
                cur_d, cur_s, fut_d, fut_s = 0, 0, 0, 0
                
                if data_line:
                    try:
                        raw_data = data_line[0].replace("[DATA]", "").strip().split(",")
                        product_name = raw_data[0].strip()
                        
                        # 현재 1단계 시프트 값
                        if "증가" in raw_data[1]: cur_d = 20
                        elif "감소" in raw_data[1]: cur_d = -20
                        if "증가" in raw_data[2]: cur_s = 20
                        elif "감소" in raw_data[2]: cur_s = -20
                        
                        # 미래 2단계 추가 시프트 값
                        if "증가" in raw_data[3]: fut_d = 20
                        elif "감소" in raw_data[3]: fut_d = -20
                        if "증가" in raw_data[4]: fut_s = 20
                        elif "감소" in raw_data[4]: fut_s = -20
                    except Exception as e:
                        pass
                
                # 가이드 텍스트 순수 분리
                ai_guide = "\n".join([line for line in lines if not line.strip().startswith("[DATA]")])
                if "---" in ai_guide:
                    ai_guide = ai_guide.split("---", 1)[1].strip()

                # 레이아웃 쪼개짐 방지용 안전 장치 분할
                intro_part = ai_guide.split("### 3. ✍️")[0].strip() if "### 3. ✍️" in ai_guide else ai_guide
                guide_part = "### 3. ✍️ " + ai_guide.split("### 3. ✍️")[1].strip() if "### 3. ✍️" in ai_guide else ""

                # 1. 상단 해설서 상자 출력
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown(intro_part)
                st.markdown('</div>', unsafe_allow_html=True)

                # 2. 중앙 정밀 그래프 2개 시각화 (미래 예측 연동 보정 완료)
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.markdown('<h3><span class="result-badge">수행평가 차트 연계</span> <b>시각화 가이드: 단계별 곡선 변화 (2가지 상황)</b></h3>', unsafe_allow_html=True)
                st.write("오른쪽 화살표 방향을 잘 관찰하세요. 미래 그래프는 이미 변동된 현재 곡선(D1, S1)을 바탕으로 추가 이동(D2, S2)을 시작합니다.")
                
                q_vals = np.linspace(10, 90, 100)
                d_base = 100 - q_vals
                s_base = q_vals

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))
                
                # --- ① 현재 그래프 (원래 점선 -> 현재 실선 이동) ---
                ax1.plot(q_vals, d_base, color="#cbd5e1", linestyle="--", alpha=0.7, label="원래 수요(D)")
                ax1.plot(q_vals, s_base, color="#cbd5e1", linestyle="--", alpha=0.7, label="원래 공급(S)")
                ax1.plot(q_vals, d_base + cur_d, color="#e11d48", linewidth=2.5, label="현재 수요(D1)")
                ax1.plot(q_vals, s_base + cur_s, color="#2563eb", linewidth=2.5, label="현재 공급(S1)")
                
                # 화살표 좌표 자동 매칭 (중앙 50 근처에서 곡선 이동 방향으로 발사)
                if cur_d != 0:
                    ax1.annotate('', xy=(50 + cur_d, 50 - (50+cur_d) + 100), xytext=(50, 50),
                                 arrowprops=dict(facecolor='#e11d48', edgecolor='#be123c', shrink=0.05, width=1.8, headwidth=6))
                if cur_s != 0:
                    ax1.annotate('', xy=(50 - cur_s, 50 + cur_s), xytext=(50, 50),
                                 arrowprops=dict(facecolor='#2563eb', edgecolor='#1d4ed8', shrink=0.05, width=1.8, headwidth=6))
                
                ax1.set_title(f"① 현재 {product_name} 시장의 균형 이동", fontproperties=font_prop, fontsize=10, fontweight="bold")
                ax1.set_xlabel("수량 (Q)", fontproperties=font_prop, fontsize=8)
                ax1.set_ylabel("가격 (P)", fontproperties=font_prop, fontsize=8)
                ax1.legend(prop=font_prop, loc="upper right", fontsize=7)
                ax1.grid(True, linestyle=':', alpha=0.3)

                # --- ② 미래 예측 그래프 (현재의 최종 곡선이 점선 베이스가 됨 -> 미래 최종 실선 이동) ---
                # 현재 상태(D1, S1)를 연한 가이드 점선으로 시각화
                ax2.plot(q_vals, d_base + cur_d, color="#fca5a5", linestyle="--", alpha=0.7, label="현재 수요(D1)")
                ax2.plot(q_vals, s_base + cur_s, color="#93c5fd", linestyle="--", alpha=0.7, label="현재 공급(S1)")
                
                # 미래 예측 결과(D2, S2)를 가장 두꺼운 실선으로 표현
                ax2.plot(q_vals, d_base + cur_d + fut_d, color="#b91c1c", linewidth=2.8, label="미래 수요(D2)")
                ax2.plot(q_vals, s_base + cur_s + fut_s, color="#1d4ed8", linewidth=2.8, label="미래 공급(S2)")
                
                # 미래 화살표: 현재 위치(D1, S1 기반)에서 출발해서 미래 위치(D2, S2 기반)로 정밀 조준 발사
                if fut_d != 0:
                    ax2.annotate('', xy=(50 + cur_d + fut_d, 50 - (50+cur_d+fut_d) + 100), xytext=(50 + cur_d, 50 - (50+cur_d) + 100),
                                 arrowprops=dict(facecolor='#b91c1c', edgecolor='#7f1d1d', shrink=0.05, width=1.8, headwidth=6))
                if fut_s != 0:
                    ax2.annotate('', xy=(50 - cur_s - fut_s, 50 + cur_s + fut_s), xytext=(50 - cur_s, 50 + cur_s),
                                 arrowprops=dict(facecolor='#1d4ed8', edgecolor='#1e3a8a', shrink=0.05, width=1.8, headwidth=6))
                
                ax2.set_title(f"② 미래 {product_name} 시장 예측 이동", fontproperties=font_prop, fontsize=10, fontweight="bold")
                ax2.set_xlabel("수량 (Q)", fontproperties=font_prop, fontsize=8)
                ax2.set_ylabel("가격 (P)", fontproperties=font_prop, fontsize=8)
                ax2.legend(prop=font_prop, loc="upper right", fontsize=7)
                ax2.grid(True, linestyle=':', alpha=0.3)

                plt.tight_layout()
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

                # 3. 하단 기사 작성 가이드 및 생생한 인과관계 예시 박스 출력
                if guide_part:
                    st.markdown('<div class="card-box" style="background-color: #faf5ff; border: 1px solid #e9d5ff;">', unsafe_allow_html=True)
                    st.markdown(guide_part)
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ 에러가 발생했습니다: {e}")