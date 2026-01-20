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

# --- 2. 커스텀 CSS (카드 디자인 + 이미지 스타일) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
        margin-bottom: 20px;
    }

    /* 카드 스타일 */
    .scout-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        max-width: 400px;
        margin: 0 auto; /* 카드 중앙 정렬 */
    }

    /* 프로필 이미지 (실루엣) */
    .profile-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid #FDBB2D;
        object-fit: cover;
        margin-bottom: 10px;
        background-color: #f0f0f0;
    }

    /* 구단 로고 */
    .team-logo-img {
        width: 60px;
        height: 60px;
        object-fit: contain;
        vertical-align: middle;
        margin-right: 10px;
    }

    .player-name { font-size: 1.8rem; font-weight: bold; color: #fff; margin-bottom: 5px; }
    .position-badge { 
        background-color: rgba(0,0,0,0.5); 
        padding: 5px 15px; 
        border-radius: 15px; 
        font-weight: bold;
        color: #FDBB2D;
        display: inline-block;
        margin-bottom: 15px;
    }

    .stat-box {
        background: rgba(0,0,0,0.25);
        border-radius: 15px;
        padding: 15px;
        margin-top: 20px;
        text-align: left;
    }
    
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
    }
    .stat-row:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
    
    .label { color: #aaa; font-size: 0.9rem; }
    .value { color: white; font-weight: bold; font-size: 1.1rem; }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #FDBB2D 0%, #22C1C3 100%);
        color: #1a1a1a;
        font-weight: bold;
        border: none;
        padding: 12px;
        font-size: 1.1rem;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터 로직 (이미지 URL 포함) ---
def determine_destiny(name, dob):
    seed_string = f"{name}{dob}"
    hash_obj = hashlib.md5(seed_string.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # 1. 포지션
    positions = [
        ("🧤", "GK", "수호신 골키퍼"),
        ("🛡️", "CB", "철벽 센터백"),
        ("⚡", "WB", "스피드 윙백"),
        ("🧠", "CDM", "사령관 수미"),
        ("⚙️", "CM", "하트비트 중미"),
        ("🎨", "CAM", "마에스트로 공미"),
        ("🚀", "LW/RW", "슈퍼 윙어"),
        ("🐯", "ST", "득점기계 톱")
    ]
    
    # 2. 팀 데이터 (이름, 로고URL - 위키미디어 등 안정적인 주소)
    teams = [
        ("맨체스터 유나이티드", "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"),
        ("맨체스터 시티", "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"),
        ("리버풀", "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg"),
        ("아스날", "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg"),
        ("토트넘 홋스퍼", "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"),
        ("첼시", "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg"),
        ("레알 마드리드", "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg"),
        ("바르셀로나", "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg"),
        ("바이에른 뮌헨", "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg"),
        ("PSG", "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg"),
        ("유벤투스", "https://upload.wikimedia.org/wikipedia/commons/b/bc/Juventus_FC_2017_icon_%28black%29.svg"),
        ("대한민국 국가대표", "https://upload.wikimedia.org/wikipedia/commons/a/a2/South_Korea_national_football_team_logo.svg")
    ]

    # 기본 프로필 실루엣 (남녀공용 느낌)
    profile_imgs = [
        "https://cdn-icons-png.flaticon.com/512/4140/4140048.png", # 남자 선수
        "https://cdn-icons-png.flaticon.com/512/4140/4140047.png", # 여자 선수 느낌
        "https://cdn-icons-png.flaticon.com/512/166/166344.png"    # 기본 실루엣
    ]

    pos_idx = hash_int % len(positions)
    team_idx = (hash_int // 10) % len(teams)
    profile_idx = (hash_int // 5) % len(profile_imgs)
    
    base_num = (hash_int % 99) + 1
    salary = (hash_int % 400) * 10 + 50 # 50억 ~ 4050억
    
    return positions[pos_idx], teams[team_idx], base_num, salary, profile_imgs[profile_idx]

# --- 4. 메인 UI ---
st.markdown('<div class="main-title">⚽ 2026 슈퍼루키 스카우팅</div>', unsafe_allow_html=True)

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("선수 이름", placeholder="이름 입력")
    with col2:
        dob = st.date_input("생년월일", min_value=date(1980, 1, 1), value=date(2002, 6, 1))
    
    submit = st.form_submit_button("✍️ 결과 확인하기")

if submit and name:
    # 데이터 생성
    (emoji, pos_code, pos_name), (team_name, team_logo), number, salary, profile_url = determine_destiny(name, dob)
    
    import time
    with st.spinner('계약서 인쇄 중... 🖨️'):
        time.sleep(1)

    st.success("스카우팅 리포트 도착!")
    
    # HTML 카드 출력 (이미지 태그 <img> 추가됨)
    st.markdown(f"""
    <div class="scout-card">
        <img src="{profile_url}" class="profile-img">
        <div class="player-name">{name}</div>
        <div class="position-badge">{emoji} {pos_name}</div>
        
        <div class="stat-box">
            <div class="stat-row">
                <span class="label">등번호 (No.)</span>
                <span class="value" style="font-size: 1.5rem; color: #FDBB2D;">{number}</span>
            </div>
            <div class="stat-row">
                <span class="label">소속팀 (Team)</span>
                <div style="display:flex; align-items:center;">
                    <img src="{team_logo}" class="team-logo-img">
                    <span class="value">{team_name}</span>
                </div>
            </div>
            <div class="stat-row">
                <span class="label">추정 이적료</span>
                <span class="value" style="color: #43e97b;">₩ {salary}억</span>
            </div>
             <div class="stat-row">
                <span class="label">포지션 코드</span>
                <span class="value">{pos_code}</span>
            </div>
        </div>
        
        <div style="margin-top:15px; font-size:0.8rem; color:#888;">
            OFFICIAL SCOUTING REPORT 2026
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.balloons()
