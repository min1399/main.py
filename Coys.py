import streamlit as st
st.title("first web app")
st.write('Welcome!')
import streamlit as st
import time

# --- 1. 페이지 설정 (가장 먼저 와야 함) ---
st.set_page_config(
    page_title="⚽ 나만의 축구 포지션 찾기",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 커스텀 CSS (화려한 디자인을 위한 스타일링) ---
st.markdown("""
    <style>
    /* 전체 배경: 축구 잔디 느낌의 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* 메인 타이틀 스타일 */
    .title-text {
        color: #ffffff;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    
    /* 결과 카드 스타일 */
    .player-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 4px solid #f1c40f; /* 골드 테두리 */
        animation: fadeIn 1s ease-in-out;
    }
    
    /* 포지션 이름 */
    .position-name {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }
    
    /* 설명 텍스트 */
    .desc-text {
        color: #555;
        font-size: 1.2rem;
        line-height: 1.6;
    }
    
    /* 이모지 강조 */
    .big-emoji {
        font-size: 5rem;
        display: block;
        margin-bottom: 10px;
    }

    /* 버튼 스타일링 */
    .stButton>button {
        width: 100%;
        background-color: #ff4b1f;
        color: white;
        font-size: 1.2rem;
        border-radius: 10px;
        padding: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff9068;
        transform: scale(1.02);
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 포지션 로직 데이터 ---
def get_position_data(number):
    if number == 1:
        return "🧤", "수호신 골키퍼 (GK)", "팀의 심장! 당신은 책임감이 강하고 든든한 최후의 보루입니다. 슈퍼세이브로 팀을 구하는 영웅이군요!"
    elif number in [2, 3, 4, 5]:
        return "🛡️", "철벽 수비수 (DF)", "통곡의 벽! 당신은 헌신적이고 끈기 있는 성격입니다. 상대 공격수에게는 악몽 같은 존재시군요."
    elif number == 6:
        return "🧠", "살림꾼 수비형 미드필더 (CDM)", "그라운드의 사령관! 경기의 흐름을 읽고 팀의 밸런스를 맞추는 지능적인 플레이어입니다."
    elif number == 7:
        return "⚡", "슈퍼스타 윙어 (Winger)", "팬들의 사랑을 독차지하는 스타! 화려한 기술과 스피드로 측면을 지배하는 에이스입니다."
    elif number == 8:
        return "⚙️", "박스 투 박스 미드필더 (CM)", "지치지 않는 체력왕! 경기장 구석구석을 누비며 공수를 연결하는 팀의 엔진입니다."
    elif number == 9:
        return "🐯", "해결사 스트라이커 (ST)", "본능적인 득점 기계! 골 냄새를 기가 막히게 맡으며, 결정적인 순간에 한 방을 터뜨립니다."
    elif number == 10:
        return "👑", "판타지스타 플레이메이커 (CAM)", "팀의 에이스! 창의적인 패스와 천재적인 센스로 경기를 지휘하는 예술가입니다."
    elif number == 11:
        return "🚀", "총알탄 스피드레이서 (LW/RW)", "누구보다 빠르다! 폭발적인 스피드로 상대 수비 라인을 붕괴시키는 돌격대장입니다."
    elif number in [12, 13, 14]:
        return "🃏", "슈퍼 서브 & 멀티플레이어", "어떤 상황에서도 흐름을 바꾸는 조커! 여러 포지션을 소화하는 다재다능한 능력자입니다."
    elif number > 99:
        return "🦄", "전설의 유니콘", "인간계의 등번호가 아닙니다! 당신은 이미 축구의 신 경지에 도달했습니다."
    else:
        return "🌟", "나만의 개성파 플레이어", f"등번호 {number}번! 남들과는 다른 길을 걷는 독창적인 스타일의 소유자시군요. 그라운드의 자유로운 영혼!"

# --- 4. 메인 UI 구성 ---

# 헤더 섹션
st.markdown('<div class="title-text">⚽ SOCCER SOUL TEST ⚽</div>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>당신의 운명의 등번호를 선택하세요!</h3>", unsafe_allow_html=True)

# 입력 섹션 (카드 모양 컨테이너 사용)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 0~99번까지 선택 가능
    choice_num = st.number_input("좋아하는 숫자를 입력하세요 (0~99)", min_value=0, max_value=999, value=7, step=1)
    
    if st.button("🔥 내 포지션 확인하기 🔥"):
        # 로딩 효과
        with st.spinner('스카우터가 당신의 재능을 분석 중입니다... 🏃‍♂️💨'):
            time.sleep(1.5) # 긴장감을 위한 딜레이
        
        # 데이터 가져오기
        emoji, pos_name, desc = get_position_data(choice_num)
        
        # 결과 화면 출력 (HTML 카드)
        st.markdown(f"""
        <div class="player-card">
            <span class="big-emoji">{emoji}</span>
            <div style="font-size: 1.5rem; color: #888;">Back Number <b>{choice_num}</b></div>
            <div class="position-name">{pos_name}</div>
            <hr>
            <div class="desc-text">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 축하 효과 (풍선 or 눈)
        if choice_num in [7, 9, 10]:
            st.balloons()
        else:
            st.snow()

# 하단 푸터
st.markdown("<br><br><div style='text-align: center; color: rgba(255,255,255,0.7);'>Made with ❤️ by Streamlit FC</div>", unsafe_allow_html=True)
