import streamlit as st
import time
import random

# --- 1. 페이지 및 세션 상태 설정 ---
st.set_page_config(
    page_title="⚽ 나만의 축구 포지션 찾기 Pro",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화 (GIF 표시 여부 제어용)
if 'show_gif_overlay' not in st.session_state:
    st.session_state.show_gif_overlay = False
if 'current_gif_url' not in st.session_state:
    st.session_state.current_gif_url = ""


# --- 2. 커스텀 CSS (화려한 디자인 + 움짤 효과) ---
st.markdown("""
    <style>
    /* 전체 배경: 기본 축구장 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        transition: background 0.5s ease;
    }
    
    /* --- ✨ 핵심: 일시적 배경 움짤 오버레이 애니메이션 --- */
    @keyframes magicBackgroundFade {
        0% { opacity: 0; z-index: 9998; }
        10% { opacity: 1; z-index: 9998; } /* 빠르게 나타남 */
        75% { opacity: 1; z-index: 9998; } /* 잠시 유지 */
        100% { opacity: 0; z-index: -1; pointer-events: none;} /* 사라지고 클릭 통과 */
    }
    
    .gif-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        /* 배경을 어둡게 깔고 그 위에 GIF를 중앙에 배치 */
        background-color: rgba(0,0,0,0.7); 
        background-repeat: no-repeat;
        background-position: center center;
        background-size: contain; /* GIF가 잘리지 않게 */
        
        /* 애니메이션 적용: 4초 동안 실행 */
        animation: magicBackgroundFade 4s forwards ease-in-out;
    }

    /* 메인 타이틀 스타일 */
    .title-text {
        color: #ffffff;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7);
        margin-bottom: 20px;
    }
    
    /* 결과 카드 스타일 (조금 더 고급스럽게) */
    .player-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        border: 4px solid #D4AF37; /* 골드 테두리 */
        animation: slideUp 0.8s ease-out;
        position: relative;
        z-index: 1; /* GIF보다 앞에 오도록 */
    }
    
    .match-player-badge {
        background-color: #D4AF37;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 10px;
        display: inline-block;
    }

    .position-name {
        color: #2c3e50;
        font-size: 2.2rem;
        font-weight: 900;
        margin: 15px 0;
    }
    
    .desc-text {
        color: #555;
        font-size: 1.15rem;
        line-height: 1.7;
    }
    
    .big-emoji {
        font-size: 6rem;
        display: block;
        margin-bottom: 5px;
        text-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }

    /* 버튼 스타일링 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff4b1f, #ff9068);
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        border-radius: 15px;
        padding: 12px;
        border: none;
        box-shadow: 0 5px 15px rgba(255, 75, 31, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(255, 75, 31, 0.6);
    }
    
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(50px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터: 포지션 정보 + 유명 선수 + 움짤 URL ---
# (안정적인 움짤 주소를 사용해야 합니다. Giphy 등에서 가져온 예시 URL입니다.)
def get_complete_data(number):
    # 기본값
    emoji = "🌟"
    pos = "나만의 개성파 플레이어"
    desc = f"등번호 {number}번! 남들과는 다른 길을 걷는 독창적인 스타일의 소유자시군요. 그라운드의 자유로운 영혼!"
    player = "알 수 없는 숨은 고수"
    # 기본 GIF (축구장 전경 등)
    gif_url = "https://media.giphy.com/media/3o6vXUgVMtK64QAezK/giphy.gif" 

    if number == 1:
        emoji, pos = "🧤", "수호신 골키퍼 (GK)"
        desc = "팀의 최후방을 책임지는 든든한 수문장! 엄청난 반사신경으로 골문을 사수합니다."
        player = "Lev Yashin (레프 야신)" # 유일한 골키퍼 발롱도르
        gif_url = "https://media.giphy.com/media/l0Iy39YV9VNjGSaY0/giphy.gif" # 멋진 세이브 장면
    elif number == 4:
        emoji, pos = "🛡️", "철벽 센터백 (CB)"
        desc = "수비 라인의 리더! 강력한 피지컬과 카리스마로 상대 공격을 원천 봉쇄합니다."
        player = "Sergio Ramos (세르히오 라모스)"
        gif_url = "https://media.giphy.com/media/3o7TKPjiWjYtS3pA6k/giphy.gif" # 라모스 수비/헤딩
    elif number == 6:
        emoji, pos = "🧠", "마에스트로 (CDM/CM)"
        desc = "경기를 조율하는 그라운드의 사령관. 우아한 볼 터치와 넓은 시야를 가졌습니다."
        player = "Xavi Hernandez (사비 에르난데스)"
        gif_url = "https://media.giphy.com/media/26tn33aiXv5fM3Hoc/giphy.gif" # 사비 패스 마스터
    elif number == 7:
        emoji, pos = "⚡", "슈퍼스타 크랙 (Winger/FW)"
        desc = "팀의 상징이자 에이스! 폭발적인 스피드와 화려한 기술로 경기를 지배합니다."
        player = "Cristiano Ronaldo (크리스티아누 호날두) & Son Heung-min (손흥민)"
        # 손흥민 찰칵 세리머니 GIF
        gif_url = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWRiNjFkZWRhNmQxNmQxNmQxNmQxNmQxNmQxNmQxNmQxNmQxNmQxNiZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/l0HlM3NfVd0G3j6Za/giphy.gif"
    elif number == 9:
        emoji, pos = "🐯", "타고난 득점 기계 (ST)"
        desc = "골 냄새를 맡는 본능적인 스트라이커. 어떤 상황에서도 마무리를 짓는 해결사입니다."
        player = "Ronaldo Nazário (호나우두 - R9)"
        gif_url = "https://media.giphy.com/media/l2JHRhAtnJSDNJ2py/giphy.gif" # 호나우두 돌파
    elif number == 10:
        emoji, pos = "👑", "축구의 신 (Playmaker)"
        desc = "설명이 필요 없는 팀의 심장. 창의성, 기술, 득점력 모든 것을 갖춘 천재입니다."
        player = "Lionel Messi (리오넬 메시)"
        gif_url = "https://media.giphy.com/media/3o6vXI8UXFWXq7jkKI/giphy.gif" # 메시 드리블
    elif number == 11:
        emoji, pos = "🚀", "총알탄 스피드레이서 (Winger)"
        desc = "측면을 파괴하는 돌격대장! 상대 수비가 반응하기도 전에 이미 지나가 있습니다."
        player = "Gareth Bale (가레스 베일)"
        gif_url = "https://media.giphy.com/media/IsRk0bTjG003S/giphy.gif" # 베일 치고 달리기
    elif number == 14:
        emoji, pos = "💎", "토탈 풋볼의 아이콘"
        desc = "그라운드 전체를 영향력 아래 두는 혁명가. 지능적이고 우아한 플레이를 펼칩니다."
        player = "Johan Cruyff (요한 크루이프)"
        gif_url = "https://media.giphy.com/media/xT1XGVp95GDPgRYm9W/giphy.gif" # 크루이프 턴

    # 기타 번호들 처리 (간략화)
    elif number in [2, 3, 5]:
        pos = "든든한 수비벽 (DF)"
        desc = "팀을 위해 몸을 아끼지 않는 헌신적인 파이터입니다."
        player = "Maldini, Cannavaro 등 레전드 수비수들"
    elif number == 8:
        pos = "지칠 줄 모르는 엔진 (Box-to-Box)"
        player = "Steven Gerrard (스티븐 제라드)"
        gif_url = "https://media.giphy.com/media/3o7btQd56X2X6M6qmk/giphy.gif"
    elif number > 99:
        emoji, pos, desc, player = "🦄", "전설의 유니콘", "인간계를 초월했습니다. 축구의 신 그 자체!", "Unknown Legend"

    return emoji, pos, desc, player, gif_url

# --- 4. 메인 UI 구성 ---

# 만약 GIF를 보여줘야 하는 상태라면, CSS 오버레이를 주입합니다.
# 이 코드는 버튼 클릭 후 리렌더링 될 때 실행되어 배경을 잠깐 바꿉니다.
if st.session_state.show_gif_overlay:
    st.markdown(f"""
    <div class="gif-overlay" style="background-image: url('{st.session_state.current_gif_url}');"></div>
    """, unsafe_allow_html=True)
    # 한 번 보여줬으므로 다음 렌더링 때는 안 보이게 상태 변경
    st.session_state.show_gif_overlay = False


st.markdown('<div class="title-text">⚽ SOCCER SOUL TEST PRO ⚽</div>', unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #eee; margin-top: -15px;'>당신의 운명의 등번호와 매칭 선수를 확인하세요!</h4>", unsafe_allow_html=True)
st.write("") # 간격

# 입력 섹션
col_spacer1, col_input, col_spacer2 = st.columns([1, 2, 1])

with col_input:
    # 숫자 입력 받기
    choice_num = st.number_input("가장 좋아하는 숫자를 선택하세요 (0~99)", min_value=0, max_value=150, value=7, step=1, help="0부터 99까지의 숫자를 입력해보세요!")
    st.write("") # 간격

    # 버튼 클릭 시 동작
    if st.button("🚀 내 포지션 & 매칭 선수 확인! 🚀"):
        # 1. 데이터 가져오기
        emoji, pos_name, desc, match_player, gif_url = get_complete_data(choice_num)
        
        # 2. 세션 상태 업데이트 (다음 렌더링 때 GIF를 보여주기 위함)
        st.session_state.current_gif_url = gif_url
        st.session_state.show_gif_overlay = True
        
        # 3. 로딩 연출 (짧고 굵게)
        with st.spinner('⚡ 슈퍼컴퓨터가 데이터를 분석 중... 레전드 선수 소환! ⚡'):
             time.sleep(1.2) # GIF 로딩 시간을 고려해 약간의 딜레이

        # 4. 결과 카드 출력
        st.markdown(f"""
        <div class="player-card">
            <span class="big-emoji">{emoji}</span>
            <div style="font-size: 1.2rem; color: #888; margin-bottom:5px;">No. <b>{choice_num}</b></div>
            <div class="match-player-badge">🔥 매칭 선수: {match_player}</div>
            <div class="position-name">{pos_name}</div>
            <hr style="border: 1px solid #eee;">
            <div class="desc-text">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 5. 축하 이펙트
        if choice_num in [7, 9, 10, 1, 4]:
            st.balloons()
        else:
            st.snow()
            
        # 중요: GIF 오버레이를 적용하기 위해 강제 리런이 필요할 수 있음.
        # (Streamlit 버전에 따라 다르지만, 보통 상태 변경 후 자동 리런됨. 안되면 아래 주석 해제)
        # st.rerun() 

# 하단 푸터
st.write("")
st.write("")
st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8rem;'>*움짤은 네트워크 환경에 따라 로딩이 지연될 수 있습니다.<br>Made with ⚽ passion by Streamlit FC</div>", unsafe_allow_html=True)
