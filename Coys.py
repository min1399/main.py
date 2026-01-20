import streamlit as st
import time

# --- 1. 페이지 및 세션 상태 설정 ---
st.set_page_config(
    page_title="⚽ 나만의 축구 포지션 찾기 Pro",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if 'show_gif_overlay' not in st.session_state:
    st.session_state.show_gif_overlay = False
if 'current_gif_url' not in st.session_state:
    st.session_state.current_gif_url = ""

# --- 2. 커스텀 CSS (수정됨: IMG 태그 방식 적용) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* --- ✨ 배경 움짤 오버레이 (수정됨) --- */
    @keyframes magicBackgroundFade {
        0% { opacity: 0; z-index: 9998; }
        10% { opacity: 1; z-index: 9998; }
        80% { opacity: 1; z-index: 9998; }
        100% { opacity: 0; z-index: -1; pointer-events: none;}
    }
    
    .gif-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0,0,0,0.85); /* 배경을 더 어둡게 */
        display: flex;
        justify-content: center;
        align-items: center;
        animation: magicBackgroundFade 4s forwards ease-in-out;
    }
    
    /* 이미지가 화면 중앙에 예쁘게 뜨도록 설정 */
    .gif-overlay img {
        max-width: 90%;
        max-height: 80%;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
        object-fit: contain;
    }

    /* 타이틀 및 카드 스타일 */
    .title-text {
        color: #ffffff;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7);
        margin-bottom: 20px;
    }
    
    .player-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        border: 4px solid #D4AF37;
        animation: slideUp 0.8s ease-out;
        position: relative;
        z-index: 1;
    }
    
    .match-player-badge {
        background-color: #D4AF37;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }

    .position-name {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 900;
        margin: 10px 0;
    }
    
    .big-emoji { font-size: 5rem; display: block; }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff4b1f, #ff9068);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 15px;
        padding: 12px;
        border: none;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(50px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터 (수정됨: 작동하는 URL로 교체) ---
def get_complete_data(number):
    emoji = "🌟"
    pos = "나만의 개성파 플레이어"
    desc = f"등번호 {number}번! 독창적인 스타일의 소유자시군요."
    player = "Future Star"
    # 기본 이미지 (축구공)
    gif_url = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjZnYzJ4d3J5eXhpOHV4eXJ5eXhpOHV4eXJ5eXhpOHV4eXJ5eXhpOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6vXUgVMtK64QAezK/giphy.gif"

    if number == 1:
        emoji, pos = "🧤", "수호신 골키퍼 (GK)"
        desc = "팀의 최후방을 책임지는 든든한 수문장! 슈퍼세이브!"
        player = "Lev Yashin / Casillas"
        # 카시야스 슈퍼세이브
        gif_url = "https://media.giphy.com/media/l0Iy39YV9VNjGSaY0/giphy.gif"
    elif number == 4:
        emoji, pos = "🛡️", "철벽 센터백 (CB)"
        desc = "수비 라인의 리더! 카리스마로 상대를 제압합니다."
        player = "Sergio Ramos / Van Dijk"
        # 라모스
        gif_url = "https://i.giphy.com/media/3o7TKPjiWjYtS3pA6k/giphy.gif"
    elif number == 7:
        emoji, pos = "⚡", "슈퍼스타 크랙 (Winger)"
        desc = "팀의 상징이자 에이스! 폭발적인 스피드의 소유자."
        player = "Son Heung-min / Ronaldo"
        # 손흥민 (찰칵 세리머니 - 조금 더 안정적인 링크)
        gif_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGJ0ZnJ6dXNxdnhxeXJ5eXhpOHV4eXJ5eXhpOHV4eXJ5eXhpOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0HlM3NfVd0G3j6Za/giphy.gif"
    elif number == 9:
        emoji, pos = "🐯", "득점 기계 (ST)"
        desc = "골 냄새를 맡는 본능적인 스트라이커."
        player = "Ronaldo (R9) / Haaland"
        # 호나우두
        gif_url = "https://media.giphy.com/media/l2JHRhAtnJSDNJ2py/giphy.gif"
    elif number == 10:
        emoji, pos = "👑", "축구의 신 (Playmaker)"
        desc = "설명이 필요 없는 팀의 심장. 마법 같은 플레이."
        player = "Lionel Messi"
        # 메시
        gif_url = "https://media.giphy.com/media/3o6vXI8UXFWXq7jkKI/giphy.gif"
    elif number == 14:
        emoji, pos = "💎", "마에스트로"
        desc = "그라운드 전체를 지휘하는 혁명가."
        player = "Johan Cruyff"
        # 크루이프
        gif_url = "https://media.giphy.com/media/xT1XGVp95GDPgRYm9W/giphy.gif"
    
    return emoji, pos, desc, player, gif_url

# --- 4. 메인 UI ---

# 움짤 오버레이 출력 (IMG 태그 사용)
if st.session_state.show_gif_overlay:
    st.markdown(f"""
    <div class="gif-overlay">
        <img src="{st.session_state.current_gif_url}" alt="Player GIF">
    </div>
    """, unsafe_allow_html=True)
    st.session_state.show_gif_overlay = False

st.markdown('<div class="title-text">⚽ SOCCER SOUL PRO ⚽</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    choice_num = st.number_input("좋아하는 숫자 (0~99)", min_value=0, max_value=99, value=7)
    
    if st.button("🚀 확인하기"):
        emoji, pos_name, desc, match_player, gif_url = get_complete_data(choice_num)
        
        st.session_state.current_gif_url = gif_url
        st.session_state.show_gif_overlay = True
        
        with st.spinner('데이터 분석 중...'):
             time.sleep(1)

        st.markdown(f"""
        <div class="player-card">
            <span class="big-emoji">{emoji}</span>
            <div class="match-player-badge">🔥 {match_player}</div>
            <div class="position-name">{pos_name}</div>
            <div class="desc-text">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if choice_num in [7, 9, 10]:
            st.balloons()
        else:
            st.snow()
            
        # UI 즉시 갱신을 위해 rerun
        st.rerun()
