import streamlit as st
import hashlib

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="FM 2025 SCOUTING",
    page_icon="⚽",
    layout="wide"
)

# --- 2. 로직: 이름으로 포지션 배정 ---
def get_fm_lineup(name):
    # 이름을 숫자로 변환
    h = int(hashlib.md5(name.encode()).hexdigest(), 16)
    
    # 4-2-3-1 포메이션 좌표 (FM 스타일)
    # top: 위에서부터의 거리(%), left: 왼쪽부터의 거리(%)
    formation = [
        {"pos": "GK",  "top": 88, "left": 50, "no": 1},
        {"pos": "DR",  "top": 70, "left": 85, "no": 2},
        {"pos": "DCR", "top": 72, "left": 60, "no": 5},
        {"pos": "DCL", "top": 72, "left": 40, "no": 4},
        {"pos": "DL",  "top": 70, "left": 15, "no": 3},
        {"pos": "MCR", "top": 50, "left": 60, "no": 8},
        {"pos": "MCL", "top": 50, "left": 40, "no": 6},
        {"pos": "AMR", "top": 30, "left": 85, "no": 7},
        {"pos": "AMC", "top": 35, "left": 50, "no": 10},
        {"pos": "AML", "top": 30, "left": 15, "no": 11},
        {"pos": "ST",  "top": 12, "left": 50, "no": 9},
    ]
    
    # 내 포지션 랜덤 결정
    my_idx = h % 11
    
    # 가상의 팀원들 (프리미어리그 스타)
    teammates = ["Alisson", "TAA", "Saliba", "Van Dijk", "Gvardiol", "Rodri", "Rice", "Saka", "Odegaard", "Son", "Haaland"]
    
    # 팀 리스트 (랜덤)
    teams = ["Arsenal", "Man City", "Liverpool", "Real Madrid", "Inter"]
    my_team = teams[h % len(teams)]

    html_players = ""
    my_info = {}

    for i, spot in enumerate(formation):
        is_me = (i == my_idx)
        p_name = name if is_me else teammates[i]
        
        if is_me:
            my_info = {"name": p_name, "pos": spot["pos"], "no": spot["no"], "team": my_team}
            # 내 유니폼은 노란색(강조)
            color_class = "my-kit"
            z_index = "10"
        else:
            # 동료 유니폼은 빨간색
            color_class = "team-kit"
            z_index = "1"

        # HTML 조립
        html_players += f"""
        <div class="player-box" style="top: {spot['top']}%; left: {spot['left']}%; z-index:{z_index};">
            <div class="kit-circle {color_class}">
                <span>{spot['no']}</span>
            </div>
            <div class="name-tag">{p_name}</div>
            <div class="role-tag">{spot['pos']}</div>
        </div>
        """
        
    return html_players, my_info

# --- 3. 메인 UI 및 디자인 ---

# CSS 스타일 정의 (FM 전술판 느낌)
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp { background-color: #1e1e1e; color: white; }

    /* 🏟️ 전술판 (Pitch) 디자인 */
    .pitch-board {
        position: relative;
        width: 100%;
        max-width: 550px;
        aspect-ratio: 2/3; /* 2:3 비율 */
        margin: 0 auto;
        background: #2b5636; /* 짙은 잔디색 */
        border: 2px solid rgba(255,255,255,0.8);
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        overflow: hidden;
    }

    /* 잔디 무늬 */
    .pitch-board::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 10%,
            rgba(0,0,0,0.1) 10%,
            rgba(0,0,0,0.1) 20%
        );
    }
    
    /* 경기장 라인 */
    .pitch-line { position: absolute; border: 2px solid rgba(255,255,255,0.6); pointer-events:none; }
    .center-circle { top: 50%; left: 50%; width: 100px; height: 100px; border-radius: 50%; transform: translate(-50%, -50%); }
    .mid-line { top: 50%; left: 0; width: 100%; height: 0; border-top: 2px solid rgba(255,255,255,0.6); }
    .box-top { top: 0; left: 50%; width: 60%; height: 15%; transform: translateX(-50%); border-top: none; }
    .box-bottom { bottom: 0; left: 50%; width: 60%; height: 15%; transform: translateX(-50%); border-bottom: none; }

    /* 👕 선수 아이콘 박스 */
    .player-box {
        position: absolute;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 80px;
        transition: all 0.3s ease;
    }
    
    .player-box:hover { transform: translate(-50%, -50%) scale(1.1); cursor: pointer; }

    /* 유니폼 원형 */
    .kit-circle {
        width: 38px; height: 38px;
        border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        font-weight: bold;
        border: 2px solid white;
        box-shadow: 0 3px 6px rgba(0,0,0,0.4);
        margin-bottom: 4px;
        font-family: sans-serif;
    }
    
    .team-kit { background: #d32f2f; color: white; } /* 팀원 (빨강) */
    .my-kit { 
        background: #fbc02d; color: black; /* 나 (노랑) */
        width: 45px; height: 45px; font-size: 1.2rem;
        border: 3px solid #fff;
        animation: glow 1.5s infinite alternate;
    }

    /* 이름표 */
    .name-tag {
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        white-space: nowrap;
        text-shadow: 0 1px 2px black;
    }
    
    /* 포지션 태그 */
    .role-tag {
        font-size: 10px;
        color: #ddd;
        background: rgba(0,0,0,0.5);
        padding: 1px 4px;
        border-radius: 4px;
        margin-top: 2px;
    }

    @keyframes glow { from { box-shadow: 0 0 5px #fbc02d; } to { box-shadow: 0 0 20px #fbc02d; } }

</style>
""", unsafe_allow_html=True)


# --- 4. 화면 구성 ---
st.title("⚽ FM 2025: PREMIER LEAGUE DEBUT")
st.write("이름을 입력하면 25/26 시즌 개막전 선발 라인업을 보여줍니다.")

col_input, col_pitch = st.columns([1, 1.5])

with col_input:
    with st.container(border=True):
        input_name = st.text_input("선수 이름 (Name)", placeholder="손흥민")
        btn = st.button("라인업 확인 (Submit)", type="primary", use_container_width=True)
        
        if btn and input_name:
            players_html, my_info = get_fm_lineup(input_name)
            
            # 결과 카드
            st.markdown("### 📋 SCOUT REPORT")
            st.markdown(f"""
            <div style="background:#333; padding:15px; border-radius:10px; border-left: 5px solid #fbc02d;">
                <h2 style="margin:0; color:#fbc02d;">{my_info['name']}</h2>
                <p style="margin:5px 0; color:#ccc;">{my_info['team']}</p>
                <hr style="border-color:#555;">
                <p style="font-size:1.2rem; font-weight:bold;">
                    Position: <span style="color:#4caf50;">{my_info['pos']}</span>
                </p>
                <p style="font-size:1.2rem; font-weight:bold;">
                    Back Number: <span style="color:white;">{my_info['no']}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            players_html = "" # 초기화

with col_pitch:
    # 버튼을 눌렀을 때만 전술판 표시
    if btn and input_name:
        st.markdown(f"""
        <div style="text-align:center; color:#ddd; margin-bottom:10px; letter-spacing:1px; font-weight:bold;">
            STARTING XI
        </div>
        <div class="pitch-board">
            <div class="pitch-line center-circle"></div>
            <div class="pitch-line mid-line"></div>
            <div class="pitch-line box-top"></div>
            <div class="pitch-line box-bottom"></div>
            
            {players_html}
        </div>
        """, unsafe_allow_html=True) # ★ 여기가 가장 중요합니다 (HTML 허용)
    else:
        # 대기 화면
        st.markdown("""
        <div class="pitch-board" style="display:flex; justify-content:center; align-items:center; opacity:0.3;">
            <h3 style="color:white;">WAITING...</h3>
        </div>
        """, unsafe_allow_html=True)
