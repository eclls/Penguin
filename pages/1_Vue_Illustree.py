"""Vue illustree de la progression Penguin."""

import streamlit as st

from utils import breakdown_days, emoji_cloud, get_user_by_id, inject_penguin_css, render_mobile_nav

st.set_page_config(
    page_title="Penguin - Vue illustree",
    page_icon="🧊",
    layout="centered",
)
inject_penguin_css()

if st.session_state.get("user_id") is None:
    st.warning("Connecte-toi d'abord sur la page Banquise.")
    st.page_link("app.py", label="Aller a la connexion", icon="🏠")
    st.stop()

user = get_user_by_id(int(st.session_state["user_id"]))
if user is None:
    st.warning("Session invalide. Reconnecte-toi.")
    st.page_link("app.py", label="Retour a l'accueil", icon="🏠")
    st.stop()

days = int(user["days"])
fauna = breakdown_days(days)

st.markdown(f"## 🧊 Vue illustree - Jour {days}")
st.caption("Conversion stricte : 1 jour = 1 mouette, 30 = 1 pingouin, 180 = 1 orque, 360 = 1 requin.")

st.markdown(
    f"""
    <div class="penguin-card">
        <h3 style="margin-top:0;">Banquise de @{user["username"]}</h3>
        <p><strong>Requins :</strong> {emoji_cloud("🦈", fauna["sharks"], max_display=10)}</p>
        <p><strong>Orques :</strong> {emoji_cloud("🐋", fauna["orcas"], max_display=10)}</p>
        <p><strong>Pingouins :</strong> {emoji_cloud("🐧", fauna["penguins"], max_display=20)}</p>
        <p><strong>Mouettes :</strong> {emoji_cloud("🐦", fauna["gulls"], max_display=30)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
col1.metric("Requins", fauna["sharks"])
col2.metric("Orques", fauna["orcas"])
col3, col4 = st.columns(2)
col3.metric("Pingouins", fauna["penguins"])
col4.metric("Mouettes", fauna["gulls"])

st.markdown("### Verification exemple")
example = breakdown_days(256)
st.code(
    f"Jour 256 -> {example['orcas']} orque(s), {example['penguins']} pingouin(s), {example['gulls']} mouette(s)",
    language="text",
)

with st.expander("Profil"):
    st.page_link("pages/2_Profil.py", label="Ouvrir mon profil", icon="👤")

render_mobile_nav(active="vue")
