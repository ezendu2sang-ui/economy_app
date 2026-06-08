import json
import matplotlib.pyplot as plt
import streamlit as st
from openai import OpenAI

# Streamlit 서버의 Secrets에서 키를 안전하게 가져옵니다.
client = OpenAI(api_key=st.secrets["YOUR_OPENAI_API_KEY"])

def analyze_economic_article(article_text):
    prompt = f"""
    당신은 경제학 교사입니다. 다음 경제 기사를 분석하여 중고등학생들이 이해하기 쉽게 요약하고, 
    수요와 공급의 법칙 중 어떤 케이스에 해당하느지 분석해주세요.
    
    [기사 내용]
    {article_text}
    
    반환 형식은 반드시 아래의 JSON 포맷으로만 출력해주세요. 다른 설명은 금지합니다.
    {{
        "commodity": "분석 대상 상품명",
        "cause": "가격 변동의 원인 한 줄 요약",
        "result": "결과 및 예측 한 줄 요약",
        "market_type": "D_INCREASE" 또는 "D_DECREASE" 또는 "S_INCREASE" ("S_DECREASE" 중 하나)
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def draw_market_chart(analysis_result):
    commodity = analysis_result['commodity']
    market_type = analysis_result['market_type']
    
    fig, ax = plt.subplots(figsize=(5, 5))
    x = [2, 4, 6, 8]
    d_original = [8, 6, 4, 2]
    s_original = [2, 4, 6, 8]
    
    ax.plot(x, d_original, label='D (Original)', color='blue', linestyle='--')
    ax.plot(x, s_original, label='S (Original)', color='orange', linestyle='--')
    
    title_suffix = ""
    if market_type == "D_INCREASE":
        d_new = [10, 8, 6, 4]
        ax.plot(x, d_new, label="D' (Increased)", color='blue', linewidth=2)
        ax.annotate('', xy=(5, 7), xytext=(4, 6), arrowprops=dict(facecolor='blue', shrink=0.05))
        title_suffix = "수요 증가"
    elif market_type == "D_DECREASE":
        d_new = [6, 4, 2, 0]
        ax.plot(x, d_new, label="D' (Decreased)", color='blue', linewidth=2)
        ax.annotate('', xy=(3, 3), xytext=(4, 4), arrowprops=dict(facecolor='blue', shrink=0.05))
        title_suffix = "수요 감소"
    elif market_type == "S_INCREASE":
        s_new = [0, 2, 4, 6]
        ax.plot(x, s_new, label="S' (Increased)", color='orange', linewidth=2)
        ax.annotate('', xy=(5, 3), xytext=(4, 4), arrowprops=dict(facecolor='orange', shrink=0.05))
        title_suffix = "공급 증가"
    elif market_type == "S_DECREASE":
        s_new = [4, 6, 8, 10]
        ax.plot(x, s_new, label="S' (Decreased)", color='orange', linewidth=2)
        ax.annotate('', xy=(3, 5), xytext=(4, 4), arrowprops=dict(facecolor='orange', shrink=0.05))
        title_suffix = "공급 감소"

    ax.set_title(f"Market: {commodity} ({title_suffix})")
    ax.set_xlabel("Quantity (Q)")
    ax.set_ylabel("Price (P)")
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    return fig

# --- 앱 UI 구성 ---
st.title("📊 경제 수행평가 도우미 앱")
st.caption("경제 기사를 입력하면 수요·공급 변화를 분석하고 그래프를 그려줍니다.")

user_article = st.text_area("여기에 분석하고 싶은 경제 뉴스를 붙여넣으세요:", height=150)

if st.button("🚀 수요·공급 분석하기", use_container_width=True):
    if not user_article.strip():
        st.warning("기사 내용을 입력해주세요!")
    else:
        with st.spinner("AI가 기사를 분석하고 그래프를 그리는 중..."):
            try:
                analysis = analyze_economic_article(user_article)
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("### 📌 수행평가 리포트")
                    st.markdown(f"**🛒 상품:** `{analysis['commodity']}`")
                    st.info(f"**🔍 원인:**\n{analysis['cause']}\n\n**📉 결과:**\n{analysis['result']}")
                with col2:
                    st.markdown("### 📈 곡선 변동")
                    fig = draw_market_chart(analysis)
                    st.pyplot(fig)
            except Exception as e:
                st.error("API 키를 설정하면 정상 작동합니다! 지금은 화면 구성만 확인하세요.")