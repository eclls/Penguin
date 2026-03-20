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
    """CSS minimal, sans Tailwind ni dépendances externes."""
    st.markdown(
        """
    <style>
      .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
      .stApp { background: #f6fafe !important; }
      .block-container { max-width: 420px; padding: 1rem; padding-bottom: 6rem; }
      [data-testid="stSidebar"] { display: none; }
      #MainMenu, footer, .stDeployButton { visibility: hidden; }
      .penguin-animal { position: absolute; transform: translate(-50%,-50%); line-height: 1; user-select: none; }
      .penguin-error-card { background: #ffebee; border: 1px solid #ef9a9a; border-radius: 0.5rem; padding: 0.8rem; margin-bottom: 0.8rem; }
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
    symbol: str,
    count: int,
    css_class: str,
    seed: int,
    zone: tuple[float, float, float, float],
    max_display: int,
    size: str = "24px",
) -> tuple[str, int]:
    """Construit le HTML des animaux (Material Symbols) et retourne le nombre masque."""
    x_min, x_max, y_min, y_max = zone
    shown = min(max(count, 0), max_display)
    parts: list[str] = []
    for i in range(shown):
        x, y = _position(seed, i, x_min, x_max, y_min, y_max)
        wobble = math.sin((seed + i) / 8.0) * 1.5
        parts.append(
            f'<span class="penguin-animal {css_class}" '
            f'style="left:{x:.2f}%; top:{(y + wobble):.2f}%; font-size:{size}">'
            f'{symbol}</span>'
        )
    hidden = max(count - shown, 0)
    return "".join(parts), hidden


def render_banquise_scene(user_id: int, fauna: dict[str, int]) -> None:
    """
    Scène banquise : banquise ronde au centre, eau autour. Animaux en emojis Apple.
    J=0 => Dodo...
    """
    days = fauna["days"]

    # Emojis Apple : oiseaux, pingouins, orques, requins
    birds_html, birds_hidden = _animals_html(
        "🐦", fauna["gulls"], "penguin-animal--bird", user_id + 11,
        (8, 92, 5, 35), 90, "22px",
    )
    penguins_html, penguins_hidden = _animals_html(
        "🐧", fauna["penguins"], "penguin-animal--penguin", user_id + 29,
        (30, 70, 50, 82), 70, "26px",
    )
    orcas_html, orcas_hidden = _animals_html(
        "🐋", fauna["orcas"], "penguin-animal--orca", user_id + 43,
        (15, 85, 68, 92), 18, "24px",
    )
    sharks_html, sharks_hidden = _animals_html(
        "🦈", fauna["sharks"], "penguin-animal--shark", user_id + 67,
        (12, 88, 75, 95), 14, "22px",
    )

    if days == 0:
        inner = '<div style="position:absolute;left:50%;top:60%;transform:translate(-50%,-50%);text-align:center;opacity:0.6"><span style="font-size:48px">🐧</span><div style="font-size:11px;font-weight:700;color:#555">Dodo...</div></div>'
    else:
        inner = f'<div style="position:absolute;inset:0">{birds_html}{penguins_html}{orcas_html}{sharks_html}</div>'

    st.markdown(
        f"""
        <div style="position:relative;width:100%;height:240px;border-radius:12px;overflow:hidden;margin:1rem 0;border:1px solid #c8dce8">
          <div style="position:absolute;inset:0;background:linear-gradient(180deg,#9eddff 0%,#dff5ff 40%,#5a9bb8 40%,#2d6a82 100%)"></div>
          <div style="position:absolute;left:50%;top:55%;transform:translate(-50%,-50%);width:55%;height:45%;background:linear-gradient(180deg,#fff 0%,#e8f4fa 80%);border-radius:50%;box-shadow:inset 0 -8px 20px rgba(100,150,180,0.15);border:1px solid rgba(255,255,255,0.9)"></div>
          {inner}
        </div>
        """,
        unsafe_allow_html=True,
    )

    chips = []
    if birds_hidden:
        chips.append(f"Mouettes +{birds_hidden}")
    if penguins_hidden:
        chips.append(f"Pingouins +{penguins_hidden}")
    if orcas_hidden:
        chips.append(f"Orques +{orcas_hidden}")
    if sharks_hidden:
        chips.append(f"Requins +{sharks_hidden}")
    if chips:
        st.caption("Hors écran : " + " • ".join(chips))


def init_session() -> None:
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("tab", "Banquise")
    st.session_state.setdefault("persistent_error", None)


def logout() -> None:
    st.session_state["user_id"] = None


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
    st.rerun()


def render_banquise(user: dict[str, Any]) -> None:
    """Vue Banquise : layout simple et fonctionnel."""
    days = int(user["days"])
    fauna = breakdown_days(days)

    # Header simple : titre + Jour
    st.markdown(f"## 🐧 Penguin — Jour {days}")
    st.caption(f"Salut {user['username']} 👋")

    # Stats : Streamlit natif
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mouettes", fauna["gulls"])
    c2.metric("Pingouins", fauna["penguins"])
    c3.metric("Orques", fauna["orcas"])
    c4.metric("Requins", fauna["sharks"])

    # Scène banquise
    render_banquise_scene(int(user["id"]), fauna)

    # Bento : Streamlit natif
    b1, b2 = st.columns(2)
    with b1:
        st.info("🌊 Océan — -2°C Arctique")
    with b2:
        st.warning("⚠️ Danger — Requin & Orque")

    # Bouton fusil : tue les pingouins = compteur à 0
    if st.button("🔫 Tuer les pingouins (remise à zéro)", type="secondary", use_container_width=True):
        set_user_days(int(user["id"]), 0)
        st.rerun()


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
            st.stop()

        current_user = get_user_by_id(int(st.session_state["user_id"]))
        if current_user is None:
            logout()
            st.error("Session invalide. Reconnecte-toi.")
            st.stop()

        tab = st.session_state.get("tab", "Banquise")

        if tab == "Banquise":
            render_banquise(current_user)
        elif tab == "Amis":
            render_amis(current_user)
        else:
            render_profil(current_user, cookie_manager)

        st.divider()
        nc1, nc2, nc3 = st.columns(3)
        with nc1:
            if st.button("🏠 Banquise", type="primary" if tab == "Banquise" else "secondary", use_container_width=True, key="nav_banquise"):
                st.session_state["tab"] = "Banquise"
                st.rerun()
        with nc2:
            if st.button("👥 Amis", type="primary" if tab == "Amis" else "secondary", use_container_width=True, key="nav_amis"):
                st.session_state["tab"] = "Amis"
                st.rerun()
        with nc3:
            if st.button("👤 Profil", type="primary" if tab == "Profil" else "secondary", use_container_width=True, key="nav_profil"):
                st.session_state["tab"] = "Profil"
                st.rerun()
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
