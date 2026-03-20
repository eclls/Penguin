"""Penguin - Application interactive de suivi de jours."""

import streamlit as st

from utils import (
    add_days,
    authenticate_user,
    breakdown_days,
    emoji_cloud,
    get_user_by_id,
    init_database,
    inject_penguin_css,
    register_user,
    render_mobile_nav,
    set_user_days,
)

st.set_page_config(
    page_title="Penguin",
    page_icon="🐧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_penguin_css()
init_database()


def _init_session() -> None:
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("show_opening_modal", False)


def _logout() -> None:
    st.session_state["user_id"] = None
    st.session_state["show_opening_modal"] = False


def _auth_screen() -> None:
    st.markdown("## 🐧 Penguin")
    st.caption("Compteur de progression interactif : mouettes, pingouins, orques et requins.")
    tab_login, tab_signup = st.tabs(["Connexion", "Creer un compte"])

    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Nom d'utilisateur", key="login_username")
            password = st.text_input("Mot de passe", type="password", key="login_password")
            submit = st.form_submit_button("Se connecter", use_container_width=True, type="primary")
        if submit:
            user = authenticate_user(username, password)
            if user is None:
                st.error("Identifiants invalides.")
            else:
                st.session_state["user_id"] = int(user["id"])
                st.session_state["show_opening_modal"] = True
                st.rerun()

    with tab_signup:
        with st.form("signup_form", clear_on_submit=False):
            username = st.text_input("Nom d'utilisateur", key="signup_username")
            password = st.text_input("Mot de passe", type="password", key="signup_password")
            confirm_password = st.text_input(
                "Confirmer le mot de passe",
                type="password",
                key="signup_password_confirm",
            )
            starting_days = st.number_input(
                "Ajouter un nombre de jours (initialisation)",
                min_value=0,
                value=0,
                step=1,
            )
            submit = st.form_submit_button("Creer le compte", use_container_width=True)
        if submit:
            if password != confirm_password:
                st.error("Les deux mots de passe ne correspondent pas.")
                return
            ok, message = register_user(username, password, int(starting_days))
            if not ok:
                st.error(message)
                return
            user = authenticate_user(username, password)
            if user is None:
                st.error("Le compte a ete cree mais la connexion a echoue.")
                return
            st.session_state["user_id"] = int(user["id"])
            st.session_state["show_opening_modal"] = True
            st.success(message)
            st.rerun()


def _opening_modal(user_id: int) -> None:
    @st.dialog("Tu as tue le pinguin ? Secoue toi")
    def _dialog() -> None:
        st.write(
            "A chaque ouverture, tu choisis soit de reset ta progression, soit de continuer."
        )
        st.info(
            "Sur mobile, secoue ton telephone puis clique sur le bouton de reset pour confirmer."
        )
        if st.button("📳 J'ai secoue: reset", type="primary", use_container_width=True):
            set_user_days(user_id, 0)
            st.session_state["show_opening_modal"] = False
            st.success("Compteur remis a zero.")
            st.rerun()
        if st.button("Continuer sans reset", use_container_width=True):
            st.session_state["show_opening_modal"] = False
            st.rerun()

    _dialog()


def _render_banquise(days: int) -> None:
    fauna = breakdown_days(days)
    st.markdown(
        f"""
        <div class="penguin-hero">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">
                <div>
                    <div class="penguin-title" style="font-size:2rem;">Penguin 🐧</div>
                    <div class="penguin-muted">Banquise de progression</div>
                </div>
                <div style="font-size:2rem;font-weight:800;color:#003465;">Jour {days}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    col1.metric("Mouettes", fauna["gulls"], help="1 jour = 1 mouette")
    col2.metric("Pingouins", fauna["penguins"], help="30 mouettes = 1 pingouin")
    col3, col4 = st.columns(2)
    col3.metric("Orques", fauna["orcas"], help="6 pingouins = 1 orque")
    col4.metric("Requins", fauna["sharks"], help="2 orques = 1 requin")

    st.markdown("### Banquise visuelle")
    st.markdown(
        f"""
        <div class="penguin-card">
            <div><strong>Requins</strong>: {emoji_cloud("🦈", fauna["sharks"])}</div>
            <div><strong>Orques</strong>: {emoji_cloud("🐋", fauna["orcas"])}</div>
            <div><strong>Pingouins</strong>: {emoji_cloud("🐧", fauna["penguins"])}</div>
            <div><strong>Mouettes</strong>: {emoji_cloud("🐦", fauna["gulls"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Exemple attendu valide: Jour 256 = 1 orque + 2 pingouins + 16 mouettes."
    )


def _render_controls(user_id: int, current_days: int) -> None:
    st.markdown("### Actions")
    quick1, quick2, quick3 = st.columns(3)
    with quick1:
        if st.button("+1 jour", use_container_width=True, type="primary"):
            add_days(user_id, 1)
            st.rerun()
    with quick2:
        if st.button("+7 jours", use_container_width=True):
            add_days(user_id, 7)
            st.rerun()
    with quick3:
        if st.button("+30 jours", use_container_width=True):
            add_days(user_id, 30)
            st.rerun()

    with st.form("manual_add_form", clear_on_submit=True):
        amount = st.number_input(
            "Ajouter un nombre de jours",
            min_value=0,
            value=0,
            step=1,
            help="Utile si tu avais deja commence avant d'installer l'app.",
        )
        submit = st.form_submit_button("Ajouter", use_container_width=True)
    if submit and int(amount) > 0:
        add_days(user_id, int(amount))
        st.success(f"{int(amount)} jours ajoutes.")
        st.rerun()

    with st.expander("Definir exactement mon compteur (option avancee)"):
        with st.form("set_exact_days_form", clear_on_submit=False):
            exact = st.number_input(
                "Compteur exact",
                min_value=0,
                value=int(current_days),
                step=1,
            )
            submit = st.form_submit_button("Mettre a jour", use_container_width=True)
        if submit:
            set_user_days(user_id, int(exact))
            st.success("Compteur mis a jour.")
            st.rerun()


_init_session()

if st.session_state["user_id"] is None:
    _auth_screen()
    st.stop()

current_user = get_user_by_id(int(st.session_state["user_id"]))
if current_user is None:
    _logout()
    st.error("Session invalide. Reconnecte-toi.")
    st.stop()

if st.session_state.get("show_opening_modal", False):
    _opening_modal(int(current_user["id"]))

st.markdown(
    f"### Salut **{current_user['username']}** ! Voici ta banquise du jour.",
)
_render_banquise(int(current_user["days"]))
_render_controls(int(current_user["id"]), int(current_user["days"]))

if st.button("Se deconnecter", use_container_width=True):
    _logout()
    st.rerun()

render_mobile_nav(active="banquise")
