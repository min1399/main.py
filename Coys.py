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

# --- 2. CSS 스타일링 (입력 막힘 해결 + 걸어나오는 효과) ---
st.markdown("""
    <style>
    /* 전체 배경: 칠흑 같은 어둠 + 별 */
    .stApp {
        background-color: #050505;
        color: white;
    }

    /* 🛑 핵심 수정: 배경 요소가 클릭을 방해하지 않도록 설정 (pointer-events: none) */
    .background-effect {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; /* 클릭 통과! 중요! */
        z-index: 0;
    }

    /* 배경 별빛 애니메이션 */
    @keyframes move-stars {
        from {background-position:0 0;}
        to {background-position:-10000px 5000px;}
    }
    .stars {
        background: #000 url(http://www.script-tutorials.com/demos/360/images/stars.png) repeat top center;
        opacity: 0.8;
    }
    .twinkling {
        background: transparent url(http://www.script-tutorials.com/demos/360/images/twinkling.png) repeat top center;
        animation: move-stars 200s linear infinite;
        opacity: 0.5;
    }

    /* 🚶‍♂️ 사람이 걸어나오는 효과 (줌인 + 페이드인) */
    @keyframes walkOutAnimation {
        0% {
            transform: scale(0.2) translateY(500px); /* 작고 아래쪽에 있음 */
            opacity: 0;
            filter: brightness(0); /* 어두운 실루엣 */
        }
        30% {
            opacity: 1;
            filter: brightness(0.2); /* 서서히 보임 */
        }
        100% {
            transform: scale(1) translateY(0); /* 원래 크기 */
            opacity: 1;
            filter: brightness(1); /* 완전히 밝아짐 */
        }
    }

    /* 카드 컨테이너 */
    .walkout-container {
        display: flex;
        justify-content: center;
        margin-top: 50px;
        perspective: 1000px; /* 3D 효과 */
    }

    .fut-card {
        width: 320px;
        background: linear-gradient(180deg, #f8e6b8 0%, #eacda3 80%, #d4af37 100%);
        border: 4px solid #f1c40f;
        border-radius: 25px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 50px rgba(241, 196, 15, 0.5);
        position: relative;
        
        /* 여기가 핵심: 애니메이션 적용 */
        animation: walkOutAnimation 3s cubic-bezier(0.19, 1, 0.22, 1) forwards;
        z-index: 10;
    }

    /* 카드 내부 요소들 */
    .card-top {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .info-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 70px;
    }
    .rating { font-size: 3.5rem; font-weight: 900; line-height: 1; color: #3d3122; }
    .position { font-size: 1.5rem; font-weight: 800; color: #3d3122; margin-bottom: 5px; }
    .nation-flag { font-size: 2rem; margin-bottom: 5px; }
    
    .player-img {
        width: 180px;
        height: 180px;
        object-fit: contain;
        margin-left: 20px;
        filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.4));
    }

    .card-name {
        font-family: 'Arial Black', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        text-transform: uppercase;
        border-bottom: 3px solid #cba765;
        margin: 10px 0;
        color: #3d3122;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5px 20px;
        font-weight: 900;
        color: #3d3122;
        font-size: 1.1rem;
    }
    
    /* 워크아웃 텍스트 (국기, 포지션 등) */
    .step-text {
        font-size: 5rem;
        font-weight: 900;
        color: #f1c40f;
        text-align: center;
        position: fixed;
        top: 40%; left: 0; right: 0;
        text-shadow: 0 0 30px #f1c40f;
        z-index: 999;
        animation: pop 0.5s ease-out;
    }
    @keyframes pop { from {transform: scale(0);} to {transform: scale(1);} }

    /* 입력 폼 스타일 (확실히 클릭되게) */
    .stTextInput, .stDateInput, .stButton {
        position: relative;
        z-index: 50 !important; /* 배경보다 무조건 위에 */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 배경 깔기 (클릭 방지 적용됨) ---
st.markdown('<div class="background-effect stars"></div><div class="background-effect twinkling"></div>', unsafe_allow_html=True)

# --- 4. 데이터 로직 ---
def generate_data(name, dob):
    seed = f"{name}{dob}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    positions = ["ST", "LW", "RW", "CAM", "CM", "CDM", "CB", "LB", "RB", "GK"]
    flags = ["🇰🇷", "🇦🇷", "🇵🇹", "🇫🇷", "🇧🇷", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🇩🇪", "🇪🇸", "🇮🇹", "🇳🇱"]
    teams = [
        ("https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg"),
        ("https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg"),
        ("https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg"),
        ("https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg"),
        ("https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg")
    ]
    
    pos = positions[h % len(positions)]
    flag = flags[(h // 7) % len(flags)]
    team_logo = teams[(h // 13) % len(teams)]
    ovr = 86 + (h % 14) # 86 ~ 99
    
    # 선수 실루엣 이미지 (기본: 남자 선수 아이콘)
    player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048122.png"
    
    # 스탯 생성
    base = ovr - 3
    stats = {}
    if pos == "GK":
         stats = {"DIV": base, "HAN": base+2, "KIC": base-5, "REF": base+3, "SPD": base-10, "POS": base}
    else:
         stats = {"PAC": base+2, "SHO": base+1, "PAS": base, "DRI": base+2, "DEF": base-10, "PHY": base-5}
         
    for k, v in stats.items():
        stats[k] = min(99, max(60, v))
        
    return pos, flag, team_logo, ovr, stats, player_img

# --- 5. 메인 UI ---
st.markdown("<h1 style='text-align: center; color: #f1c40f;'>⚡ FC 26 ULTIMATE PACK ⚡</h1>", unsafe_allow_html=True)

# 입력 폼 (컨테이너 사용)
with st.container():
    c1, c2 = st.columns(2)
    name = c1.text_input("Player Name (이름)", placeholder="SON")
    dob = c2.date_input("Birth Date (생일)", value=date(2000, 1, 1))
    
    btn = st.button("🔥 PACK OPEN (팩 개봉) 🔥", type="primary", use_container_width=True)

# 버튼 클릭 시 실행
if btn:
    if not name:
        st.error("이름을 입력해주세요!")
    else:
        # 데이터 생성
        pos, flag, team_logo, ovr, stats, player_img = generate_data(name, dob)
        
        # --- 워크아웃 연출 (단계별 텍스트) ---
        placeholder = st.empty()
        
        # 1. 국기 쿵!
        placeholder.markdown(f"<div class='step-text'>{flag}</div>", unsafe_allow_html=True)
        time.sleep(1.0)
        
        # 2. 포지션 쿵!
        placeholder.markdown(f"<div class='step-text'>{pos}</div>", unsafe_allow_html=True)
        time.sleep(1.0)
        
        # 3. 로고 쿵!
        placeholder.markdown(f"<div class='step-text'><img src='{team_logo}' width='150'></div>", unsafe_allow_html=True)
        time.sleep(1.0)
        
        # 4. 화면 비우고 카드 등장 (걸어나오는 애니메이션)
        placeholder.empty()
        st.balloons()
        
        # 스탯 HTML 만들기
        stats_html = ""
        for k, v in stats.items():
            stats_html += f"<div style='display:flex; justify-content:space-between;'><span>{v}</span><span style='opacity:0.7;'>{k}</span></div>"

        # 최종 카드 출력 (애니메이션 클래스 포함)
        st.markdown(f"""
        <div class="walkout-container">
            <div class="fut-card">
                <div class="card-top">
                    <div class="info-col">
                        <span class="rating">{ovr}</span>
                        <span class="position">{pos}</span>
                        <span class="nation-flag">{flag}</span>
                        <img src="{team_logo}" width="40">
                    </div>
                    <img src="{player_img}" class="player-img">
                </div>
                
                <div class="card-name">{name}</div>
                <div class="stats-grid">
                    {stats_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
