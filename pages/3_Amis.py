"""Page sociale Penguin : ajout d'amis et progression."""

import streamlit as st

from utils import (
    add_friend_by_username,
    breakdown_days,
    get_user_by_id,
    inject_penguin_css,
    list_discoverable_users,
    list_friend_progress,
)

st.set_page_config(page_title="Penguin - Amis", page_icon="👥", layout="wide")
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

st.markdown("## 👥 Amis")
st.caption("Ajoute des amis par pseudo et compare votre progression.")

with st.form("add_friend_form"):
    friend_username = st.text_input("Pseudo de ton ami")
    submit_add = st.form_submit_button("Ajouter un ami", type="primary", use_container_width=True)
if submit_add:
    ok, message = add_friend_by_username(int(user["id"]), friend_username)
    if ok:
        st.success(message)
    else:
        st.error(message)

friends = list_friend_progress(int(user["id"]))
st.metric("Nombre d'amis", len(friends))

if not friends:
    st.info("Aucun ami pour l'instant.")
else:
    st.markdown("### Progression de mes amis")
    for friend in friends:
        fauna = breakdown_days(int(friend["days"]))
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.write(f"**{friend['username']}**")
            c2.metric("Jour", int(friend["days"]))
            c3.metric("Orques", fauna["orcas"])
            c4.metric("Requins", fauna["sharks"])

discoverable = list_discoverable_users(int(user["id"]), limit=8)
if discoverable:
    st.markdown("### Suggestions")
    cols = st.columns(2)
    for idx, candidate in enumerate(discoverable):
        with cols[idx % 2]:
            with st.container(border=True):
                st.write(f"**{candidate['username']}**")
                st.caption(f"Jour {candidate['days']}")
                if st.button("Ajouter", key=f"add_{candidate['id']}"):
                    ok, message = add_friend_by_username(int(user["id"]), candidate["username"])
                    if ok:
                        st.success(f"{candidate['username']} ajoute.")
                    else:
                        st.warning(message)
                    st.rerun()

nav1, nav2, nav3 = st.columns(3)
with nav1:
    st.page_link("app.py", label="Banquise", icon="🏠")
with nav2:
    st.page_link("pages/1_Vue_Illustree.py", label="Vue Illustree", icon="🧊")
with nav3:
    st.page_link("pages/2_Profil.py", label="Profil", icon="👤")
