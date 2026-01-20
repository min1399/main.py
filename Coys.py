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

# --- 2. CSS 스타일링 ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1a0f2e 0%, #0d0612 100%);
        color: white;
    }

    /* 배경 터널 애니메이션 */
    @keyframes tunnelFade {
        0% { opacity: 1; z-index: 9999; }
        80% { opacity: 1; z-index: 9999; }
        100% { opacity: 0; z-index: -1; visibility: hidden; }
    }

    .tunnel-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: url('https://i.pinimg.com/originals/a1/1f/65/a11f654296d4107462cd636967ecba0b.gif') no-repeat center center fixed;
        background-size: cover;
        pointer-events: none;
        animation: tunnelFade 3s forwards linear;
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
        animation: cardPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
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

    .stats-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 8px 30px;
        padding: 10px 30px; font-weight: 800; font-size: 1.2rem; color: #3d3122; text-align: left;
    }
    .stat-row { display: flex; justify-content: space-between; align-items: center; }
    .stat-val { font-size: 1.3rem; font-weight: 900; margin-right: 8px; }
    .stat-label { font-weight: normal; font-size: 1rem; opacity: 0.8; }

    .walkout-step {
        font-size: 5rem; font-weight: 900; color: #f1c40f; text-align: center;
        text-shadow: 0 0 30px #f1c40f; animation: pulse 0.8s infinite alternate;
    }

    @keyframes cardPop { from { transform: scale(0.5); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    @keyframes pulse { from { opacity: 0.7; transform: scale(0.95); } to { opacity: 1; transform: scale(1.05); } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터 생성 로직 (수정됨) ---
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

    # 🔥 여기가 수정된 부분입니다 (.items() 추가) 🔥
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
    
    if st.button("🔥 PACK OPEN 🔥", type="primary"):
        if not name_input:
            st.error("이름을 입력해주세요!")
        else:
            pos, flag, team_logo, ovr, stats, player_img = generate_player_data(name_input, dob_input)
            
            # 터널 애니메이션 시작
            st.markdown('<div class="tunnel-overlay"></div>', unsafe_allow_html=True)
            
            placeholder = st.empty()
            time.sleep(2.5) # 터널 지속 시간과 맞춤
            
            placeholder.markdown(f"<div class='walkout-step'>{flag}</div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            placeholder.markdown(f"<div class='walkout-step'>{pos}</div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            placeholder.markdown(f"<div style='text-align:center;'><img src='{team_logo}' width='150'></div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            placeholder.empty()
            st.balloons()
            
            # 스탯 HTML 만들기
            stats_html = ""
            if pos == "GK":
                labels = [("DIV", stats["DIV"]), ("HAN", stats["HAN"]), ("KIC", stats["KIC"]),
                          ("REF", stats["REF"]), ("SPD", stats["SPD"]), ("POS", stats["POS"])]
            else:
                labels = [("PAC", stats["PAC"]), ("SHO", stats["SHO"]), ("PAS", stats["PAS"]),
                          ("DRI", stats["DRI"]), ("DEF", stats["DEF"]), ("PHY", stats["PHY"])]
            
            for label, val in labels:
                stats_html += f"<div class='stat-row'><span class='stat-val'>{val}</span><span class='stat-label'>{label}</span></div>"

            # 카드 출력
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
