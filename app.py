"""
Penguin - Application Banquise
Page d'accueil : Banquise Jour 1
"""
import streamlit as st
from utils import inject_penguin_css

st.set_page_config(
    page_title="Penguin - Banquise",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_penguin_css()

# Masquer le sidebar par défaut
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { display: none; }
        .stDeployButton { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# TopAppBar
st.markdown(
    """
    <div style="position:fixed;top:0;left:0;right:0;z-index:999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 1.5rem;background:rgba(255,255,255,0.9);backdrop-filter:blur(20px);box-shadow:0 4px 20px rgba(0,52,101,0.06);">
        <div style="display:flex;align-items:center;gap:0.5rem;">
            <span class="material-symbols-outlined" style="font-size:28px;color:#003465;">ice_skating</span>
            <span style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.5rem;color:#003465;">Penguin</span>
        </div>
        <div style="display:flex;align-items:center;gap:1rem;">
            <span style="font-weight:700;font-size:1rem;color:#003465;background:#00346508;padding:0.25rem 0.75rem;border-radius:999px;border:1px solid #00346520;">Jour 1</span>
            <div style="width:40px;height:40px;border-radius:50%;background:#dfe3e7;display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined" style="color:#003465;">person</span>
            </div>
        </div>
    </div>
    <div style="height:80px;"></div>
    """,
    unsafe_allow_html=True,
)

# Contenu principal
st.markdown("<div style='max-width:28rem;margin:0 auto;'>", unsafe_allow_html=True)

# Carte stats faune
st.markdown(
    """
    <div style="background:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.6);padding:1rem;border-radius:0.5rem;margin-bottom:1.5rem;backdrop-filter:blur(8px);display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0.5rem;text-align:center;">
        <div><span class="material-symbols-outlined" style="color:#326578;font-size:20px;">flutter_dash</span><div style="font-size:10px;font-weight:700;">30</div><div style="font-size:8px;text-transform:uppercase;color:#424750;">Mouettes</div></div>
        <div style="border-left:1px solid rgba(255,255,255,0.6);"><span class="material-symbols-outlined" style="color:#003465;font-size:20px;">ice_skating</span><div style="font-size:10px;font-weight:700;">1</div><div style="font-size:8px;text-transform:uppercase;color:#424750;">Penguin</div></div>
        <div style="border-left:1px solid rgba(255,255,255,0.6);"><span class="material-symbols-outlined" style="color:#004b8d;font-size:20px;">water_drop</span><div style="font-size:10px;font-weight:700;">1/6</div><div style="font-size:8px;text-transform:uppercase;color:#424750;">Orque</div></div>
        <div style="border-left:1px solid rgba(255,255,255,0.6);"><span class="material-symbols-outlined" style="color:#ba1a1a;font-size:20px;">sailing</span><div style="font-size:10px;font-weight:700;">1/12</div><div style="font-size:8px;text-transform:uppercase;color:#424750;">Requin</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Iceberg Hero
st.markdown(
    """
    <div style="position:relative;width:100%;aspect-ratio:1;max-width:28rem;margin:0 auto 2rem;background:linear-gradient(180deg,#b5e7fe 0%,#f0f4f8 100%);border-radius:1rem;overflow:hidden;">
        <div style="position:absolute;bottom:0;width:100%;height:33%;background:rgba(0,52,101,0.1);"></div>
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-2deg);width:80%;height:50%;background:#fff;border-radius:1rem;box-shadow:0 10px 40px rgba(0,0,0,0.1);border:1px solid rgba(255,255,255,0.5);display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <div style="position:absolute;top:1rem;right:2.5rem;display:flex;flex-direction:column;align-items:center;">
                <span class="material-symbols-outlined" style="font-size:32px;color:#424750;">flutter_dash</span>
                <span style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#326578;">Mouette</span>
            </div>
            <div style="display:flex;flex-direction:column;align-items:center;opacity:0.4;filter:grayscale(1);">
                <span class="material-symbols-outlined" style="font-size:64px;color:#003465;">ice_skating</span>
                <span style="font-size:12px;font-weight:700;">Dodo...</span>
            </div>
        </div>
        <div style="position:absolute;top:2.5rem;left:2.5rem;opacity:0.2;"><span class="material-symbols-outlined" style="font-size:48px;">water_drop</span></div>
        <div style="position:absolute;bottom:5rem;right:1rem;opacity:0.1;"><span class="material-symbols-outlined" style="font-size:56px;">sailing</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Bento Grid
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class="penguin-card" style="padding:1.25rem;">
            <span class="material-symbols-outlined" style="color:#326578;font-size:24px;">waves</span>
            <div style="font-family:'Plus Jakarta Sans';font-weight:700;color:#171c1f;margin-top:0.5rem;">Océan</div>
            <div style="font-size:12px;color:#424750;">-2°C Arctique</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="penguin-card" style="padding:1.25rem;">
            <span class="material-symbols-outlined" style="color:#4f2b00;font-size:24px;">warning</span>
            <div style="font-family:'Plus Jakarta Sans';font-weight:700;color:#171c1f;margin-top:0.5rem;">Danger</div>
            <div style="font-size:12px;color:#424750;">Requin & Orque</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Popup "Tu as tué le pinguin ?"
st.markdown(
    """
    <div style="text-align:center;padding:2rem;background:rgba(255,255,255,0.9);border-radius:1rem;box-shadow:0 4px 20px rgba(0,52,101,0.08);margin-top:1rem;">
        <div style="width:96px;height:96px;margin:0 auto 1.5rem;background:linear-gradient(135deg,#003465,#004b8d);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 32px rgba(0,52,101,0.2);">
            <span class="material-symbols-outlined" style="font-size:48px;color:white;">ice_skating</span>
        </div>
        <h2 style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.5rem;color:#003465;margin-bottom:0.75rem;">Tu as tué le pinguin ?</h2>
        <p style="color:#424750;margin-bottom:1.5rem;">Secoue toi pour le ramener sur sa banquise !</p>
    </div>
    """,
    unsafe_allow_html=True,
)
if st.button("🔄 Réinitialiser (Secouer)", type="primary", use_container_width=True):
    st.success("Manchot réveillé ! 🐧")
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# BottomNavBar (Streamlit page_link)
st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    st.page_link("app.py", label="Banquise", icon="🏠")
with nav_col2:
    st.page_link("pages/1_Vue_Illustree.py", label="Vue", icon="🧊")
with nav_col3:
    st.page_link("pages/3_Amis.py", label="Amis", icon="👥")
with nav_col4:
    st.page_link("pages/2_Profil.py", label="Profil", icon="👤")
