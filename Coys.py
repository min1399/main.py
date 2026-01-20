import streamlit as st
import hashlib
from datetime import date
import time

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="2026 슈퍼루키 스카우팅",
    page_icon="⚽",
    layout="centered"
)

# --- 2. 디자인 CSS (배경 및 폰트) ---
st.markdown("""
    <style>
    /* 전체 배경: 고급스러운 다크 네이비 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    
    /* 텍스트 강조 스타일 */
    .highlight {
        color: #FDBB2D;
        font-weight: bold;
    }
    
    /* 카드 컨테이너 스타일 */
    div[data-testid="stContainer"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 데이터 로직 ---
def determine_destiny(name, dob):
    seed_string = f"{name}{dob}"
    hash_obj = hashlib.md5(seed_string.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # 포지션 데이터
    positions = [
        ("🧤", "GK", "수호신 골키퍼"),
        ("🛡️", "CB", "철벽 센터백"),
        ("⚡", "WB", "스피드 윙백"),
        ("🧠", "CDM", "사령관 수비형 미드필더"),
        ("⚙️", "CM", "하트비트 중앙 미드필더"),
        ("🎨", "CAM", "마에스트로 공격형 미드필더"),
        ("🚀", "LW/RW", "크랙 윙어"),
        ("🐯", "ST", "득점기계 스트라이커")
    ]
    
    # 팀 데이터 (이름, 로고 이미지 URL)
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
        ("K리그 올스타", "https://upload.wikimedia.org/wikipedia/en/thumb/5/54/K_League_Official_Logo.svg/1200px-K_League_Official_Logo.svg.png")
    ]
    
    # 프로필 이미지 (사람 실루엣 아이콘)
    profile_imgs = [
        "https://cdn-icons-png.flaticon.com/512/3048/3048122.png", # 남자1
        "https://cdn-icons-png.flaticon.com/512/3048/3048127.png", # 남자2
        "https://cdn-icons-png.flaticon.com/512/4140/4140047.png"  # 여자 느낌
    ]

    # 해시값으로 랜덤 선택
    pos_idx = hash_int % len(positions)
    team_idx = (hash_int // 10) % len(teams)
    profile_idx = (hash_int // 5) % len(profile_imgs)
    
    # 등번호 및 연봉 계산
    base_num = (hash_int % 99) + 1
    salary = (hash_int % 500) * 10 + 100 # 최소 100억부터
    
    return positions[pos_idx], teams[team_idx], base_num, salary, profile_imgs[profile_idx]

# --- 4. 메인 UI 화면 ---
st.title("⚽ 2026 슈퍼루키 스카우팅 리포트")
st.markdown("당신의 이름과 생일로 **운명의 축구 포지션**을 확인하세요!")

# 1. 입력 폼
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("선수 이름", placeholder="이름을 입력하세요")
    with col2:
        dob = st.date_input("생년월일", min_value=date(1970, 1, 1), value=date(2002, 6, 1))
    
    btn = st.button("📝 계약서 서명 및 결과 확인", type="primary")

# 2. 결과 출력
if btn and name:
    # 분석 로딩 효과
    with st.spinner(f"🌍 {name} 선수의 데이터를 빅리그 구단에 전송 중..."):
        time.sleep(1.5)
    
    # 데이터 가져오기
    (emoji, pos_code, pos_name), (team_name, team_logo), number, salary, profile_url = determine_destiny(name, dob)
    
    st.balloons() # 축하 효과
    
    # --- 결과 카드 섹션 (Streamlit Native 방식) ---
    st.markdown("### ✅ OFFICIAL ANNOUNCEMENT")
    
    # 카드 형태의 컨테이너 생성
    with st.container(border=True):
        
        # [상단] 프로필 사진과 이름
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image(profile_url, width=120) # 프로필 이미지
            st.markdown(f"<h2 style='text-align: center; color: white;'>{name}</h2>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; color: #FDBB2D; font-size: 1.2rem; margin-bottom: 20px;'>{emoji} {pos_name}</div>", unsafe_allow_html=True)

        st.divider() # 구분선

        # [중단] 팀 정보 (로고 + 팀명)
        st.markdown("#### 🏆 소속 구단 (Team)")
        t1, t2 = st.columns([1, 3])
        with t1:
            st.image(team_logo, width=70) # 팀 로고 이미지
        with t2:
            st.markdown(f"## {team_name}")
            st.caption("2026-2027 Season Contract")

        st.divider()

        # [하단] 상세 스탯 (등번호, 연봉)
        s1, s2 = st.columns(2)
        with s1:
            st.metric(label="등번호 (Back No.)", value=f"No. {number}")
        with s2:
            st.metric(label="추정 이적료 (Value)", value=f"{salary} 억 원")

        # 마지막 멘트
        st.info(f"🎤 스카우터 코멘트: \"{name} 선수는 {team_name}의 전설이 될 재목입니다!\"")

elif btn and not name:
    st.warning("⚠️ 이름을 입력해야 계약을 진행할 수 있습니다!")
