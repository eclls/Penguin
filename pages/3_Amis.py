"""
Penguin - Amis & Social
Communauté polaire, colonie, suggestions
"""
import streamlit as st
from utils import inject_penguin_css

st.set_page_config(
    page_title="Amis - Penguin",
    page_icon="👥",
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
            <span style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:1.5rem;color:#003465;">Penguin</span>
        </div>
        <div style="display:flex;align-items:center;gap:1rem;">
            <div style="width:40px;height:40px;border-radius:50%;background:#f0f4f8;display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined" style="color:#003465;">search</span>
            </div>
            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBpoIby-GO0QuvzDHPOEllPdkY6wWrnaBZfssJhLvPuc_exHj1-B_zOkSjHrOylBQp2aPJgtDlJkQFjcypp01B-E9lypYUqG6E9mmX_metz8q3TsAQHZ0XALTGkh_uWVRRwxCQHgEUDKbgQEh4lsyv84kv259dzohDey2sgxmnKO_jafAuRc2o7fIHZXHo1n76NpE_Z3E41zg5l6nBX-JIE05B-PXOAMotbukpDnS1P7Iwx414-_0vyJaVCCnDVFU0Tq-LzLRNsdBI" alt="Profil" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid #91bdff;"/>
        </div>
    </div>
    <div style="height:96px;"></div>
    """,
    unsafe_allow_html=True,
)

# Hero Section
st.markdown(
    """
    <div style="max-width:40rem;margin:0 auto 2.5rem;">
    <div style="background:linear-gradient(135deg,#003465,#004b8d);padding:2rem 3rem;border-radius:1rem;color:white;overflow:hidden;position:relative;box-shadow:0 25px 50px rgba(0,52,101,0.3);">
        <span style="font-size:0.875rem;letter-spacing:0.2em;opacity:0.8;display:block;margin-bottom:1rem;">Communauté Polaire</span>
        <h1 style="font-family:'Plus Jakarta Sans';font-size:2.5rem;font-weight:800;margin-bottom:1.5rem;line-height:1.2;">Tes compagnons de dérive.</h1>
        <p style="color:rgba(255,255,255,0.9);font-size:1.125rem;line-height:1.6;margin-bottom:2rem;">Suis la production de ressources de ta colonie et compare tes gains horaires avec tes amis.</p>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Bouton Ajouter des Amis
if st.button("➕ Ajouter des Amis", type="primary", use_container_width=True):
    st.info("Fonctionnalité à venir !")

# Stats Overview
st.markdown(
    """
    <div style="max-width:40rem;margin:2rem auto;">
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
        <div style="background:#fff;padding:1.25rem;border-radius:1rem;display:flex;align-items:center;gap:1.25rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #e4e9ed;">
            <div style="width:48px;height:48px;border-radius:50%;background:#b5e7fe;display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined" style="color:#37697d;">groups</span>
            </div>
            <div>
                <div style="font-size:1.25rem;font-weight:700;color:#003465;">24</div>
                <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#424750;">Amis Actifs</div>
            </div>
        </div>
        <div style="background:#fff;padding:1.25rem;border-radius:1rem;display:flex;align-items:center;gap:1.25rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #e4e9ed;">
            <div style="width:48px;height:48px;border-radius:50%;background:rgba(111,63,0,0.2);display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined" style="color:#4f2b00;">leaderboard</span>
            </div>
            <div>
                <div style="font-size:1.25rem;font-weight:700;color:#003465;">Niv. 12</div>
                <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#424750;">Moyenne Colonie</div>
            </div>
        </div>
        <div style="background:#fff;padding:1.25rem;border-radius:1rem;display:flex;align-items:center;gap:1.25rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #e4e9ed;">
            <div style="width:48px;height:48px;border-radius:50%;background:#d4e3ff;display:flex;align-items:center;justify-content:center;">
                <span class="material-symbols-outlined" style="color:#001c3a;">rocket_launch</span>
            </div>
            <div>
                <div style="font-size:1.25rem;font-weight:700;color:#003465;">85%</div>
                <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.1em;color:#424750;">Objectif Commun</div>
            </div>
        </div>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Ma Colonie
st.markdown(
    """
    <div style="max-width:40rem;margin:2rem auto;">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:1.5rem;padding:0 0.5rem;">
        <div>
            <h2 style="font-family:'Plus Jakarta Sans';font-size:1.5rem;font-weight:700;color:#171c1f;">Ma Colonie</h2>
            <p style="font-size:0.875rem;color:#424750;">Status des ressources par heure.</p>
        </div>
        <span style="font-size:0.875rem;font-weight:700;color:#003465;">Tout voir →</span>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Cartes amis
amis = [
    {"nom": "Lars l'Explorateur", "status": "En ligne", "status_color": "#22c55e", "badge": "ELITE", "badge_style": "background:#e4e9ed;color:#37697d;", "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuAVhql6HATDPWj9HDlvitW2OfIuZTGNw2P1YzP-wldqFZ1oN0IV_WvkyEcZuPJ4-JnN7UEthV_3CA1SEYzVJKsv3m8HnInnNoYmpBrd4yqfwu-RTeP9KPLL3OGsc5AJPueQdXoxvEMbylwij7MmiB4yB5wCjOwnAgF5_9vj2BnXGZfDrV3iZlPiR73X8k9H0ewpSeSW70UXYFCzk_SLdZgeDExsSXYDcl4Ouc8-kuFTsEjppk3GftLO5OX-9PKQh_W8lnPXxbx_Zi0", "orques": "2", "pingouins": "1", "mouettes": "12"},
    {"nom": "Sven Le Malin", "status": "Pêche en cours...", "status_color": "#f97316", "badge": "AMI PROCHE", "badge_style": "background:#ffdcbe;color:#4f2b00;", "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuBapBNnaT5C-wl23-DAypVgeDHlsIwLLohkvS3AM1Cs-M7xHDg6HvzUZ_tuh_r4eYQgQioarqfTeguSWcMvgJ4JRj6PHOdI4M2mXrtecwt5Xm0jGhM0-y_WJQq794UHjDmr9U7nu8wnN9G9utej39sqPa2DDT88nbY6py94mtqcgozKOuzh6RXLH6v-CW5QGKwd5AF_9SUZADmBJFz9hC8nA25rW7Qet02Y_hd-qYtpIsVs6rmHrYbG50LHUUCua5KmOUT68K1WBC4", "orques": "0", "pingouins": "4", "mouettes": "8"},
    {"nom": "Olga des Neiges", "status": "Activité : hier", "status_color": "#94a3b8", "badge": "", "badge_style": "", "avatar": "https://lh3.googleusercontent.com/aida-public/AB6AXuA7F6oMP0cdyARoo8-mtme26989nIg4NTxtEIxa541AHWMlxTFUDJDPReGhGD4CETcvLgN0XC3MfJKKxZqFVpiuqzp29l1ubcDIlHWqp1M4xV-2A8AfURtk1rOXHwbH3BZ-tWKamdcM52s0k619hHYZIqxBvkp96TM6xZsTRs-KW9n5Jq51Fg996cy1s7iUnLZm_UM9Jv7UTbnZXL49rvzvtrh1yBF8WiYVu_Y-JU90RDiWjD_jb19iXhqatMYiwtulB6clGF9Rflc", "orques": "1", "pingouins": "0", "mouettes": "32"},
]

for ami in amis:
    badge_html = f'<span style="padding:0.25rem 0.5rem;border-radius:4px;font-size:10px;font-weight:700;text-transform:uppercase;{ami["badge_style"]}">{ami["badge"]}</span>' if ami["badge"] else ""
    st.markdown(
        f"""
        <div style="max-width:40rem;margin:0 auto 1.5rem;">
        <div style="background:#fff;padding:1.5rem;border-radius:1rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #e4e9ed;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.5rem;">
                <div style="display:flex;align-items:center;gap:1rem;">
                    <div style="position:relative;">
                        <img src="{ami['avatar']}" alt="{ami['nom']}" style="width:64px;height:64px;border-radius:1rem;object-fit:cover;border:4px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.1);"/>
                        {"<div style='position:absolute;bottom:-4px;right:-4px;width:20px;height:20px;background:#22c55e;border:2px solid white;border-radius:50%;'></div>" if ami['status_color'] == '#22c55e' else ""}
                    </div>
                    <div>
                        <h3 style="font-family:'Plus Jakarta Sans';font-size:1.125rem;font-weight:700;margin:0 0 0.25rem;">{ami['nom']}</h3>
                        <p style="font-size:12px;color:#424750;display:flex;align-items:center;gap:0.25rem;">
                            {"<span style='width:8px;height:8px;border-radius:50%;background:" + ami['status_color'] + ";'></span>" if ami['status_color'] != '#94a3b8' else ""}
                            {ami['status']}
                        </p>
                    </div>
                </div>
                {badge_html}
            </div>
            <div style="background:#f0f4f8;padding:1rem;border-radius:0.75rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;margin-bottom:0.5rem;">
                    <span style="display:flex;align-items:center;gap:0.5rem;color:#424750;"><span class="material-symbols-outlined" style="font-size:14px;color:#003465;">sailing</span>{ami['orques']} Orques /h</span>
                    <span style="font-weight:700;color:#003465;">Rang</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;margin-bottom:0.5rem;">
                    <span style="display:flex;align-items:center;gap:0.5rem;color:#424750;"><span class="material-symbols-outlined" style="font-size:14px;color:#003465;">ice_skating</span>{ami['pingouins']} Pingouins /h</span>
                    <span style="font-weight:700;color:#003465;">—</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;">
                    <span style="display:flex;align-items:center;gap:0.5rem;color:#424750;"><span class="material-symbols-outlined" style="font-size:14px;color:#003465;">air</span>{ami['mouettes']} Mouettes /h</span>
                    <span style="font-weight:700;color:#003465;">—</span>
                </div>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Suggestions
st.markdown(
    """
    <div style="max-width:40rem;margin:2rem auto;">
    <h2 style="font-family:'Plus Jakarta Sans';font-size:1.5rem;font-weight:700;margin-bottom:1rem;padding:0 0.5rem;">Suggestions Glacées</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

suggestions = [("Erik", "🦭"), ("Moby", "🐋"), ("Balto", "🐺"), ("Glacia", "🧊")]
cols = st.columns(4)
for i, (nom, emoji) in enumerate(suggestions):
    with cols[i]:
        st.markdown(
            f"""
            <div style="background:#fff;padding:1.25rem;border-radius:1rem;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #e4e9ed;">
                <div style="width:64px;height:64px;margin:0 auto 0.75rem;border-radius:50%;background:#f0f9ff;display:flex;align-items:center;justify-content:center;font-size:2rem;">{emoji}</div>
                <div style="font-weight:700;font-size:0.875rem;margin-bottom:1rem;">{nom}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(f"Suivre {nom}", key=f"suivre_{i}")

st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)

# Bottom Nav
st.markdown(
    """
    <div style="position:fixed;bottom:0;left:0;right:0;z-index:999;display:flex;justify-content:space-around;align-items:center;padding:0.75rem 1rem 1.5rem;background:rgba(255,255,255,0.9);backdrop-filter:blur(20px);box-shadow:0 -10px 40px rgba(0,52,101,0.08);border-radius:2.5rem 2.5rem 0 0;border-top:1px solid #e4e9ed;">
        <a href="/" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1rem;text-decoration:none;"><span class="material-symbols-outlined">home</span><span style="font-size:9px;font-weight:700;text-transform:uppercase;">Banquise</span></a>
        <a href="/Amis" style="display:flex;flex-direction:column;align-items:center;color:#003465;padding:0.5rem 1rem;text-decoration:none;"><span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">group</span><span style="font-size:9px;font-weight:700;text-transform:uppercase;">Amis</span></a>
        <a href="#" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1rem;text-decoration:none;"><span class="material-symbols-outlined">notifications</span><span style="font-size:9px;font-weight:700;text-transform:uppercase;">Alertes</span></a>
        <a href="/Profil" style="display:flex;flex-direction:column;align-items:center;color:#64748b;padding:0.5rem 1rem;text-decoration:none;"><span class="material-symbols-outlined">person</span><span style="font-size:9px;font-weight:700;text-transform:uppercase;">Profil</span></a>
    </div>
    """,
    unsafe_allow_html=True,
)
