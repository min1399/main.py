import streamlit as st
import hashlib
import time
from datetime import date

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="FC 2026 PACK OPENING",
    page_icon="⚽",
    layout="centered"
)

# --- 2. CSS 스타일링 (이미지 없이 코드로 구현) ---
st.markdown("""
    <style>
    /* 전체 배경: 어두운 우주 느낌 */
    .stApp {
        background: radial-gradient(circle at center, #000000 0%, #1a0f2e 50%, #0d0612 100%);
        color: white;
    }

    /* 🚀 핵심: 순수 CSS로 만든 터널/워프 효과 */
    @keyframes warpEffect {
        0% { transform: scale(1); opacity: 0; }
        10% { opacity: 1; }
        80% { opacity: 1; }
        100% { transform: scale(4); opacity: 0; }
    }
    
    @keyframes flash {
        0%, 100% { opacity: 0; }
        50% { opacity: 0.8; }
    }

    .tunnel-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 9999;
        pointer-events: none;
        /* 중앙에서 빛이 뿜어져 나오는듯한 그래디언트 */
        background: radial-gradient(circle, rgba(255,255,255,0) 0%, rgba(255,215,0,0.2) 40%, rgba(255,100,0,0.6) 80%, rgba(0,0,0,1) 100%);
        /* 점점 커지면서 다가오는 애니메이션 */
        animation: warpEffect 3.5s ease-in-out forwards;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* 추가적인 번쩍임 효과 */
    .tunnel-overlay::after {
        content: '';
        position: absolute;
        width: 100%; height: 100%;
        background: white;
        animation: flash 0.5s 3 ease-in-out; /* 3번 번쩍임 */
        opacity: 0;
    }


    /* 카드 디자인 */
    .fut-card {
        background: linear-gradient(180deg, #f8e6b8 0%, #eacda3 80%, #d4af37 100%);
        border: 3px solid #f1c40f;
        border-radius: 25px;
        padding: 15px;
        width: 340px;
        margin: 20px auto;
        color: #2c3e50;
        box-shadow: 0 0 60px rgba(241, 196, 15, 0.6), inset 0 0 20px rgba(255,255,255,0.5);
        text-align: center;
        position: relative;
        animation: cardPop 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        z-index: 1;
    }

    .card-left-info {
        position: absolute; top: 20px; left: 20px;
        display: flex; flex-direction: column; align-items: center; z-index: 2;
    }
    .rating { font-size: 4rem; font-weight: 900; line-height: 0.9; color: #3d3122; }
    .position { font-size: 1.6rem; font-weight: 800; margin-top: 5px; color: #3d3122; }
    .nation-flag { font-size: 2.2rem; margin: 5px 0; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3)); }
    .club-logo { width: 45px; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3)); }

    .player-face {
        width: 200px; height: 200px; object-fit: contain; margin-left: 60px;
        filter: drop-shadow(8px 8px 10px rgba(0,0,0,0.4));
    }

    .card-name {
        font-family: 'Arial Black', sans-serif; font-size: 2rem; font-weight: 900;
        text-transform: uppercase; letter-spacing: 1px; margin: 10px 0 15px 0;
        color: #3d3122; border-bottom: 3px solid #cba765; display: inline-block; padding-bottom: 5px;
    }

    /* 스탯 그리드 디자인 */
    .stats-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 5px 30px;
        padding: 10px 30px; font-weight: 800; font-size: 1.2rem; color: #3d3122; text-align: left;
    }
    .stat-row { display: flex; justify-content: space-between; align-items: center; }
    .stat-val { font-size: 1.3rem; font-weight: 900; margin-right: 8px; }
    .stat-label { font-weight: normal; font-size: 1rem; opacity: 0.8; }

    /* 워크아웃 글자 효과 (화면 중앙 정렬) */
    .walkout-container {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10000; /* 터널보다 위에 */
        text-align: center;
        width: 100%;
    }
    .walkout-step {
        font-size: 6rem; font-weight: 900; color: #f1c40f;
        text-shadow: 0 0 50px #f1c40f, 0 0 20px white;
        animation: pulse 0.8s infinite alternate;
    }
    .walkout-img {
        width: 200px;
        filter: drop-shadow(0 0 30px #f1c40f);
        animation: pulse 0.8s infinite alternate;
    }


    @keyframes cardPop { from { transform: scale(0.5); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    @keyframes pulse { from { opacity: 0.7; transform: scale(0.95); } to { opacity: 1; transform: scale(1.05); } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터 생성 로직 ---
def generate_player_data(name, dob):
    seed = f"{name}{dob}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    # 기본 데이터
    positions = ["ST", "LW", "RW", "CAM", "CM", "CDM", "CB", "LB", "RB", "GK"]
    flags = ["🇰🇷", "🇦🇷", "🇵🇹", "🇫🇷", "🇧🇷", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🇩🇪", "🇪🇸", "🇮🇹", "🇳🇱"]
    teams = [
        ("Real Madrid", "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg"),
        ("Man City", "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"),
        ("Bayern", "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg"),
        ("PSG", "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg"),
        ("Liverpool", "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg")
    ]
    
    pos = positions[h % len(positions)]
    flag = flags[(h // 7) % len(flags)]
    team_name, team_logo = teams[(h // 13) % len(teams)]
    
    ovr = 85 + (h % 15)
    base = ovr - 3
    
    stats = {}
    if pos in ["ST", "LW", "RW"]:
        stats = {"PAC": base+3, "SHO": base+4, "PAS": base-1, "DRI": base+3, "DEF": base-25, "PHY": base-5}
    elif pos in ["CAM", "CM", "CDM"]:
        stats = {"PAC": base-2, "SHO": base, "PAS": base+4, "DRI": base+2, "DEF": base, "PHY": base}
    elif pos in ["CB", "LB", "RB"]:
        stats = {"PAC": base-1, "SHO": base-20, "PAS": base-3, "DRI": base-5, "DEF": base+5, "PHY": base+4}
    else: # GK
        stats = {"DIV": base+2, "HAN": base+2, "KIC": base, "REF": base+4, "SPD": base-15, "POS": base+2}

    # 스탯 계산
    for k, v in stats.items():
        stats[k] = min(99, max(50, v + (h % 5) - 2))
        
    player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048122.png"
    if ovr >= 90:
         player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048127.png"

    return pos, flag, team_logo, ovr, stats, player_img

# --- 4. 메인 UI ---
st.markdown("<h1 style='text-align: center; color: #f1c40f; text-shadow: 0 0 20px #f1c40f;'>⚡ ULTIMATE FUT 26 PACK ⚡</h1>", unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2)
    name_input = c1.text_input("Player Name (ENG/KOR)", placeholder="e.g. SON")
    dob_input = c2.date_input("Birth Date", value=date(2000, 1, 1))
    
    if st.button("🔥 PACK OPEN (팩 개봉) 🔥", type="primary"):
        if not name_input:
            st.error("이름을 입력해주세요!")
        else:
            pos, flag, team_logo, ovr, stats, player_img = generate_player_data(name_input, dob_input)
            
            # 1. [핵심] 순수 CSS로 만든 터널 효과 시작
            st.markdown('<div class="tunnel-overlay"></div>', unsafe_allow_html=True)
            
            placeholder = st.empty()
            
            # 터널 진행 중... (긴장감 조성)
            time.sleep(2.5)
            
            # 2. 워크아웃 단계별 정보 표시 (화면 중앙)
            # 국기
            placeholder.markdown(f"<div class='walkout-container'><div class='walkout-step'>{flag}</div></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            # 포지션
            placeholder.markdown(f"<div class='walkout-container'><div class='walkout-step'>{pos}</div></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            # 소속팀
            placeholder.markdown(f"<div class='walkout-container'><img src='{team_logo}' class='walkout-img'></div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            # 3. 최종 카드 공개
            placeholder.empty()
            st.balloons()
            
            # 스탯 HTML 조립
            stats_html = ""
            if pos == "GK":
                labels = [("DIV", stats["DIV"]), ("HAN", stats["HAN"]), ("KIC", stats["KIC"]),
                          ("REF", stats["REF"]), ("SPD", stats["SPD"]), ("POS", stats["POS"])]
            else:
                labels = [("PAC", stats["PAC"]), ("SHO", stats["SHO"]), ("PAS", stats["PAS"]),
                          ("DRI", stats["DRI"]), ("DEF", stats["DEF"]), ("PHY", stats["PHY"])]
            
            for label, val in labels:
                stats_html += f"<div class='stat-row'><span class='stat-val'>{val}</span><span class='stat-label'>{label}</span></div>"

            # 카드 HTML 출력
            st.markdown(f"""
            <div class="fut-card">
                <div class="card-left-info">
                    <span class="rating">{ovr}</span>
                    <span class="position">{pos}</span>
                    <span class="nation-flag">{flag}</span>
                    <img src="{team_logo}" class="club-logo">
                </div>
                <img src="{player_img}" class="player-face">
                <div class="card-name">{name_input}</div>
                <div class="stats-grid">{stats_html}</div>
            </div>
            """, unsafe_allow_html=True)
