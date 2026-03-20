"""Penguin - version mobile-first mono-fichier pour Streamlit."""

from __future__ import annotations

from datetime import datetime, timedelta
import os
import sqlite3
from pathlib import Path
from typing import Any

import extra_streamlit_components as stx
import streamlit as st

st.set_page_config(
    page_title="Penguin",
    page_icon="🐧",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def inject_css() -> None:
    st.markdown(
        """
    <style>
      .stApp {
        background: linear-gradient(180deg, #bde8ff 0%, #eaf7ff 35%, #f6fafe 100%) !important;
      }
      .block-container {
        max-width: 560px;
        padding-top: 0.9rem;
        padding-bottom: 2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
      }
      [data-testid="stSidebar"] { display: none; }
      #MainMenu, footer, .stDeployButton { visibility: hidden; }
      .stButton > button, .stFormSubmitButton > button {
        min-height: 46px;
        border-radius: 14px;
        font-weight: 700;
      }
      .penguin-card {
        background: rgba(255, 255, 255, 0.92);
        border-radius: 1rem;
        border: 1px solid rgba(0, 52, 101, 0.1);
        padding: 1rem;
        box-shadow: 0 8px 30px rgba(0, 52, 101, 0.08);
      }
    </style>
    """,
        unsafe_allow_html=True,
    )


def _db_path() -> Path:
    db_path_raw = os.getenv("PENGUIN_DB_PATH", "data/penguin.db").strip() or "data/penguin.db"
    db_path = Path(db_path_raw)
    if not db_path.is_absolute():
        db_path = Path.cwd() / db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_database() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE COLLATE NOCASE,
              password_hash TEXT NOT NULL,
              days INTEGER NOT NULL DEFAULT 0 CHECK(days >= 0),
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS friendships (
              user_id INTEGER NOT NULL,
              friend_id INTEGER NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (user_id, friend_id),
              FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
              FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE,
              CHECK(user_id != friend_id)
            );
            """
        )


def register_user(username: str, starting_days: int = 0) -> tuple[bool, str]:
    clean_username = username.strip()
    if len(clean_username) < 3:
        return False, "Le nom d'utilisateur doit contenir au moins 3 caracteres."
    if starting_days < 0:
        return False, "Le nombre de jours ne peut pas etre negatif."

    try:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, days) VALUES (?, ?, ?)",
                (clean_username, "local-trust-no-password", int(starting_days)),
            )
    except sqlite3.IntegrityError:
        return False, "Ce nom d'utilisateur existe deja."
    return True, "Compte cree avec succes."


def authenticate_user(username: str) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
    if row is None:
        return None
    return dict(row)


def get_user_by_username(username: str) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
    return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
    return dict(row) if row else None


def set_user_days(user_id: int, days: int) -> None:
    with _connect() as conn:
        conn.execute("UPDATE users SET days = ? WHERE id = ?", (max(0, int(days)), int(user_id)))


def add_days(user_id: int, delta: int) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET days = MAX(0, days + ?) WHERE id = ?",
            (int(delta), int(user_id)),
        )


def breakdown_days(days: int) -> dict[str, int]:
    total = max(0, int(days))
    sharks = total // 360
    remaining = total % 360
    orcas = remaining // 180
    remaining %= 180
    penguins = remaining // 30
    gulls = remaining % 30
    return {
        "days": total,
        "sharks": sharks,
        "orcas": orcas,
        "penguins": penguins,
        "gulls": gulls,
    }


def add_friend_by_username(user_id: int, friend_username: str) -> tuple[bool, str]:
    clean_username = friend_username.strip()
    if not clean_username:
        return False, "Entre un nom d'utilisateur."

    with _connect() as conn:
        target = conn.execute(
            "SELECT id FROM users WHERE username = ? COLLATE NOCASE",
            (clean_username,),
        ).fetchone()
        if target is None:
            return False, "Utilisateur introuvable."
        friend_id = int(target["id"])
        if friend_id == int(user_id):
            return False, "Tu ne peux pas t'ajouter toi-meme."
        existing = conn.execute(
            "SELECT 1 FROM friendships WHERE user_id = ? AND friend_id = ?",
            (int(user_id), friend_id),
        ).fetchone()
        if existing:
            return False, "Cet utilisateur est deja dans tes amis."

        conn.execute("INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)", (int(user_id), friend_id))
        conn.execute("INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)", (friend_id, int(user_id)))
    return True, "Ami ajoute."


def list_friend_progress(user_id: int) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT u.id, u.username, u.days
            FROM friendships f
            JOIN users u ON u.id = f.friend_id
            WHERE f.user_id = ?
            ORDER BY u.days DESC, u.username ASC
            """,
            (int(user_id),),
        ).fetchall()
    return [dict(row) for row in rows]


def list_discoverable_users(user_id: int, limit: int = 8) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT u.id, u.username, u.days
            FROM users u
            WHERE u.id != ?
              AND u.id NOT IN (
                SELECT friend_id FROM friendships WHERE user_id = ?
              )
            ORDER BY u.created_at DESC
            LIMIT ?
            """,
            (int(user_id), int(user_id), int(limit)),
        ).fetchall()
    return [dict(row) for row in rows]


def emoji_cloud(emoji: str, count: int, max_display: int = 20) -> str:
    safe_count = max(0, int(count))
    if safe_count == 0:
        return "—"
    displayed = min(safe_count, max_display)
    cloud = " ".join([emoji] * displayed)
    if safe_count > max_display:
        cloud += f"  +{safe_count - max_display}"
    return cloud


COOKIE_NAME = "penguin_username"


@st.cache_resource
def get_cookie_manager() -> stx.CookieManager:
    return stx.CookieManager()


def init_session() -> None:
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("show_reset_modal", False)
    st.session_state.setdefault("tab", "Banquise")


def logout() -> None:
    st.session_state["user_id"] = None
    st.session_state["show_reset_modal"] = False


def auth_screen(cookie_manager: stx.CookieManager) -> None:
    st.markdown("## 🐧 Penguin")
    st.caption(
        "Version locale de confiance: choisis ton pseudo, et l'app garde ton compte + tes jours en memoire."
    )
    remembered = cookie_manager.get(COOKIE_NAME)
    if remembered:
        st.info(f"Pseudo memorise sur cet appareil: **{remembered}**")

    with st.form("choose_username_form", clear_on_submit=False):
        username = st.text_input("Choisir mon pseudo")
        starting_days = st.number_input(
            "Jours de depart (si nouveau pseudo)",
            min_value=0,
            value=0,
            step=1,
            help="Utilise uniquement si ce pseudo n'existe pas encore.",
        )
        remember_me = st.checkbox("Se souvenir de mon pseudo sur cet appareil", value=True)
        submit = st.form_submit_button("Continuer", use_container_width=True, type="primary")

    if not submit:
        return

    clean_username = username.strip()
    if len(clean_username) < 3:
        st.error("Le pseudo doit contenir au moins 3 caracteres.")
        return

    user = get_user_by_username(clean_username)
    if user is None:
        ok, message = register_user(clean_username, int(starting_days))
        if not ok:
            st.error(message)
            return
        st.success(message)
        user = get_user_by_username(clean_username)

    if user is None:
        st.error("Impossible de charger le compte.")
        return

    if remember_me:
        cookie_manager.set(
            COOKIE_NAME,
            str(user["username"]),
            expires_at=datetime.now() + timedelta(days=365),
        )
    else:
        cookie_manager.delete(COOKIE_NAME)

    st.session_state["user_id"] = int(user["id"])
    st.session_state["show_reset_modal"] = False
    st.rerun()


def opening_modal(user_id: int) -> None:
    @st.dialog("Tu as tue le pinguin ? Secoue toi")
    def _dialog() -> None:
        st.write("Action A: reset apres secousse. Action B: annuler.")
        st.info("Sur smartphone, secoue puis confirme avec le bouton reset.")
        if st.button("📳 J'ai secoue: reset", type="primary", use_container_width=True):
            set_user_days(user_id, 0)
            st.session_state["show_reset_modal"] = False
            st.success("Compteur remis a zero.")
            st.rerun()
        if st.button("Annuler", use_container_width=True):
            st.session_state["show_reset_modal"] = False
            st.rerun()

    _dialog()


def render_banquise(user: dict[str, Any]) -> None:
    days = int(user["days"])
    fauna = breakdown_days(days)
    st.markdown(f"## Jour {days}")
    st.caption(f"Salut {user['username']} 👋")

    c1, c2 = st.columns(2)
    c1.metric("Mouettes", fauna["gulls"])
    c2.metric("Pingouins", fauna["penguins"])
    c3, c4 = st.columns(2)
    c3.metric("Orques", fauna["orcas"])
    c4.metric("Requins", fauna["sharks"])

    st.markdown(
        f"""
        <div class="penguin-card">
          <div><strong>🦈 Requins:</strong> {emoji_cloud("🦈", fauna["sharks"])}</div>
          <div><strong>🐋 Orques:</strong> {emoji_cloud("🐋", fauna["orcas"])}</div>
          <div><strong>🐧 Pingouins:</strong> {emoji_cloud("🐧", fauna["penguins"])}</div>
          <div><strong>🐦 Mouettes:</strong> {emoji_cloud("🐦", fauna["gulls"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Exemple valide: Jour 256 = 1 orque + 2 pingouins + 16 mouettes.")

    st.markdown("### Actions")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("+1", use_container_width=True, type="primary"):
            add_days(int(user["id"]), 1)
            st.rerun()
    with q2:
        if st.button("+7", use_container_width=True):
            add_days(int(user["id"]), 7)
            st.rerun()
    with q3:
        if st.button("+30", use_container_width=True):
            add_days(int(user["id"]), 30)
            st.rerun()

    with st.form("manual_add"):
        amount = st.number_input("Ajouter un nombre de jours", min_value=0, value=0, step=1)
        submit = st.form_submit_button("Ajouter", use_container_width=True)
    if submit and int(amount) > 0:
        add_days(int(user["id"]), int(amount))
        st.rerun()


def render_vue(user: dict[str, Any]) -> None:
    days = int(user["days"])
    fauna = breakdown_days(days)
    st.markdown(f"## 🧊 Vue illustree - Jour {days}")
    st.markdown(
        f"""
        <div class="penguin-card">
            <p><strong>Requins :</strong> {emoji_cloud("🦈", fauna["sharks"], 10)}</p>
            <p><strong>Orques :</strong> {emoji_cloud("🐋", fauna["orcas"], 10)}</p>
            <p><strong>Pingouins :</strong> {emoji_cloud("🐧", fauna["penguins"], 20)}</p>
            <p><strong>Mouettes :</strong> {emoji_cloud("🐦", fauna["gulls"], 30)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    ex = breakdown_days(256)
    st.code(
        f"Jour 256 -> {ex['orcas']} orque(s), {ex['penguins']} pingouin(s), {ex['gulls']} mouette(s)",
        language="text",
    )


def render_amis(user: dict[str, Any]) -> None:
    st.markdown("## 👥 Amis")
    with st.form("add_friend"):
        username = st.text_input("Pseudo de ton ami")
        submit = st.form_submit_button("Ajouter un ami", use_container_width=True, type="primary")
    if submit:
        ok, msg = add_friend_by_username(int(user["id"]), username)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

    friends = list_friend_progress(int(user["id"]))
    st.metric("Nombre d'amis", len(friends))
    if not friends:
        st.info("Aucun ami pour l'instant.")
    else:
        for friend in friends:
            fauna = breakdown_days(int(friend["days"]))
            with st.container(border=True):
                st.write(f"**{friend['username']}**")
                c1, c2 = st.columns(2)
                c1.metric("Jour", int(friend["days"]))
                c2.metric("Orques/Requins", f"{fauna['orcas']}/{fauna['sharks']}")

    suggestions = list_discoverable_users(int(user["id"]), limit=6)
    if suggestions:
        st.markdown("### Suggestions")
        for candidate in suggestions:
            with st.container(border=True):
                st.write(f"**{candidate['username']}** - Jour {candidate['days']}")
                if st.button(f"Ajouter {candidate['username']}", key=f"cand_{candidate['id']}"):
                    ok, msg = add_friend_by_username(int(user["id"]), candidate["username"])
                    if ok:
                        st.success(msg)
                    else:
                        st.warning(msg)
                    st.rerun()


def render_profil(user: dict[str, Any], cookie_manager: stx.CookieManager) -> None:
    days = int(user["days"])
    fauna = breakdown_days(days)
    friend_count = len(list_friend_progress(int(user["id"])))
    st.markdown(f"## 👤 Profil de {user['username']}")
    c1, c2 = st.columns(2)
    c1.metric("Jour actuel", days)
    c2.metric("Amis", friend_count)
    st.metric("Progression requins", fauna["sharks"])

    with st.form("set_days"):
        new_days = st.number_input("Definir le compteur exact", min_value=0, value=days, step=1)
        submit = st.form_submit_button("Sauvegarder", use_container_width=True, type="primary")
    if submit:
        set_user_days(int(user["id"]), int(new_days))
        st.success("Compteur mis a jour.")
        st.rerun()

    if st.button("⚠️ Remettre le compteur a zero", use_container_width=True):
        st.session_state["show_reset_modal"] = True
        st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚪 Se deconnecter", use_container_width=True):
            logout()
            st.rerun()
    with c2:
        if st.button("🧹 Oublier ce pseudo", use_container_width=True):
            cookie_manager.delete(COOKIE_NAME)
            logout()
            st.rerun()


def run_app() -> None:
    inject_css()
    init_database()
    init_session()
    cookie_manager = get_cookie_manager()

    if st.session_state["user_id"] is None:
        remembered = cookie_manager.get(COOKIE_NAME)
        if remembered:
            remembered_user = get_user_by_username(remembered)
            if remembered_user is not None:
                st.session_state["user_id"] = int(remembered_user["id"])

    if st.session_state["user_id"] is None:
        auth_screen(cookie_manager)
        st.stop()

    current_user = get_user_by_id(int(st.session_state["user_id"]))
    if current_user is None:
        logout()
        st.error("Session invalide. Reconnecte-toi.")
        st.stop()

    if st.session_state.get("show_reset_modal", False):
        opening_modal(int(current_user["id"]))

    tab = st.radio(
        "Navigation",
        options=["Banquise", "Vue illustree", "Amis", "Profil"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if tab == "Banquise":
        render_banquise(current_user)
    elif tab == "Vue illustree":
        render_vue(current_user)
    elif tab == "Amis":
        render_amis(current_user)
    else:
        render_profil(current_user, cookie_manager)


if __name__ == "__main__":
    run_app()
