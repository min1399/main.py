import streamlit as st
st.title("first web app")
st.write('Welcome!')
import streamlit as st
import time
import random

# --- 1. 페이지 및 세션 상태 설정 ---
st.set_page_config(
    page_title="⚽ 나만의 축구 포지션 찾기 Pro",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화 (GIF 표시 여부 제어용)
if 'show_gif_overlay' not in st.session_state:
    st.session_state.show_gif_overlay = False
if 'current_gif_url' not in st.session_state:
    st.session_state.current_gif_url = ""


# --- 2. 커스텀 CSS (화려한 디자인 + 움짤 효과) ---
st.markdown("""
    <style>
    /* 전체 배경: 기본 축구장 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        transition: background 0.5s ease;
    }
    
    /* --- ✨ 핵심: 일시적 배경 움짤 오버레이 애니메이션 --- */
    @keyframes magicBackgroundFade {
        0% { opacity: 0; z-index: 9998; }
        10% { opacity: 1; z-index: 9998; } /* 빠르게 나타남 */
        75% { opacity: 1; z-index: 9998; } /* 잠시 유지 */
        100% { opacity: 0; z-index: -1; pointer-events: none;} /* 사라지고 클릭 통과 */
    }
    
    .gif-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        /* 배경을 어둡게 깔고 그 위에 GIF를 중앙에 배치 */
        background-color: rgba(0,0,0,0.7); 
        background-repeat: no-repeat;
        background-position: center center;
        background-size: contain; /* GIF가 잘리지 않게 */
        
        /* 애니메이션 적용: 4초 동안 실행 */
        animation: magicBackgroundFade 4s forwards ease-in-out;
    }

    /* 메인 타이틀 스타일 */
    .title-text {
        color: #ffffff;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7);
        margin-bottom: 20px;
    }
    
    /* 결과 카드 스타일 (조금 더 고급스럽게) */
    .player-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        border: 4px solid #D4AF37; /* 골드 테두리 */
        animation: slideUp 0.8s ease-out;
        position: relative;
        z-index: 1; /* GIF보다 앞에 오도록 */
    }
    
    .match-player-badge {
        background-color: #D4AF37;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 10px;
        display: inline-block;
    }

    .position-name {
        color: #2c3e50;
        font-size: 2.2rem;
        font-weight: 900;
        margin: 15px 0;
    }
    
    .desc-text {
        color: #555;
        font-size: 1.15rem;
        line-height: 1.7;
    }
    
    .big-emoji {
        font-size: 6rem;
        display: block;
        margin-bottom: 5px;
        text-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }

    /* 버튼 스타일링 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff4b1f, #ff9068);
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        border-radius: 15px;
        padding: 12px;
        border: none;
        box-shadow: 0 5px 15px rgba(255, 75, 31, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(255, 75, 31, 0.6);
    }
    
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(50px); }
        100% { opacity: 1; transform: translateY(0); }
