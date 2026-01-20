import streamlit as st
import hashlib
import random
import time
from datetime import date

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="OFFICIAL CONTRACT OFFER",
    page_icon="📝",
    layout="centered"
)

# --- 2. CSS 스타일 (서류 날라오는 애니메이션 + 계약서 디자인) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Playfair+Display:wght@700&display=swap');

    /* 전체 배경: 고급스러운 책상 느낌 */
    .stApp {
        background-color: #2c3e50;
        background-image: radial-gradient(#34495e 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* 📄 핵심: 서류가 날라오는 애니메이션 */
    @keyframes flyIn {
        0% { 
            transform: translateY(-1000px) rotate(-45deg) scale(0.5); 
            opacity: 0; 
        }
        60% {
            transform: translateY(30px) rotate(3deg) scale(1.02);
            opacity: 1;
        }
        80% {
            transform: translateY(-10px) rotate(-2deg);
        }
        100% { 
            transform: translateY(0) rotate(0deg) scale(1); 
            opacity: 1;
        }
    }

    /* 🔴 도장이 찍히는 애니메이션 */
    @keyframes stamp {
        0% { transform: scale(3); opacity: 0; }
        50% { transform: scale(1); opacity: 1; }
        100% { transform: scale(1) rotate(-10deg); }
    }

    /* 계약서 종이 스타일 */
    .contract-paper {
        background: #fdfbf7; /* 미색 종이 */
        width: 100%;
        max-width: 600px;
        margin: 20px auto;
        padding: 40px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        font-family: 'Courier Prime', monospace; /* 타자기 폰트 */
        color: #333;
        position: relative;
        border: 1px solid #dcdcdc;
        
        /* 애니메이션 적용 */
        animation: flyIn 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }

    /* 종이 질감 효과 */
    .contract-paper::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url("https://www.transparenttextures.com/patterns/paper.png");
        opacity: 0.5;
        pointer-events: none;
    }

    /* 헤더 (구단 로고 영역) */
    .club-header {
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }
    
    .club-logo { width: 80px; display: block; margin: 0 auto 10px auto; }
    .doc-title { font-family: 'Playfair Display', serif; font-size: 24px; font-weight: bold; letter-spacing: 1px; }

    /* 본문 내용 */
    .field-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
        border-bottom: 1px dashed #ccc;
        padding-bottom: 5px;
    }
    .label { font-weight: bold; color: #555; }
    .value { font-weight: bold; color: #000; font-size: 1.1rem; }

    /* 스카우터 코멘트 박스 */
    .scout-note {
        margin-top: 30px;
        background: #f0f0f0;
        padding: 15px;
        border-left: 4px solid #c0392b;
        font-size: 0.9rem;
        font-style: italic;
    }

    /* 도장 스타일 */
    .stamp-mark {
        position: absolute;
        bottom: 50px;
        right: 40px;
        border: 4px solid #c0392b;
        color: #c0392b;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 10px 20px;
        text-transform: uppercase;
        border-radius: 10px;
        opacity: 0; /* 처음엔 안 보임 */
        animation: stamp 0.3s cubic-bezier(0.6, 0.04, 0.98, 0.335) forwards;
        animation-delay: 1.5s; /* 종이가 착지한 뒤 찍힘 */
        transform: rotate(-10deg);
        mask-image: url("https://www.transparenttextures.com/patterns/paper.png"); /* 도장도 질감 처리 */
    }
    
    /* 서명 란 */
    .signature-area {
        margin-top: 50px;
        display: flex;
        justify-content: space-between;
    }
    .sign-box { border-top: 1px solid #333; width: 45%; padding-top: 5px; font-size: 0.8rem; text-align: center; }

    </style>
""", unsafe_allow_html=True)

# --- 3. 데이터 생성 로직 ---
def generate_contract(name, dob):
    seed = f"{name}{dob}"
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    # 구단 데이터
    clubs = [
        {"name": "Real Madrid", "logo": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg", "currency": "€"},
        {"name": "Manchester City", "logo": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg", "currency": "£"},
        {"name": "Bayern Munich", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg", "currency": "€"},
        {"name": "Paris Saint-Germain", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg", "currency": "€"},
        {"name": "Liverpool FC", "logo": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg", "currency": "£"},
        {"name": "Inter Milan", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/05/FC_Internazionale_Milano_2021.svg", "currency": "€"},
    ]
    
    # 국적 데이터
    nations = [
        ("South Korea", "🇰🇷"), ("England", "🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("Spain", "🇪🇸"), 
        ("Brazil", "🇧🇷"), ("France", "🇫🇷"), ("Germany", "🇩🇪"), 
        ("Argentina", "🇦🇷"), ("Japan", "🇯🇵")
    ]
    
    # 포지션 및 스카우터 코멘트
    positions = [
        ("ST", "Striker", "골 결정력이 월드클래스 수준임. 즉시 전력감."),
        ("LW/RW", "Winger", "폭발적인 스피드와 드리블 돌파가 인상적임."),
        ("CAM", "Playmaker", "창의적인 패스로 경기를 지배하는 마에스트로."),
        ("CDM", "Defensive Mid", "중원을 장악하는 파이터형 미드필더."),
        ("CB", "Center Back", "제공권과 대인 마크 능력이 탁월함. 통곡의 벽."),
        ("GK", "Goalkeeper", "반사 신경이 동물적임. 팀의 수호신.")
    ]

    club = clubs[h % len(clubs)]
    nation_name, nation_flag = nations[(h // 3) % len(nations)]
    pos_code, pos_name, comment = positions[(h // 7) % len(positions)]
    
    # 주급 계산 (랜덤성 + 이름 길이 보너스)
    wage_base = (h % 300) + 50 # 50k ~ 350k
    wage_str = f"{club['currency']}{wage_base},000 / week"
    
    # 계약 기간
    years = (h % 5) + 2026

    return {
        "club_name": club['name'],
        "club_logo": club['logo'],
        "player_name": name.upper(),
        "nation": f"{nation_flag} {nation_name}",
        "position": f"{pos_name} ({pos_code})",
        "wage": wage_str,
        "contract_until": f"June 30, {years}",
        "comment": comment
    }

# --- 4. 메인 UI ---
st.title("⚽ TRANSFER MARKET 2026")
st.markdown("에이전트에게 연락이 왔습니다. 이름을 입력하고 제안서를 확인하세요.")

with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        name_input = st.text_input("Player Name", placeholder="e.g. Heung-min Son")
    with col2:
        dob_input = st.date_input("Date of Birth", value=date(2002, 1, 1))
    
    # 버튼을 누르면 form submit 처리
    btn = st.button("📩 제안서 열어보기 (Open Offer)", type="primary")

if btn and name_input:
    # 1. 데이터 생성
    data = generate_contract(name_input, dob_input)
    
    # 2. 로딩 (긴장감 조성)
    with st.spinner("팩스로 서류가 들어오는 중입니다... 📠"):
        time.sleep(1.2)
    
    # 3. 계약서 HTML 렌더링 (애니메이션 포함)
    st.markdown(f"""
    <div class="contract-paper">
        <div class="club-header">
            <img src="{data['club_logo']}" class="club-logo">
            <div class="doc-title">OFFICIAL CONTRACT OFFER</div>
            <div style="font-size: 0.8rem; color: #666; margin-top:5px;">Ref: {hashlib.md5(name_input.encode()).hexdigest()[:8].upper()}</div>
        </div>

        <div class="field-row">
            <span class="label">PLAYER NAME:</span>
            <span class="value">{data['player_name']}</span>
        </div>
        <div class="field-row">
            <span class="label">NATIONALITY:</span>
            <span class="value">{data['nation']}</span>
        </div>
        <div class="field-row">
            <span class="label">POSITION:</span>
            <span class="value">{data['position']}</span>
        </div>
        <div class="field-row">
            <span class="label">WEEKLY WAGE:</span>
            <span class="value">{data['wage']}</span>
        </div>
        <div class="field-row">
            <span class="label">CONTRACT UNTIL:</span>
            <span class="value">{data['contract_until']}</span>
        </div>

        <div class="scout-note">
            <strong>👁️ CHIEF SCOUT'S REPORT:</strong><br>
            "{data['comment']}"
        </div>
        
        <div class="signature-area">
            <div class="sign-box">
                <br>Director of Football
            </div>
            <div class="sign-box">
                <br>Player's Agent
            </div>
        </div>

        <div class="stamp-mark">OFFICIAL<br>OFFER</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. 축하 효과
    time.sleep(1.5) # 도장이 찍힐 때쯤
    st.balloons()

elif btn and not name_input:
    st.error("이름을 입력해야 계약서를 확인할 수 있습니다.")
