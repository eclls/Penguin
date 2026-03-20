"""Penguin - version mobile-first mono-fichier pour Streamlit."""

from __future__ import annotations

from datetime import datetime, timedelta
import math
import os
import sqlite3
import traceback
from pathlib import Path
from typing import Any

import extra_streamlit_components as stx
import streamlit as st
import streamlit.components.v1 as components

IOS_ICON_URL = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f427.png"

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
      .penguin-error-card {
        background: rgba(255, 237, 237, 0.96);
        border: 1px solid rgba(186, 26, 26, 0.25);
        border-radius: 0.9rem;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
      }
      .penguin-scene {
        position: relative;
        width: 100%;
        aspect-ratio: 4 / 5;
        border-radius: 1rem;
        overflow: hidden;
        background: linear-gradient(180deg, #9eddff 0%, #dff5ff 45%, #79b6dc 45%, #4b8bb7 100%);
        border: 1px solid rgba(0, 52, 101, 0.2);
      }
      .penguin-ice {
        position: absolute;
        left: 12%;
        right: 12%;
        bottom: 18%;
        height: 33%;
        background: linear-gradient(180deg, #ffffff 0%, #e9f8ff 85%);
        border-radius: 46% 54% 43% 57% / 44% 39% 61% 56%;
        box-shadow: inset 0 -14px 30px rgba(56, 122, 166, 0.12);
        border: 1px solid rgba(0, 52, 101, 0.14);
      }
      .penguin-animal {
        position: absolute;
        transform: translate(-50%, -50%);
        line-height: 1;
        user-select: none;
      }
      .penguin-animal--bird {
        font-size: clamp(14px, 2.1vw, 18px);
        filter: saturate(1.2);
      }
      .penguin-animal--penguin {
        font-size: clamp(18px, 3vw, 28px);
      }
      .penguin-animal--orca {
        font-size: clamp(22px, 4vw, 34px);
      }
      .penguin-animal--shark {
        font-size: clamp(26px, 4.3vw, 38px);
      }
      .penguin-frost {
        position: absolute;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
      }
    </style>
    """,
        unsafe_allow_html=True,
    )


def inject_ios_webapp_meta() -> None:
    """Ajoute des meta tags pour une experience bookmark iOS."""
    html = """
        <script>
        (function() {
          const doc = window.parent.document;
          const head = doc.head;
          function ensureMeta(name, content) {
            let el = head.querySelector(`meta[name="${name}"]`);
            if (!el) {
              el = doc.createElement("meta");
              el.setAttribute("name", name);
              head.appendChild(el);
            }
            el.setAttribute("content", content);
          }
          ensureMeta("apple-mobile-web-app-capable", "yes");
          ensureMeta("apple-mobile-web-app-status-bar-style", "black-translucent");
          ensureMeta("apple-mobile-web-app-title", "Penguin");
          ensureMeta("mobile-web-app-capable", "yes");
          ensureMeta("theme-color", "#003465");
          function ensureLink(rel) {
            let el = head.querySelector(`link[rel="${rel}"]`);
            if (!el) {
              el = doc.createElement("link");
              el.setAttribute("rel", rel);
              head.appendChild(el);
            }
            return el;
          }

          // Force une icone pingouin explicite pour eviter l'icone Streamlit par defaut.
          const iconUrl = "__ICON_URL__";
          const appleIcon = ensureLink("apple-touch-icon");
          appleIcon.setAttribute("sizes", "180x180");
          appleIcon.setAttribute("href", iconUrl);
          ensureLink("icon").setAttribute("href", iconUrl);
          ensureLink("shortcut icon").setAttribute("href", iconUrl);
        })();
        </script>
        """
    components.html(
        html.replace("__ICON_URL__", IOS_ICON_URL),
        height=0,
        width=0,
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


class SessionCookieFallback:
    """Fallback si le composant cookies n'est pas disponible."""

    def get(self, name: str) -> str | None:
        return st.session_state.get(f"_fallback_cookie_{name}")

    def set(self, name: str, value: str, expires_at: datetime | None = None) -> None:
        _ = expires_at  # Signature compatible avec CookieManager.
        st.session_state[f"_fallback_cookie_{name}"] = value

    def delete(self, name: str) -> None:
        st.session_state.pop(f"_fallback_cookie_{name}", None)


def get_cookie_manager() -> Any:
    # Ne pas cacher cette fonction: les composants Streamlit sont interdits en cache.
    try:
        return stx.CookieManager()
    except Exception:
        set_persistent_error(
            "Le module de memorisation locale a eu un souci. L'app utilise un mode de secours pour cette session."
        )
        return SessionCookieFallback()


def safe_cookie_get(cookie_manager: Any, name: str) -> str | None:
    try:
        value = cookie_manager.get(name)
        return value if value else None
    except Exception:
        return None


def safe_cookie_set(
    cookie_manager: Any,
    name: str,
    value: str,
    expires_at: datetime | None = None,
) -> None:
    try:
        cookie_manager.set(name, value, expires_at=expires_at)
    except Exception as exc:
        set_persistent_error(
            "Impossible d'enregistrer le pseudo localement sur cet appareil.",
            details=str(exc),
        )


def safe_cookie_delete(cookie_manager: Any, name: str) -> None:
    try:
        # Certains gestionnaires levent KeyError si le cookie n'existe pas.
        if safe_cookie_get(cookie_manager, name) is None:
            return
        cookie_manager.delete(name)
    except KeyError:
        return
    except Exception as exc:
        set_persistent_error(
            "Impossible de supprimer le pseudo memorise.",
            details=str(exc),
        )


def render_ios_bookmark_help() -> None:
    """Affiche une aide simple pour ajouter l'app en bookmark iOS."""
    with st.expander("📱 Installer sur iPhone (bookmark ecran d'accueil)"):
        st.markdown(
            """
1. Ouvre l'app dans **Safari**.
2. Appuie sur **Partager** (carré avec flèche vers le haut).
3. Choisis **Sur l'ecran d'accueil**.
4. Valide **Ajouter**.

Ensuite l'app se lance en mode web-app plein ecran, comme une mini application.
Si l'ancienne icone Streamlit reste visible, supprime d'abord l'ancien raccourci puis recree-le.
"""
        )


def _position(seed: int, idx: int, x_min: float, x_max: float, y_min: float, y_max: float) -> tuple[float, float]:
    """Genere une position stable pour placer un animal."""
    x_span = x_max - x_min
    y_span = y_max - y_min
    # Formule deterministe: meme compte => meme scene.
    t1 = (seed * 97 + idx * 37 + idx * idx * 11) % 1000
    t2 = (seed * 53 + idx * 73 + idx * idx * 7) % 1000
    x = x_min + (t1 / 1000.0) * x_span
    y = y_min + (t2 / 1000.0) * y_span
    return x, y


def _animals_html(
    emoji: str,
    count: int,
    css_class: str,
    seed: int,
    zone: tuple[float, float, float, float],
    max_display: int,
) -> tuple[str, int]:
    """Construit le HTML des animaux et retourne le nombre masque."""
    x_min, x_max, y_min, y_max = zone
    shown = min(max(count, 0), max_display)
    parts: list[str] = []
    for i in range(shown):
        x, y = _position(seed, i, x_min, x_max, y_min, y_max)
        wobble = math.sin((seed + i) / 8.0) * 1.5
        parts.append(
            (
                f'<span class="penguin-animal {css_class}" '
                f'style="left:{x:.2f}%; top:{(y + wobble):.2f}%;">{emoji}</span>'
            )
        )
    hidden = max(count - shown, 0)
    return "".join(parts), hidden


def render_banquise_scene(user_id: int, fauna: dict[str, int]) -> None:
    """Rendu illustre de la banquise avec les bons animaux."""
    birds_html, birds_hidden = _animals_html(
        "🐦",
        fauna["gulls"],
        "penguin-animal--bird",
        user_id + 11,
        (8, 92, 8, 39),
        max_display=90,
    )
    penguins_html, penguins_hidden = _animals_html(
        "🐧",
        fauna["penguins"],
        "penguin-animal--penguin",
        user_id + 29,
        (20, 80, 53, 77),
        max_display=70,
    )
    orcas_html, orcas_hidden = _animals_html(
        "🐋",
        fauna["orcas"],
        "penguin-animal--orca",
        user_id + 43,
        (10, 90, 70, 92),
        max_display=18,
    )
    sharks_html, sharks_hidden = _animals_html(
        "🦈",
        fauna["sharks"],
        "penguin-animal--shark",
        user_id + 67,
        (12, 88, 78, 96),
        max_display=14,
    )

    frost = []
    for i in range(14):
        x, y = _position(user_id + 101, i, 4, 96, 6, 42)
        frost.append(f'<span class="penguin-frost" style="left:{x:.2f}%; top:{y:.2f}%;"></span>')

    st.markdown(
        f"""
        <div class="penguin-scene">
          {"".join(frost)}
          <div class="penguin-ice"></div>
          {birds_html}
          {penguins_html}
          {orcas_html}
          {sharks_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    chips = []
    if birds_hidden:
        chips.append(f"🐦 +{birds_hidden}")
    if penguins_hidden:
        chips.append(f"🐧 +{penguins_hidden}")
    if orcas_hidden:
        chips.append(f"🐋 +{orcas_hidden}")
    if sharks_hidden:
        chips.append(f"🦈 +{sharks_hidden}")
    if chips:
        st.caption("Animaux supplementaires hors ecran pour garder une vue lisible : " + " • ".join(chips))


def init_session() -> None:
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("show_reset_modal", False)
    st.session_state.setdefault("tab", "Banquise")
    st.session_state.setdefault("persistent_error", None)


def logout() -> None:
    st.session_state["user_id"] = None
    st.session_state["show_reset_modal"] = False


def set_persistent_error(message: str, details: str | None = None) -> None:
    st.session_state["persistent_error"] = {
        "message": message,
        "details": details or "",
    }


def render_persistent_error() -> None:
    error_data = st.session_state.get("persistent_error")
    if not error_data:
        return
    st.markdown('<div class="penguin-error-card">', unsafe_allow_html=True)
    st.error(error_data.get("message", "Une erreur est survenue."))
    details = error_data.get("details", "").strip()
    if details:
        with st.expander("Details techniques"):
            st.code(details, language="text")
    if st.button("Fermer le message d'erreur", use_container_width=True):
        st.session_state["persistent_error"] = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def auth_screen(cookie_manager: Any) -> None:
    st.markdown("## 🐧 Penguin")
    st.caption(
        "Version locale de confiance: choisis ton pseudo, et l'app garde ton compte + tes jours en memoire."
    )
    remembered = safe_cookie_get(cookie_manager, COOKIE_NAME)
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
        safe_cookie_set(
            cookie_manager,
            COOKIE_NAME,
            str(user["username"]),
            expires_at=datetime.now() + timedelta(days=365),
        )
    else:
        safe_cookie_delete(cookie_manager, COOKIE_NAME)

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


def render_vue(user: dict[str, Any]) -> None:
    days = int(user["days"])
    fauna = breakdown_days(days)
    st.markdown(f"## 🧊 Vue illustree - Jour {days}")
    st.caption("La scene ci-dessous affiche la banquise avec les bons animaux selon ton compteur.")
    render_banquise_scene(int(user["id"]), fauna)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Mouettes", fauna["gulls"])
        st.metric("Orques", fauna["orcas"])
    with c2:
        st.metric("Pingouins", fauna["penguins"])
        st.metric("Requins", fauna["sharks"])

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


def render_profil(user: dict[str, Any], cookie_manager: Any) -> None:
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
            safe_cookie_delete(cookie_manager, COOKIE_NAME)
            logout()
            st.rerun()


def run_app() -> None:
    inject_css()
    inject_ios_webapp_meta()
    init_database()
    init_session()
    render_persistent_error()

    try:
        cookie_manager = get_cookie_manager()

        if st.session_state["user_id"] is None:
            remembered = safe_cookie_get(cookie_manager, COOKIE_NAME)
            if remembered:
                remembered_user = get_user_by_username(remembered)
                if remembered_user is not None:
                    st.session_state["user_id"] = int(remembered_user["id"])

        if st.session_state["user_id"] is None:
            auth_screen(cookie_manager)
            render_ios_bookmark_help()
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

        render_ios_bookmark_help()
    except Exception:
        details = traceback.format_exc()
        set_persistent_error(
            "Une erreur est survenue. Le message est conserve ici tant que tu ne le fermes pas.",
            details=details,
        )
        st.error("Erreur capturee et conservee. Ouvre les details ci-dessous.")
        with st.expander("Details techniques"):
            st.code(details, language="text")


if __name__ == "__main__":
    run_app()
