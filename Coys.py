import streamlit as st
import hashlib

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2025 TEAM LINEUP",
    page_icon="⚽",
    layout="wide" # 넓은 화면 사용
)

# --- 2. 스타일 (CSS) - 전술판 및 유니폼 디자인 ---
st.markdown("""
    <style>
    /* 전체 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@400;700&display=swap');
    
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }

    /* 🏟️ 축구장 (전술판) 스타일 - 순수 CSS 구현 */
    .pitch-container {
        position: relative;
        width: 100%;
        max-width: 600px;
        aspect-ratio: 2/3; /* 세로형 축구장 비율 */
        margin: 0 auto;
        background: repeating-linear-gradient(
            0deg,
            #2e7d32,
            #2e7d32 10%,
            #388e3c 10%,
            #388e3c 20%
        );
        border: 2px solid white;
        border-radius: 5px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        overflow: hidden;
    }

    /* 경기장 라인 */
    .line { position: absolute; border: 2px solid rgba(255,255,255,0.7); }
    .center-circle { 
        top: 50%; left: 50%; width: 100px; height: 100px; 
        border-radius: 50%; transform: translate(-50%, -50%); 
    }
    .half-line { top: 50%; width: 100%; height: 2px; background: rgba(255,255,255,0.7); border:none; }
    .penalty-box-top { top: 0; left: 50%; width: 60%; height: 15%; transform: translateX(-50%); border-top: none; }
    .penalty-box-bottom { bottom: 0; left: 50%; width: 60%; height: 15%; transform: translateX(-50%); border-bottom: none; }

    /* 👕 선수 아이콘 (유니폼) */
    .player-marker {
        position: absolute;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 80px;
        text-align: center;
        transition: all 0.3s;
    }
    
    /* 유니폼 원형 */
    .jersey-circle {
        width: 40px; height: 40px;
        border-radius: 50%;
        background: #f44336; /* 기본 팀 컬러 (빨강) */
        border: 2px solid white;
        display: flex; justify-content: center; align-items: center;
        color: white; font-weight: bold; font-size: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* 내 선수 강조 스타일 */
    .my-player .jersey-circle {
        background: #FFD700; /* 골드 */
        color: #000;
        width: 50px; height: 50px; font-size: 1.5rem;
        border: 3px solid #fff;
        box-shadow: 0 0 15px #FFD700;
        animation: pulse 1.5s infinite;
    }

    /* 이름표 */
    .player-name {
        background: rgba(0,0,0,0.7);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
        margin-top: 5px;
        font-family: 'Roboto', sans-serif;
        white-space: nowrap;
    }
    .my-player .player-name {
        background: #FFD700;
        color: black;
        font-weight: bold;
        font-size: 1rem;
    }

    /* 포지션 텍스트 */
    .pos-label { font-size: 0.7rem; color: #ddd; margin-top: -2px; }

    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
    </style>
""", unsafe_allow_html=True)

# --- 3. 로직: 이름에 따른 포지션 배정 ---
def get_lineup_data(name):
    # 이름을 해시값으로 변환하여 고정된 결과 생성
    hash_val = int(hashlib.md5(name.encode()).hexdigest(), 16)
    
    # 4-3-3 포메이션 좌표 (Top%, Left%) - 위쪽이 공격
    formation = [
        {"pos": "GK",  "top": 90, "left": 50, "no": 1},
        {"pos": "LB",  "top": 75, "left": 15, "no": 3},
        {"pos": "CB",  "top": 75, "left": 38, "no": 4},
        {"pos": "CB",  "top": 75, "left": 62, "no": 5},
        {"pos": "RB",  "top": 75, "left": 85, "no": 2},
        {"pos": "CM",  "top": 55, "left": 30, "no": 8},
        {"pos": "CDM", "top": 60, "left": 50, "no": 6},
        {"pos": "CM",  "top": 55, "left": 70, "no": 10},
        {"pos": "LW",  "top": 25, "left": 20, "no": 7},
        {"pos": "ST",  "top": 20, "left": 50, "no": 9},
        {"pos": "RW",  "top": 25, "left": 80, "no": 11},
    ]
    
    # 내 포지션 결정 (11개 중 하나)
    my_idx = hash_val % 11
    
    # 가상의 팀원 이름들
    teammates = ["De Gea", "Davies", "Van Dijk", "Saliba", "Walker", "KDB", "Rodri", "Bellingham", "Vinicius", "Haaland", "Salah"]
    
    # 데이터 조립
    players = []
    for i, spot in enumerate(formation):
        is_me = (i == my_idx)
        player_name = name if is_me else teammates[i]
        
        players.append({
            "name": player_name,
            "pos": spot["pos"],
            "top": spot["top"],
            "left": spot["left"],
            "no": spot["no"],
            "is_me": is_me
        })
        
    # 팀 정보 (해시값 기반 랜덤)
    teams = ["Manchester City", "Real Madrid", "Arsenal", "Liverpool", "Bayern Munich"]
    my_team = teams[hash_val % len(teams)]
    
    return players, my_team, players[my_idx] # 전체선수, 팀명, 내정보

# --- 4. 메인 화면 UI ---

col1, col2 = st.columns([1, 2])

# 왼쪽: 입력란
with col1:
    st.markdown("### 📋 SCOUTING REPORT")
    st.info("이름을 입력하면 25/26 시즌 선발 라인업에서의 당신의 위치를 보여줍니다.")
    
    input_name = st.text_input("선수 이름 입력", placeholder="예: 손흥민")
    
    btn = st.button("라인업 확인하기", type="primary", use_container_width=True)

    if btn and input_name:
        players, team_name, my_info = get_lineup_data(input_name)
        
        st.markdown("---")
        st.success(f"✅ **{team_name}** 입단 확정!")
        
        # 내 스탯 표시 (카드 형태)
        st.markdown(f"""
        <div style="background:#333; padding:20px; border-radius:10px; border-left: 5px solid #FFD700;">
            <h2 style="margin:0; color:#FFD700;">{my_info['name']}</h2>
            <p style="color:#aaa; margin:0;">No. {my_info['no']} | {my_info['pos']}</p>
            <hr style="border-color:#555;">
            <div style="display:flex; justify-content:space-between; font-weight:bold;">
                <span>OVR (평점)</span>
                <span style="color:#4CAF50;">{(85 + len(input_name)) % 15 + 85}</span>
            </div>
            <div style="margin-top:10px; font-size:0.9rem; color:#ccc;">
                "감독이 당신을 <strong>{my_info['pos']}</strong> 포지션의 핵심으로 낙점했습니다."
            </div>
        </div>
        """, unsafe_allow_html=True)

# 오른쪽: 전술판 (항상 표시되거나 버튼 클릭시 갱신)
with col2:
    if btn and input_name:
        players, team_name, my_info = get_lineup_data(input_name)
        
        # HTML로 전술판 그리기
        players_html = ""
        for p in players:
            extra_class = "my-player" if p["is_me"] else ""
            players_html += f"""
            <div class="player-marker {extra_class}" style="top: {p['top']}%; left: {p['left']}%;">
                <div class="jersey-circle">{p['no']}</div>
                <div class="player-name">{p['name']}</div>
                <div class="pos-label">{p['pos']}</div>
            </div>
            """
            
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:10px;">
            <h2 style="color:white; letter-spacing:2px;">STARTING XI</h2>
            <div style="color:#aaa;">{team_name} vs All-Stars</div>
        </div>
        
        <div class="pitch-container">
            <div class="line center-circle"></div>
            <div class="line half-line"></div>
            <div class="line penalty-box-top"></div>
            <div class="line penalty-box-bottom"></div>
            
            {players_html}
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # 대기 화면 (빈 전술판)
        st.markdown("""
        <div class="pitch-container" style="opacity:0.5; display:flex; justify-content:center; align-items:center;">
             <h3 style="color:white;">WAITING FOR PLAYER...</h3>
        </div>
        """, unsafe_allow_html=True)
