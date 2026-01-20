import streamlit as st
import hashlib
import time
import random
from datetime import date

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="FC 2026 PACK OPENING",
    page_icon="⚽",
    layout="centered"
)

# --- 2. FIFA 스타일 CSS (화려함 극대화) ---
st.markdown("""
    <style>
    /* 배경: 게임 메뉴 같은 어두운 배경 */
    .stApp {
        background: radial-gradient(circle, #2b0c38 0%, #1a0525 100%);
        color: white;
    }
    
    /* 폰트 스타일 */
    h1, h2, h3 { font-family: 'Arial Black', sans-serif; text-transform: uppercase; }
    
    /* 카드 디자인 (Ultimate Team 스타일) */
    .fut-card {
        background: linear-gradient(180deg, #e6b980 0%, #eacda3 100%);
        border: 2px solid #f1c40f;
        border-radius: 20px;
        padding: 10px;
        width: 320px;
        margin: 0 auto;
        color: #2c3e50;
        box-shadow: 0 0 50px rgba(241, 196, 15, 0.4);
        position: relative;
        text-align: center;
        animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    /* 카드 내부 상단 정보 (OVR, 포지션, 국적, 팀) */
    .card-top {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        margin-bottom: -40px;
        padding-left: 10px;
        padding-top: 10px;
        position: relative;
        z-index: 10;
    }
    
    .rating { font-size: 3.5rem; font-weight: 900; line-height: 1; color: #333; }
    .position { font-size: 1.5rem; font-weight: bold; margin-bottom: 5px; color: #333; }
    .nation-flag { font-size: 2rem; display: block; margin-bottom: 5px; }
    .club-logo { width: 40px; display: block; }

    /* 선수 이미지 */
    .player-face {
        width: 180px;
        height: 180px;
        object-fit: contain;
        margin-top: 10px;
        filter: drop-shadow(5px 5px 5px rgba(0,0,0,0.3));
    }

    /* 이름 */
    .card-name {
        font-size: 1.8rem;
        font-weight: 900;
        letter-spacing: 1px;
        margin: 5px 0 10px 0;
        border-bottom: 2px solid #cca164;
        color: #333;
    }

    /* 스탯 그리드 (PAC, SHO, PAS...) */
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5px 20px;
        padding: 0 20px 20px 20px;
        font-weight: bold;
        font-size: 1.1rem;
        color: #333;
    }
    .stat-row { display: flex; justify-content: space-between; }
    .stat-val { font-weight: 900; }
    
    /* 애니메이션 키프레임 */
    @keyframes popIn {
        0% { transform: scale(0.1); opacity: 0; }
        80% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); }
    }
    
    /* 워크아웃 효과 텍스트 */
    .walkout-text {
        font-size: 4rem;
        font-weight: 900;
        color: #f1c40f;
        text-align: center;
        text-shadow: 0 0 20px #f1c40f;
        animation: flash 1s infinite alternate;
    }
    @keyframes flash { from { opacity: 0.5; } to { opacity: 1; } }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff00cc, #333399);
        color: white;
        font-weight: bold;
        font-size: 1.5rem;
        padding: 15px;
        border: none;
        border-radius: 50px;
        box-shadow: 0 0 20px rgba(255, 0, 204, 0.5);
    }
    .stButton>button:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터 로직 (OVR 및 세부 스탯 생성) ---
def generate_player_stats(name, dob):
    seed_string = f"{name}{dob}"
    hash_obj = hashlib.md5(seed_string.encode())
    h = int(hash_obj.hexdigest(), 16)
    
    # 포지션
    positions = [("ST", "스트라이커"), ("LW", "윙어"), ("RW", "윙어"), ("CAM", "공미"), ("CM", "중미"), ("CDM", "수미"), ("CB", "센터백"), ("LB", "풀백"), ("RB", "풀백"), ("GK", "골키퍼")]
    pos_code, _ = positions[h % len(positions)]
    
    # 구단
    teams = [
        ("Real Madrid", "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg"),
        ("Man City", "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"),
        ("Bayern", "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg"),
        ("PSG", "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg"),
        ("Liverpool", "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg")
    ]
    team_name, team_logo = teams[(h // 10) % len(teams)]
    
    # 국적 (임의)
    flags = ["🇰🇷", "🇦🇷", "🇵🇹", "🇫🇷", "🇧🇷", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🇩🇪", "🇪🇸"]
    flag = flags[(h // 5) % len(flags)]
    
    # OVR (오버롤) - 최소 84 ~ 최대 99 (월드클래스 보장)
    ovr = 84 + (h % 16)
    
    # 세부 스탯 생성 (포지션에 따라 가중치 부여)
    stats = {}
    base = ovr - 5 # 기본 베이스
    
    if pos_code in ["ST", "LW", "RW"]:
        stats = {"PAC": base+4, "SHO": base+5, "PAS": base-2, "DRI": base+3, "DEF": base-20, "PHY": base-5}
    elif pos_code in ["CAM", "CM"]:
        stats = {"PAC": base, "SHO": base, "PAS": base+5, "DRI": base+4, "DEF": base-5, "PHY": base-5}
    elif pos_code in ["CDM", "CB", "LB", "RB"]:
        stats = {"PAC": base-2, "SHO": base-15, "PAS": base, "DRI": base-5, "DEF": base+5, "PHY": base+5}
    else: # GK
        stats = {"DIV": base+2, "HAN": base+3, "KIC": base, "REF": base+4, "SPD": base-10, "POS": base+2}
        
    # 약간의 랜덤성 추가
    for k in stats:
        stats[k] = min(99, max(40, stats[k] + (h % 7) - 3))

    # 선수 실루엣 이미지 (워크아웃 느낌)
    silhouette = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5Z3Z5/3o7TKy7hC4tH6qQe6Q/giphy.gif" # 임시 GIF
    if ovr >= 90:
        player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048122.png" # 레전드 느낌
    else:
        player_img = "https://cdn-icons-png.flaticon.com/512/166/166344.png" # 일반 느낌
        
    return pos_code, team_logo, flag, ovr, stats, player_img

# --- 4. 메인 UI ---

st.markdown("<h1 style='text-align: center; color: #f1c40f;'>FC 2026 ULTIMATE PACK</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>이름과 생일을 입력하고 팩을 개봉하세요!</p>", unsafe_allow_html=True)

# 입력 폼
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Player Name", placeholder="SON HEUNG MIN")
    with c2:
        dob = st.date_input("Date of Birth", value=date(2000,1,1), min_value=date(1950,1,1))

    # 버튼: 상태 관리를 위해 콜백 대신 if문 처리
    open_pack = st.button("⚡ OPEN PACK (팩 개봉) ⚡")

# --- 5. 연출 및 결과 (Animation Logic) ---
if open_pack and name:
    # 1. 데이터 생성
    pos, team_logo, flag, ovr, stats, player_img = generate_player_stats(name, dob)
    
    # 2. 워크아웃 애니메이션 (st.empty 사용)
    placeholder = st.empty()
    
    # 단계 1: 터널/스포트라이트 GIF
    with placeholder.container():
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        # 터널 느낌의 GIF (외부 소스)
        st.image("https://media.giphy.com/media/l41YtZOb9EUABfS9O/giphy.gif", caption="WALKOUT...", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(2.5) # 긴장감 조성
    
    # 단계 2: 국기 등장
    with placeholder.container():
        st.markdown(f"<div class='walkout-text'>{flag}</div>", unsafe_allow_html=True)
    time.sleep(1.0)
    
    # 단계 3: 포지션 등장
    with placeholder.container():
        st.markdown(f"<div class='walkout-text'>{pos}</div>", unsafe_allow_html=True)
    time.sleep(1.0)
    
    # 단계 4: 소속팀 로고 등장
    with placeholder.container():
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st.image(team_logo, width=150)
        st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(1.2)
    
    # 단계 5: 쾅! 카드 공개 (Final Reveal)
    placeholder.empty() # 기존 내용 지우기
    st.balloons() # 축하 효과
    
    # 카드 HTML 렌더링
    stats_html = ""
    # 포지션이 GK가 아니면 일반 스탯
    if pos != "GK":
        s_keys = [("PAC", stats["PAC"]), ("SHO", stats["SHO"]), ("PAS", stats["PAS"]), 
                  ("DRI", stats["DRI"]), ("DEF", stats["DEF"]), ("PHY", stats["PHY"])]
    else:
        s_keys = [("DIV", stats["DIV"]), ("HAN", stats["HAN"]), ("KIC", stats["KIC"]),
                  ("REF", stats["REF"]), ("SPD", stats["SPD"]), ("POS", stats["POS"])]

    for k, v in s_keys:
        stats_html += f"<div class='stat-row'><span class='stat-val'>{v}</span> <span style='font-weight:normal;'>{k}</span></div>"

    st.markdown(f"""
    <div class="fut-card">
        <div class="card-top">
            <div style="display:flex; flex-direction:column; align-items:center; width: 60px;">
                <span class="rating">{ovr}</span>
                <span class="position">{pos}</span>
                <span class="nation-flag">{flag}</span>
                <img src="{team_logo}" class="club-logo">
            </div>
            <img src="{player_img}" class="player-face" style="margin-left: 10px;">
        </div>
        
        <div class="card-name">{name.upper()}</div>
        
        <div class="stats-grid">
            {stats_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 하단 코멘트
    time.sleep(0.5)
    if ovr >= 90:
        st.success("✨ WALKOUT! WORLD CLASS PLAYER! ✨")
    elif ovr >= 86:
        st.info("🔥 BOARDS! TOP TALENT! 🔥")
    else:
        st.warning("👍 GOOD PLAYER!")

elif open_pack and not name:
    st.error("Please enter a name first!")
