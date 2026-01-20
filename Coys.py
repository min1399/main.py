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

# --- 2. CSS 스타일링 (터널 & 워크아웃 애니메이션) ---
st.markdown("""
    <style>
    /* 전체 페이지 배경 (우주/어두운 느낌) */
    .stApp {
        background-color: #000;
        color: white;
    }

    /* 🌌 배경 3D 터널 효과 (순수 CSS) */
    @keyframes move-twink-back {
        from {background-position:0 0;}
        to {background-position:-10000px 5000px;}
    }
    
    .stars, .twinkling {
        position:fixed; top:0; left:0; width:100%; height:100%; display:block;
    }
    
    .stars {
        background:#000 url(http://www.script-tutorials.com/demos/360/images/stars.png) repeat top center;
        z-index:0;
    }
    
    .twinkling{
        background:transparent url(http://www.script-tutorials.com/demos/360/images/twinkling.png) repeat top center;
        z-index:1;
        animation:move-twink-back 200s linear infinite;
        opacity: 0.7;
    }

    /* 🏃‍♂️ 선수 걸어나오는 효과 (Walkout Animation) */
    @keyframes walkOut {
        0% { 
            transform: scale(0.1) translateY(300px); 
            opacity: 0; 
            filter: blur(10px) brightness(0);
        }
        20% {
            opacity: 1;
            filter: blur(5px) brightness(0); /* 처음엔 실루엣처럼 어둡게 */
        }
        50% {
            transform: scale(0.6) translateY(50px);
            filter: blur(0) brightness(0.5); 
        }
        100% { 
            transform: scale(1) translateY(0); 
            opacity: 1; 
            filter: brightness(1);
        }
    }
    
    /* 카드 뒤의 광채 효과 */
    @keyframes rotateLight {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .light-burst {
        position: absolute;
        top: 50%; left: 50%;
        width: 200vw; height: 200vw;
        margin-left: -100vw; margin-top: -100vw;
        background: conic-gradient(from 0deg, transparent 0deg, rgba(255, 215, 0, 0.3) 20deg, transparent 40deg);
        animation: rotateLight 10s linear infinite;
        z-index: 0;
        pointer-events: none;
    }

    /* 카드 디자인 */
    .fut-card-container {
        position: relative;
        z-index: 10;
        animation: walkOut 2.5s cubic-bezier(0.25, 1, 0.5, 1) forwards; /* 걸어나오는 애니메이션 적용 */
        margin-top: 50px;
    }

    .fut-card {
        background: linear-gradient(180deg, #f8e6b8 0%, #eacda3 80%, #d4af37 100%);
        border: 4px solid #f1c40f;
        border-radius: 25px;
        padding: 15px;
        width: 320px;
        margin: 0 auto;
        color: #2c3e50;
        box-shadow: 0 0 80px rgba(241, 196, 15, 0.8), inset 0 0 20px rgba(255,255,255,0.5);
        text-align: center;
        position: relative;
        overflow: hidden; /* 광채가 카드 밖으로 나가지 않게 하려면 카드 내부에 넣거나 조정 필요 */
    }

    .card-left-info {
        position: absolute; top: 20px; left: 15px;
        display: flex; flex-direction: column; align-items: center; z-index: 20;
    }
    .rating { font-size: 3.5rem; font-weight: 900; line-height: 0.9; color: #3d3122; }
    .position { font-size: 1.4rem; font-weight: 800; margin-top: 5px; color: #3d3122; }
    .nation-flag { font-size: 2rem; margin: 5px 0; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3)); }
    .club-logo { width: 40px; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3)); }
    
    .player-face {
        width: 220px; height: 220px; 
        object-fit: contain; 
        margin-left: 50px;
        filter: drop-shadow(10px 10px 15px rgba(0,0,0,0.5));
        position: relative;
        z-index: 10;
    }
    
    .card-name {
        font-family: 'Arial Black', sans-serif; font-size: 1.8rem; font-weight: 900;
        text-transform: uppercase; letter-spacing: 1px; margin: 10px 0 10px 0;
        color: #3d3122; border-bottom: 3px solid #cba765; display: inline-block; padding-bottom: 5px;
        position: relative; z-index: 20;
    }
    
    .stats-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 5px 20px;
        padding: 10px 20px; font-weight: 800; font-size: 1.1rem; color: #3d3122; text-align: left;
        position: relative; z-index: 20;
    }

    /* 워크아웃 텍스트 효과 */
    .walkout-text {
        font-size: 5rem; font-weight: 900; color: #fff;
        text-align: center;
        text-shadow: 0 0 30px #f1c40f;
        position: fixed; top: 40%; left: 0; right: 0;
        z-index: 999;
        animation: fadeInOut 1s ease-in-out;
    }
    
    @keyframes fadeInOut {
        0% { opacity: 0; transform: scale(0.5); }
        50% { opacity: 1; transform: scale(1.2); }
        100% { opacity: 0; transform: scale(1.5); }
    }

    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터 로직 ---
def generate_player_data(name, dob):
    seed = f"{name}{dob}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
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
    else: 
        stats = {"DIV": base+2, "HAN": base+2, "KIC": base, "REF": base+4, "SPD": base-15, "POS": base+2}

    for k, v in stats.items():
        stats[k] = min(99, max(50, v + (h % 5) - 2))
        
    # 선수 이미지: 더 실사 같은 실루엣 사용 (걷는 느낌을 주기 위해 상체 위주)
    player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048122.png" 
    if ovr >= 90:
         player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048127.png"

    return pos, flag, team_logo, ovr, stats, player_img

# --- 4. 메인 UI ---
st.markdown("<h1 style='text-align: center; color: #f1c40f; text-shadow: 0 0 20px #f1c40f;'>⚡ FC 26 PACK OPENING ⚡</h1>", unsafe_allow_html=True)

# 배경 요소 (별 + 반짝임)
st.markdown('<div class="stars"></div><div class="twinkling"></div>', unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2)
    name_input = c1.text_input("Player Name", placeholder="SON")
    dob_input = c2.date_input("Birth Date", value=date(2000, 1, 1))
    
    if st.button("🔥 PACK OPEN (팩 개봉) 🔥", type="primary"):
        if not name_input:
            st.error("이름을 입력해주세요!")
        else:
            pos, flag, team_logo, ovr, stats, player_img = generate_player_data(name_input, dob_input)
            
            placeholder = st.empty()
            
            # --- 1. 워크아웃 연출 (텍스트) ---
            # 국기
            placeholder.markdown(f"<div class='walkout-text'>{flag}</div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            # 포지션
            placeholder.markdown(f"<div class='walkout-text'>{pos}</div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            # 구단 로고
            placeholder.markdown(f"<div class='walkout-text'><img src='{team_logo}' width='150'></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            # --- 2. 선수 걸어나오는 연출 (카드 등장) ---
            placeholder.empty()
            st.balloons()
            
            # 스탯 HTML
            stats_html = ""
            if pos == "GK":
                labels = [("DIV", stats["DIV"]), ("HAN", stats["HAN"]), ("KIC", stats["KIC"]), ("REF", stats["REF"]), ("SPD", stats["SPD"]), ("POS", stats["POS"])]
            else:
                labels = [("PAC", stats["PAC"]), ("SHO", stats["SHO"]), ("PAS", stats["PAS"]), ("DRI", stats["DRI"]), ("DEF", stats["DEF"]), ("PHY", stats["PHY"])]
            
            for label, val in labels:
                stats_html += f"<div style='display:flex; justify-content:space-between;'><span style='font-weight:900; font-size:1.1rem;'>{val}</span><span style='font-size:0.9rem; opacity:0.8;'>{label}</span></div>"

            # 3. 최종 카드 렌더링 (걸어나오는 애니메이션 포함)
            st.markdown(f"""
            <div class="light-burst"></div> <div class="fut-card-container">
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
            </div>
            """, unsafe_allow_html=True)
