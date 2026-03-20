"""Profil utilisateur Penguin."""

import streamlit as st

from utils import (
    breakdown_days,
    get_user_by_id,
    inject_penguin_css,
    list_friend_progress,
    render_mobile_nav,
    set_user_days,
)

st.set_page_config(page_title="Penguin - Profil", page_icon="👤", layout="centered")
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
friend_count = len(list_friend_progress(int(user["id"])))

st.markdown(f"## 👤 Profil de {user['username']}")
col1, col2 = st.columns(2)
col1.metric("Jour actuel", days)
col2.metric("Amis", friend_count)
st.metric("Progression requins", fauna["sharks"])

st.markdown("### Ajustement manuel")
with st.form("profile_adjust_days"):
    new_days = st.number_input(
        "Ajouter un nombre de jours de depart / correction",
        min_value=0,
        value=days,
        step=1,
    )
    submit = st.form_submit_button("Sauvegarder", type="primary", use_container_width=True)
if submit:
    set_user_days(int(user["id"]), int(new_days))
    st.success("Compteur mis a jour.")
    st.rerun()

st.markdown("### Resume conversion")
st.write(
    f"- {fauna['sharks']} requin(s)\n"
    f"- {fauna['orcas']} orque(s)\n"
    f"- {fauna['penguins']} pingouin(s)\n"
    f"- {fauna['gulls']} mouette(s)"
)

if st.button("🚪 Se deconnecter", use_container_width=True):
    st.session_state["user_id"] = None
    st.session_state["show_opening_modal"] = False
    st.rerun()

render_mobile_nav(active="profil")
