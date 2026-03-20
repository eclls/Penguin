"""
Penguin - Vue Illustrée (Jour 256)
Écosystème polaire avec manchots, goélands, orque
"""
import streamlit as st
from utils import inject_penguin_css

st.set_page_config(
    page_title="Vue Illustrée - Penguin",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_penguin_css()

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
        <div style="display:flex;align-items:center;gap:0.75rem;">
            <span class="material-symbols-outlined" style="font-size:28px;color:#003465;">ice_skating</span>
            <span style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.25rem;color:#003465;">23 Octobre</span>
        </div>
        <div style="display:flex;align-items:center;gap:0.5rem;background:#dfe3e7;padding:0.25rem 1rem;border-radius:999px;">
            <span style="font-size:10px;font-weight:700;color:#003465;letter-spacing:0.15em;">EN DIRECT</span>
            <div style="width:8px;height:8px;border-radius:50%;background:#ba1a1a;animation:pulse 1.5s infinite;"></div>
        </div>
    </div>
    <div style="height:80px;"></div>
    """,
    unsafe_allow_html=True,
)

# Hero Jour 256
st.markdown(
    """
    <div style="text-align:center;margin-bottom:2.5rem;">
        <span style="font-size:0.75rem;color:#37697d;font-weight:500;text-transform:uppercase;letter-spacing:0.2em;">Expédition Polaire</span>
        <h1 style="font-family:'Plus Jakarta Sans';font-size:3rem;font-weight:800;color:#003465;margin:0.5rem 0;">Jour 256</h1>
        <p style="color:#424750;margin-top:0.5rem;max-width:20rem;margin-left:auto;margin-right:auto;">La glace dérive doucement vers le sud. L'écosystème est stable.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Canvas Banquise (simplifié)
st.markdown(
    """
    <div style="position:relative;width:100%;aspect-ratio:4/5;max-width:32rem;margin:0 auto;border-radius:1rem;overflow:hidden;background:linear-gradient(180deg,#bbe9ff 0%,#f0f4f8 100%);box-shadow:0 24px 48px rgba(0,52,101,0.06);">
        <div style="position:absolute;top:1.5rem;left:1.5rem;display:flex;flex-direction:column;gap:0.5rem;">
            <div style="background:rgba(0,52,101,0.1);backdrop-filter:blur(12px);padding:0.25rem 0.75rem;border-radius:999px;display:flex;align-items:center;gap:0.5rem;">
                <span class="material-symbols-outlined" style="font-size:14px;color:#003465;">waves</span>
                <span style="font-size:12px;font-weight:700;color:#003465;">Eau : -1.8°C</span>
            </div>
        </div>
        <div style="position:absolute;inset:0;padding:2rem;display:flex;flex-direction:column;justify-content:center;align-items:center;">
            <div style="background:rgba(255,255,255,0.9);backdrop-filter:blur(20px);width:16rem;padding:2rem;border-radius:3rem;transform:rotate(-5deg);box-shadow:0 24px 48px rgba(0,52,101,0.06);display:flex;flex-direction:column;align-items:center;gap:1rem;">
                <div style="display:flex;gap:2rem;align-items:flex-end;">
                    <div style="display:flex;flex-direction:column;align-items:center;">
                        <span class="material-symbols-outlined" style="font-size:60px;color:#003465;font-variation-settings:'FILL' 1;">child_care</span>
                        <span style="font-size:10px;font-weight:700;color:rgba(0,52,101,0.6);text-transform:uppercase;">Pingu</span>
                    </div>
                    <div style="display:flex;flex-direction:column;align-items:center;padding-bottom:0.5rem;">
                        <span class="material-symbols-outlined" style="font-size:48px;color:rgba(0,52,101,0.8);font-variation-settings:'FILL' 1;">child_care</span>
                        <span style="font-size:10px;font-weight:700;color:rgba(0,52,101,0.6);text-transform:uppercase;">Pingo</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Stats Bento
st.markdown("<div style='max-width:32rem;margin:2rem auto;'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div style="background:#f0f4f8;padding:1.5rem;border-radius:0.5rem;display:flex;flex-direction:column;gap:0.75rem;">
            <div style="width:40px;height:40px;border-radius:50%;background:#b5e7fe;display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined" style="color:#37697d;">groups</span>
            </div>
            <span style="font-size:1.5rem;font-weight:700;color:#003465;">19</span>
            <span style="font-size:0.875rem;color:#37697d;font-weight:500;">Habitants Actifs</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div style="background:#f0f4f8;padding:1.5rem;border-radius:0.5rem;display:flex;flex-direction:column;gap:0.75rem;">
            <div style="width:40px;height:40px;border-radius:50%;background:#ffdcbe;display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined" style="color:#693c00;">wb_sunny</span>
            </div>
            <span style="font-size:1.5rem;font-weight:700;color:#003465;">22h</span>
            <span style="font-size:0.875rem;color:#37697d;font-weight:500;">Lumière du jour</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Liste Faune
st.markdown(
    """
    <h3 style="font-family:'Plus Jakarta Sans';font-size:1.125rem;font-weight:700;color:#003465;margin:2.5rem 0 1rem 0.5rem;">Détails de la Faune</h3>
    <div style="display:flex;flex-direction:column;gap:0.75rem;">
        <div style="background:#fff;padding:1rem;border-radius:0.5rem;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:48px;height:48px;border-radius:50%;background:#eaeef2;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="color:#003465;">sailing</span>
                </div>
                <div>
                    <span style="font-weight:700;color:#171c1f;">Orque Majestueuse</span>
                    <div style="font-size:12px;color:#424750;">Souverain des profondeurs</div>
                </div>
            </div>
            <span style="font-size:1.125rem;font-weight:700;color:#003465;">1</span>
        </div>
        <div style="background:#fff;padding:1rem;border-radius:0.5rem;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:48px;height:48px;border-radius:50%;background:#eaeef2;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="color:#003465;">child_care</span>
                </div>
                <div>
                    <span style="font-weight:700;color:#171c1f;">Manchots Empereurs</span>
                    <div style="font-size:12px;color:#424750;">Gardiens de la glace</div>
                </div>
            </div>
            <span style="font-size:1.125rem;font-weight:700;color:#003465;">2</span>
        </div>
        <div style="background:#fff;padding:1rem;border-radius:0.5rem;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:48px;height:48px;border-radius:50%;background:#eaeef2;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="color:#003465;">airplanemode_active</span>
                </div>
                <div>
                    <span style="font-weight:700;color:#171c1f;">Goélands Arctiques</span>
                    <div style="font-size:12px;color:#424750;">Messagers du ciel</div>
                </div>
            </div>
            <span style="font-size:1.125rem;font-weight:700;color:#003465;">16</span>
        </div>
    </div>
    </div>
    <div style="height:120px;"></div>
    """,
    unsafe_allow_html=True,
)

# Bottom Nav
st.markdown(
    """
    <div style="position:fixed;bottom:0;left:0;right:0;z-index:999;display:flex;justify-content:space-around;align-items:center;padding:0.75rem 1rem 1.5rem;background:rgba(255,255,255,0.9);backdrop-filter:blur(20px);box-shadow:0 -12px 24px rgba(0,52,101,0.04);border-radius:2rem 2rem 0 0;">
        <a href="/" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1.25rem;text-decoration:none;"><span class="material-symbols-outlined">home</span><span style="font-size:11px;">Accueil</span></a>
        <a href="/Vue_Illustree" style="display:flex;flex-direction:column;align-items:center;background:#00346520;color:#003465;padding:0.5rem 1.25rem;border-radius:999px;text-decoration:none;"><span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">ac_unit</span><span style="font-size:11px;">Banquise</span></a>
        <a href="#" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1.25rem;text-decoration:none;"><span class="material-symbols-outlined">notifications</span><span style="font-size:11px;">Alertes</span></a>
        <a href="/Profil" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1.25rem;text-decoration:none;"><span class="material-symbols-outlined">person</span><span style="font-size:11px;">Profil</span></a>
    </div>
    """,
    unsafe_allow_html=True,
)
