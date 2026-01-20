import streamlit as st
import hashlib
import random
from datetime import date

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="⚽ 2026 슈퍼루키 데뷔 시뮬레이터",
    page_icon="🏆",
    layout="centered"
)

# --- 2. 커스텀 CSS (FIFA 카드/계약서 스타일) ---
st.markdown("""
    <style>
    /* 배경: 챔피언스리그 느낌의 짙은 네이비 + 별빛 */
    .stApp {
        background: radial-gradient(circle at center, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    /* 타이틀 스타일 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
        margin-bottom: 30px;
    }

    /* 결과 카드 (선수 카드 느낌) */
    .scout-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.2);
        animation: flipIn 1s ease-out;
    }

    .team-logo { font-size: 5rem; margin-bottom: 10px; }
    .player-name { font-size: 2rem; font-weight: bold; color: #ffeb3b; }
    .info-label { color: #aaa; font-size: 0.9rem; margin-top: 15px; }
    .info-value { font-size: 1.5rem; font-weight: bold; color: white; }
    
    .stat-box {
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        padding: 10px;
        margin-top: 20px;
    }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #FDBB2D 0%, #22C1C3 100%);
        color: #1a1a1a;
        font-weight: bold;
        border: none;
        padding: 15px;
        font-size: 1.2rem;
        border-radius: 12px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }

    @keyframes flipIn {
        from { transform: perspective(400px) rotateX(90deg); opacity: 0; }
        to { transform: perspective(400px) rotateX(0deg); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 운명 결정 로직 (이름+생일로 고정된 결과 생성) ---
def determine_destiny(name, dob):
    # 입력값을 합쳐서 고유한 시드값 생성
    seed_string = f"{name}{dob}"
    # MD5 해시를 사용하여 항상 같은 입력엔 같은 숫자가 나오도록 함
    hash_obj = hashlib.md5(seed_string.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # 1. 포지션 데이터
    positions = [
        ("🧤", "GK", "수호신 골키퍼", "팀의 최후방을 책임지는 철벽"),
        ("🛡️", "CB", "센터백", "피지컬로 상대를 압도하는 통곡의 벽"),
        ("🏃", "WB", "윙백", "폭발적인 활동량의 측면 지배자"),
        ("🧠", "CDM", "수비형 미드필더", "경기의 흐름을 읽는 사령관"),
        ("⚙️", "CM", "중앙 미드필더", "공수를 연결하는 팀의 심장"),
        ("🎨", "CAM", "공격형 미드필더", "창의적인 패스 마스터"),
        ("⚡", "LW/RW", "윙 포워드", "상대 수비를 찢는 스피드 레이서"),
        ("🐯", "ST", "스트라이커", "골 냄새를 맡는 해결사")
    ]
    
    # 2. 팀 데이터 (재미를 위해 다양하게)
    teams = [
        ("🇪🇸 레알 마드리드", "Royal White"),
        ("🇪🇸 바르셀로나", "Blaugrana"),
        ("🇬🇧 맨체스터 시티", "Sky Blue"),
        ("🇬🇧 리버풀", "The Reds"),
        ("🇬🇧 토트넘 홋스퍼", "Spurs"),
        ("🇬🇧 맨체스터 유나이티드", "Red Devils"),
        ("🇬🇧 아스날", "Gunners"),
        ("🇬🇧 첼시", "The Blues"),
        ("🇩🇪 바이에른 뮌헨", "Die Roten"),
        ("🇩🇪 도르트문트", "Yellow Black"),
        ("🇫🇷 PSG", "Les Parisiens"),
        ("🇮🇹 유벤투스", "Bianconeri"),
        ("🇮🇹 인테르", "Nerazzurri"),
        ("🇮🇹 나폴리", "Gli Azzurri"),
        ("🇰🇷 K리그 올스타", "K-League King")
    ]

    # 해시값을 이용해 선택
    pos_idx = hash_int % len(positions)
    team_idx = (hash_int // 10) % len(teams)
    
    # 등번호: 1~99번 중 하나, 단 포지션에 따라 약간의 보정(완전 랜덤보단 그럴싸하게)
    base_num = (hash_int % 99) + 1
    # 골키퍼는 1번 확률 높임
    if positions[pos_idx][1] == "GK" and base_num % 2 == 0: 
        back_number = 1
    else:
        back_number = base_num

    # 연봉 (재미 요소): 10억 ~ 3000억 사이
    salary = (hash_int % 300) * 10 + 10 
    
    return positions[pos_idx], teams[team_idx], back_number, salary

# --- 4. 메인 UI ---

st.markdown('<div class="main-title">⚽ PRO DEBUT SCOUTING</div>', unsafe_allow_html=True)
st.write("축구 선수로 데뷔한다면? 당신의 이름과 생년월일로 운명의 팀을 확인하세요!")

# 입력 폼
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("선수 이름 (Name)", placeholder="예: 손흥민")
    with col2:
        dob = st.date_input("생년월일 (Birth Date)", min_value=date(1950, 1, 1), max_value=date(2020, 12, 31), value=date(2000, 1, 1))
    
    submit = st.form_submit_button("✍️ 계약서 서명하고 결과 보기")

# 결과 출력
if submit:
    if not name:
        st.warning("이름을 입력해주세요!")
    else:
        # 로직 실행
        (emoji, pos_code, pos_name, pos_desc), (team_name, team_nick), number, salary = determine_destiny(name, dob)
        
        # 로딩 효과
        with st.spinner('구단 스카우터들과 협상 중입니다... 📞'):
            import time
            time.sleep(1.5)
        
        st.success(f"축하합니다! {team_name} 구단과 계약을 체결했습니다! 🎉")
        st.balloons()
        
        # 결과 카드 렌더링
        st.markdown(f"""
        <div class="scout-card">
            <div style="color: #bbb; font-size: 0.9rem; margin-bottom: 5px;">OFFICIAL ANNOUNCEMENT</div>
            <div class="player-name">{name}</div>
            <div style="color: white; font-size: 1.2rem;">No. {number}</div>
            
            <hr style="border: 1px solid rgba(255,255,255,0.2); margin: 20px 0;">
            
            <div style="font-size: 4rem; margin-bottom: 10px;">{emoji}</div>
            <div class="info-value">{pos_name} ({pos_code})</div>
            <div style="color: #ccc; font-size: 1rem; margin-bottom: 20px;">"{pos_desc}"</div>
            
            <div class="stat-box">
                <div class="info-label">소속 팀 (Team)</div>
                <div class="info-value" style="color: #4facfe;">{team_name}</div>
                <div class="info-label">주급 / 연봉 (Market Value)</div>
                <div class="info-value" style="color: #43e97b;">약 {salary}억 원</div>
            </div>
            
            <div style="margin-top: 25px; font-size: 0.8rem; color: #888;">
                * 위 결과는 당신의 이름과 생년월일의 기운을 분석한 고정 결과입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
