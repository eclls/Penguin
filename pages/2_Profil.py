"""
Penguin - Profil Utilisateur
"""
import streamlit as st
from utils import inject_penguin_css

st.set_page_config(
    page_title="Profil - Penguin",
    page_icon="👤",
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
        <div style="display:flex;align-items:center;gap:0.5rem;">
            <span class="material-symbols-outlined" style="font-size:28px;color:#003465;">ice_skating</span>
            <span style="font-family:'Plus Jakarta Sans';font-weight:700;font-size:1.5rem;color:#003465;">Penguin</span>
        </div>
        <span class="material-symbols-outlined" style="color:#64748b;font-size:24px;">settings</span>
    </div>
    <div style="height:96px;"></div>
    """,
    unsafe_allow_html=True,
)

# Hero Profile Card
st.markdown(
    """
    <div style="max-width:32rem;margin:0 auto 3rem;">
    <div style="background:#fff;border-radius:1rem;padding:2rem;box-shadow:0 24px 48px rgba(0,52,101,0.06);display:flex;flex-direction:column;align-items:center;">
        <div style="position:relative;width:128px;height:128px;margin-bottom:1.5rem;">
            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuDf9-WBEHOlycBT-kSzeUCU5x7UY-FRTWHH5_i9e2ght8N32aaFrzqIiZA14KwNYgkDAgSsNzBsXkCmyrn1gMU76fnlknewXV_-h5lcKUBjlg160Al_hYOd0ZKFrsX0toLETCGGt6tPmQzYQfMd6dxumb3yFDl-pyCxHdgP4xEhbz8Udl6BRObZA7Ysro7565JVUqS0fdt1Igl5ph9gtpJ40XM-ZBCqdUXOt2I78gCNoe8KvX9pFKtZPkSTdmO-YTjT6uhOmm7fKE0" alt="Avatar" style="width:100%;height:100%;object-fit:cover;border-radius:50%;border:4px solid white;box-shadow:0 10px 30px rgba(0,0,0,0.15);"/>
            <div style="position:absolute;bottom:0;right:0;background:#ffdcbe;padding:0.5rem;border-radius:50%;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                <span class="material-symbols-outlined" style="font-size:14px;color:#4f2b00;font-variation-settings:'FILL' 1;">edit</span>
            </div>
        </div>
        <h1 style="font-family:'Plus Jakarta Sans';font-size:1.875rem;font-weight:700;color:#171c1f;margin:0 0 0.25rem;">Adélie Explorateur</h1>
        <p style="font-size:0.75rem;color:#37697d;text-transform:uppercase;letter-spacing:0.15em;font-weight:600;margin-bottom:2rem;">Maître des Glaces • Niv. 42</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;width:100%;">
            <div style="background:#f0f4f8;padding:1.25rem;border-radius:0.5rem;text-align:center;">
                <span style="font-size:1.875rem;font-weight:800;color:#003465;">248</span>
                <div style="font-size:10px;color:#37697d;text-transform:uppercase;letter-spacing:0.1em;margin-top:0.25rem;">Jours Survécus</div>
            </div>
            <div style="background:#f0f4f8;padding:1.25rem;border-radius:0.5rem;text-align:center;">
                <span style="font-size:1.875rem;font-weight:800;color:#003465;">12.4k</span>
                <div style="font-size:10px;color:#37697d;text-transform:uppercase;letter-spacing:0.1em;margin-top:0.25rem;">Poissons Récoltés</div>
            </div>
        </div>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Paramètres
st.markdown(
    """
    <div style="max-width:32rem;margin:0 auto;">
    <h2 style="font-family:'Plus Jakarta Sans';font-size:1.25rem;font-weight:700;margin-bottom:1rem;padding:0 0.5rem;">Paramètres de l'expédition</h2>
    <div style="background:#fff;border-radius:0.5rem;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">
        <div style="display:flex;align-items:center;justify-content:space-between;padding:1.25rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:40px;height:40px;border-radius:50%;background:#f0f4f8;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="color:#003465;">notifications</span>
                </div>
                <div>
                    <span style="font-weight:600;">Notifications</span>
                    <div style="font-size:0.875rem;color:#424750;">Alertes de tempête et amis</div>
                </div>
            </div>
            <div style="width:48px;height:24px;background:#003465;border-radius:999px;padding:2px;position:relative;">
                <div style="width:20px;height:20px;background:white;border-radius:50%;transform:translateX(24px);"></div>
            </div>
        </div>
        <div style="border-top:1px solid #dfe3e7;display:flex;align-items:center;justify-content:space-between;padding:1.25rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:40px;height:40px;border-radius:50%;background:#f0f4f8;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="color:#003465;">security</span>
                </div>
                <div>
                    <span style="font-weight:600;">Confidentialité</span>
                    <div style="font-size:0.875rem;color:#424750;">Visibilité de votre banquise</div>
                </div>
            </div>
            <span class="material-symbols-outlined" style="color:#727782;">chevron_right</span>
        </div>
        <div style="border-top:1px solid #dfe3e7;display:flex;align-items:center;justify-content:space-between;padding:1.25rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:40px;height:40px;border-radius:50%;background:#f0f4f8;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="color:#003465;">language</span>
                </div>
                <div>
                    <span style="font-weight:600;">Langue</span>
                    <div style="font-size:0.875rem;color:#424750;">Français (Arctique)</div>
                </div>
            </div>
            <span class="material-symbols-outlined" style="color:#727782;">chevron_right</span>
        </div>
        <div style="border-top:1px solid #dfe3e7;display:flex;align-items:center;justify-content:space-between;padding:1.25rem;">
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="width:40px;height:40px;border-radius:50%;background:#f0f4f8;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="color:#003465;">calendar_today</span>
                </div>
                <div>
                    <span style="font-weight:600;">Ajuster le jour de départ</span>
                    <div style="font-size:0.875rem;color:#424750;">Modifier manuellement votre progression</div>
                </div>
            </div>
            <span class="material-symbols-outlined" style="color:#727782;">chevron_right</span>
        </div>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Bouton Déconnexion
st.markdown("<div style='max-width:32rem;margin:2rem auto;'>", unsafe_allow_html=True)
if st.button("🚪 Déconnexion de la Banquise", type="secondary", use_container_width=True):
    st.warning("Déconnexion simulée !")

st.markdown(
    """
    <p style="text-align:center;margin-top:1.5rem;font-size:12px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.1em;">Version 2.4.0 • Penguin Editorial</p>
    <div style="height:120px;"></div>
    """,
    unsafe_allow_html=True,
)

# Bottom Nav
st.markdown(
    """
    <div style="position:fixed;bottom:0;left:0;right:0;z-index:999;display:flex;justify-content:space-around;align-items:center;padding:0.75rem 1rem 1.5rem;background:rgba(255,255,255,0.9);backdrop-filter:blur(20px);box-shadow:0 -12px 32px rgba(0,52,101,0.04);border-radius:2rem 2rem 0 0;">
        <a href="/" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1.25rem;text-decoration:none;"><span class="material-symbols-outlined">home</span><span style="font-size:10px;">Banquise</span></a>
        <a href="/Amis" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1.25rem;text-decoration:none;"><span class="material-symbols-outlined">group</span><span style="font-size:10px;">Friends</span></a>
        <a href="#" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1.25rem;text-decoration:none;"><span class="material-symbols-outlined">notifications</span><span style="font-size:10px;">Alerts</span></a>
        <a href="/Profil" style="display:flex;flex-direction:column;align-items:center;background:#003465;color:white;padding:0.5rem 1.25rem;border-radius:999px;text-decoration:none;"><span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">person</span><span style="font-size:10px;">Profile</span></a>
    </div>
    """,
    unsafe_allow_html=True,
)
