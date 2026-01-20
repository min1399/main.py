import streamlit as st
import hashlib
import time
from datetime import date
import streamlit.components.v1 as components

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="FC 2026 PACK OPENING",
    page_icon="⚽",
    layout="centered"
)

# --- 2. 🚀 핵심 기술: 자바스크립트(JS)로 만든 3D 워프 애니메이션 ---
# 이 코드는 외부 이미지가 아니라, 사용자의 브라우저에서 실시간으로 그래픽을 그려냅니다.
def warp_animation_code():
    return """
    <canvas id="warpCanvas"></canvas>
    <script>
    document.body.style.overflow = 'hidden'; // 스크롤 방지
    const canvas = document.getElementById('warpCanvas');
    const ctx = canvas.getContext('2d');
    
    // 캔버스를 화면 전체로 설정
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '9998'; // 텍스트보다 뒤, 배경보다 앞
    canvas.style.background = 'black';
    
    let width, height;
    let stars = [];
    const numStars = 600; // 별의 개수 (많을수록 화려함)
    const speed = 25; // 속도 (빠를수록 박진감 넘침)

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        
        // 캔버스 중심 설정
        ctx.translate(width / 2, height / 2);
    }
    
    class Star {
        constructor() {
            this.reset();
        }
        reset() {
            this.x = (Math.random() - 0.5) * width * 2;
            this.y = (Math.random() - 0.5) * height * 2;
            this.z = Math.random() * width; // 깊이감
            this.pz = this.z;
        }
        update() {
            this.z = this.z - speed;
            if (this.z < 1) {
                this.reset();
                this.z = width;
                this.pz = this.z;
            }
        }
        show() {
            let sx = (this.x / this.z) * width;
            let sy = (this.y / this.z) * height;
            
            let px = (this.x / this.pz) * width;
            let py = (this.y / this.pz) * height;
            
            this.pz = this.z;
            
            ctx.beginPath();
            ctx.strokeStyle = "rgba(255, 255, 255, " + (1 - this.z / width) + ")";
            ctx.lineWidth = (1 - this.z / width) * 4; // 가까울수록 두껍게
            ctx.moveTo(px, py);
            ctx.lineTo(sx, sy);
            ctx.stroke();
        }
    }

    function init() {
        resize();
        stars = [];
        for (let i = 0; i < numStars; i++) {
            stars.push(new Star());
        }
        animate();
    }

    function animate() {
        // 꼬리 잔상 효과를 위해 약간 투명한 검은색으로 덮음
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)"; 
        ctx.fillRect(-width/2, -height/2, width, height);
        
        for (let star of stars) {
            star.update();
            star.show();
        }
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', resize);
    init();
    
    // 5초 뒤에 자동으로 사라지게 설정 (파이썬 로직과 싱크 맞춤)
    setTimeout(() => {
        canvas.style.transition = 'opacity 1s ease';
        canvas.style.opacity = '0';
        setTimeout(() => { canvas.remove(); }, 1000);
    }, 4500);
    </script>
    """

# --- 3. CSS 스타일링 (카드 및 텍스트) ---
st.markdown("""
    <style>
    /* 기본 배경 */
    .stApp {
        background: radial-gradient(circle at center, #111 0%, #000 100%);
        color: white;
    }

    /* 워크아웃 텍스트 (화면 중앙, 아주 크게) */
    .walkout-container {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999; /* 워프 효과보다 더 앞에 */
        text-align: center;
        width: 100%;
        pointer-events: none;
    }
    
    .walkout-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 7rem;
        font-weight: 900;
        color: #fff;
        text-transform: uppercase;
        text-shadow: 0 0 20px #f1c40f, 0 0 50px #f1c40f;
        animation: zoomIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .walkout-img {
        width: 250px;
        filter: drop-shadow(0 0 40px #fff);
        animation: zoomIn 0.5s;
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
        animation: cardReveal 1s ease-out;
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
    
    .stats-grid {
        display: grid; grid-template-columns: 1fr 1fr; gap: 5px 30px;
        padding: 10px 30px; font-weight: 800; font-size: 1.2rem; color: #3d3122; text-align: left;
    }
    
    @keyframes zoomIn { from { transform: scale(0); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    @keyframes cardReveal { from { transform: translateY(100px) scale(0.8); opacity: 0; } to { transform: translateY(0) scale(1); opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 데이터 로직 ---
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
        
    player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048122.png"
    if ovr >= 90:
         player_img = "https://cdn-icons-png.flaticon.com/512/3048/3048127.png"

    return pos, flag, team_logo, ovr, stats, player_img

# --- 5. 메인 UI ---
st.markdown("<h1 style='text-align: center; color: #f1c40f; text-shadow: 0 0 20px #f1c40f;'>🚀 HYPER WARP PACK 🚀</h1>", unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2)
    name_input = c1.text_input("Player Name", placeholder="SON")
    dob_input = c2.date_input("Birth Date", value=date(2000, 1, 1))
    
    if st.button("🔥 워프 엔진 가동 (팩 개봉) 🔥", type="primary"):
        if not name_input:
            st.error("이름을 입력해주세요!")
        else:
            # 1. 데이터 생성
            pos, flag, team_logo, ovr, stats, player_img = generate_player_data(name_input, dob_input)
            
            # 2. [핵심] 3D 워프 애니메이션 자바스크립트 주입
            # components.html을 사용하지 않고 markdown으로 직접 넣어야 전체 화면에 적용됨
            st.markdown(warp_animation_code(), unsafe_allow_html=True)
            
            placeholder = st.empty()
            
            # 3. 워프 진행 중... 텍스트 연출 (싱크 맞춤)
            time.sleep(1.0) # 속도감 증가
            
            # 국기
            placeholder.markdown(f"<div class='walkout-container'><div class='walkout-text'>{flag}</div></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            # 포지션
            placeholder.markdown(f"<div class='walkout-container'><div class='walkout-text'>{pos}</div></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            # 구단 로고
            placeholder.markdown(f"<div class='walkout-container'><img src='{team_logo}' class='walkout-img'></div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            # 4. 카드 최종 공개
            placeholder.empty() # 텍스트 지움
            # (캔버스는 자바스크립트가 알아서 4.5초 뒤에 사라짐)
            
            st.balloons()
            
            # 카드 렌더링
            stats_html = ""
            if pos == "GK":
                labels = [("DIV", stats["DIV"]), ("HAN", stats["HAN"]), ("KIC", stats["KIC"]), ("REF", stats["REF"]), ("SPD", stats["SPD"]), ("POS", stats["POS"])]
            else:
                labels = [("PAC", stats["PAC"]), ("SHO", stats["SHO"]), ("PAS", stats["PAS"]), ("DRI", stats["DRI"]), ("DEF", stats["DEF"]), ("PHY", stats["PHY"])]
            
            for label, val in labels:
                stats_html += f"<div style='display:flex; justify-content:space-between;'><span style='font-weight:900; font-size:1.3rem;'>{val}</span><span style='font-size:1rem; opacity:0.8;'>{label}</span></div>"

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
