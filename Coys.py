import streamlit as st
import time

# --- 1. 페이지 및 세션 상태 설정 ---
st.set_page_config(
    page_title="⚽ 나만의 축구 포지션 찾기 Pro",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if 'show_gif_overlay' not in st.session_state:
    st.session_state.show_gif_overlay = False
if 'current_gif_url' not in st.session_state:
    st.session_state.current_gif_url = ""

# --- 2. 커스텀 CSS (수정됨: IMG 태그 방식 적용) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* --- ✨ 배경 움짤 오버레이 (수정됨) --- */
    @keyframes magicBackgroundFade {
        0% { opacity: 0; z-index: 9998; }
        10% { opacity: 1; z-index: 9998; }
        80% { opacity: 1; z-index: 9998; }
        100% { opacity: 0; z-index: -1; pointer-events: none;}
    }
    
    .gif-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0,0,0,0.85); /* 배경을 더 어둡게 */
        display: flex;
        justify-content: center;
        align-items: center;
        animation: magicBackgroundFade 4s forwards ease-in-out;
    }
    
    /* 이미지가 화면 중앙에 예쁘게 뜨도록 설정 */
    .gif-overlay img {
        max-width: 90%;
        max-height: 80%;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
        object-fit: contain;
    }

    /* 타이틀 및 카드 스타일 */
    .title-text {
        color: #ffffff;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7);
        margin-bottom: 20px;
    }
    
    .player-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        border: 4px solid #D4AF37;
        animation: slideUp 0.8s ease-out;
        position: relative;
        z-index: 1;
    }
    
    .match-player-badge {
        background-color: #D4AF37;
        color: white;
