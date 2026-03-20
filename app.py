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
    """Inject Tailwind, fonts, Material Symbols et styles fidèles au HTML fourni."""
    st.markdown(
        """
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              "primary": "#003465",
              "primary-container": "#004b8d",
              "secondary": "#326578",
              "background": "#f6fafe",
              "surface-container-low": "#f0f4f8",
              "surface-container-highest": "#dfe3e7",
              "on-surface": "#171c1f",
              "on-surface-variant": "#424750",
              "error": "#ba1a1a",
              "secondary-container": "#b5e7fe"
            },
            fontFamily: { "headline": ["Plus Jakarta Sans"], "body": ["Be Vietnam Pro"] },
            borderRadius: { "DEFAULT": "1rem", "lg": "2rem", "xl": "3rem", "full": "9999px" }
          }
        }
      }
    </script>
    <style>
      .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
      body, .stApp { font-family: 'Be Vietnam Pro', sans-serif; background: #f6fafe !important; }
      .block-container { max-width: 28rem; padding: 0 1.5rem 8rem; padding-top: 6rem; }
      [data-testid="stSidebar"] { display: none; }
      #MainMenu, footer, .stDeployButton { visibility: hidden; }
      .arctic-gradient { background: linear-gradient(135deg, #003465 0%, #004b8d 100%); }
      .snow-glow { box-shadow: 0 24px 48px rgba(0, 52, 101, 0.06); }
      .glass-panel { background: rgba(255,255,255,0.85); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); }
      .penguin-animal { position: absolute; transform: translate(-50%,-50%); line-height: 1; user-select: none; }
      .penguin-animal--bird .material-symbols-outlined { color: #326578; }
      .penguin-animal--penguin .material-symbols-outlined { color: #003465; }
      .penguin-animal--orca .material-symbols-outlined { color: #1e3a5f; }
      .penguin-animal--shark .material-symbols-outlined { color: #ba1a1a; }
      .penguin-error-card { background: rgba(255,237,237,0.96); border: 1px solid rgba(186,26,26,0.25); border-radius: 0.9rem; padding: 0.8rem; margin-bottom: 0.8rem; }
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
            f'<span class="ms material-symbols-outlined">{symbol}</span></span>'
        )
    hidden = max(count - shown, 0)
    return "".join(parts), hidden


def render_banquise_scene(user_id: int, fauna: dict[str, int]) -> None:
    """
    Layout inspiré de l'illustration banquise : glace à gauche, océan à droite.
    Animaux dynamiques selon J : oiseaux (ciel), pingouins (glace), orques/requins (eau).
    J=0 => banquise vide (Dodo...).
    """
    days = fauna["days"]

    # Zones inspirées de l'illustration : oiseaux dans le ciel, pingouins sur la glace, orques/requins dans l'eau
    birds_html, birds_hidden = _animals_html(
        "flutter_dash",
        fauna["gulls"],
        "penguin-animal--bird",
        user_id + 11,
        (15, 85, 5, 28),  # ciel : large, haut
        max_display=90,
        size="26px",
    )
    penguins_html, penguins_hidden = _animals_html(
        "ice_skating",
        fauna["penguins"],
        "penguin-animal--penguin",
        user_id + 29,
        (8, 42, 45, 88),  # glace gauche : zone gauche, milieu-bas
        max_display=70,
        size="30px",
    )
    orcas_html, orcas_hidden = _animals_html(
        "water_ec",
        fauna["orcas"],
        "penguin-animal--orca",
        user_id + 43,
        (55, 92, 45, 82),  # eau droite : surface
        max_display=18,
        size="28px",
    )
    sharks_html, sharks_hidden = _animals_html(
        "sailing",
        fauna["sharks"],
        "penguin-animal--shark",
        user_id + 67,
        (58, 95, 72, 95),  # eau droite : plus bas
        max_display=14,
        size="26px",
    )

    if days == 0:
        inner = """
        <div style="position:absolute;left:15%;top:55%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;opacity:0.5;filter:grayscale(1)">
          <span class="material-symbols-outlined" style="font-size:56px;color:#003465">ice_skating</span>
          <span style="font-size:12px;font-weight:700;margin-top:6px;color:#424750">Dodo...</span>
        </div>
        """
    else:
        inner = f"""
        <div style="position:absolute;inset:0;pointer-events:none">
          {birds_html}
          {penguins_html}
          {orcas_html}
          {sharks_html}
        </div>
        """

    st.markdown(
        f"""
        <div class="penguin-scene-landscape" style="position:relative;width:100%;max-width:28rem;aspect-ratio:4/3;border-radius:1rem;overflow:hidden;margin-bottom:2rem;box-shadow:0 12px 40px rgba(0,52,101,0.15)">
          <!-- Ciel -->
          <div style="position:absolute;inset:0 0 60% 0;background:linear-gradient(180deg,#b8d4e8 0%,#d4e8f5 50%,#e8f2f8 100%)"></div>
          <!-- Montagnes lointaines -->
          <div style="position:absolute;bottom:25%;left:0;right:0;height:35%;background:linear-gradient(180deg,transparent 0%,rgba(200,220,235,0.6) 40%,rgba(180,200,215,0.5) 100%);clip-path:polygon(0 100%,0 60%,15% 75%,30% 55%,45% 70%,60% 50%,75% 65%,90% 55%,100% 70%,100% 100%)"></div>
          <!-- Banquise (gauche) : glace blanche/bleutée, bord irrégulier -->
          <div style="position:absolute;left:0;bottom:0;width:52%;height:55%;background:linear-gradient(180deg,#f0f8ff 0%,#e4f2fa 30%,#d4e8f2 70%,#c8e0ee 100%);clip-path:polygon(0 100%,0 25%,8% 15%,18% 22%,28% 12%,38% 18%,48% 8%,52% 15%,52% 100%);border-right:2px solid rgba(255,255,255,0.8);box-shadow:inset 0 -8px 20px rgba(150,180,200,0.2)"></div>
          <!-- Océan (droite) : bleu-vert profond -->
          <div style="position:absolute;right:0;bottom:0;width:52%;height:55%;background:linear-gradient(180deg,#5a9bb8 0%,#3d7a96 40%,#2a5f78 100%);box-shadow:inset 0 4px 20px rgba(0,0,0,0.15)"></div>
          <!-- Petits blocs de glace flottants -->
          <div style="position:absolute;right:8%;bottom:35%;width:12%;height:8%;background:rgba(255,255,255,0.7);border-radius:30% 70% 50% 50%;opacity:0.9"></div>
          <div style="position:absolute;right:25%;bottom:28%;width:8%;height:6%;background:rgba(255,255,255,0.6);border-radius:60% 40% 50% 50%;opacity:0.8"></div>
          <!-- Animaux dynamiques -->
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
        st.caption("Animaux supplementaires hors ecran : " + " • ".join(chips))


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


def render_reset_modal_overlay() -> None:
    """
    Pop-up ludique (Glass Overlay) - fidèle au HTML.
    Shake detection : quand l'utilisateur secoue le téléphone, déclenche la réinitialisation.
    Clic à côté / Annuler = pas de reset.
    """
    st.markdown(
        """
        <div id="penguin-reset-overlay" style="position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:1.5rem;background:rgba(0,52,101,0.3);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)">
          <div onclick="event.stopPropagation()" style="background:rgba(255,255,255,0.85);backdrop-filter:blur(24px);border-radius:0.75rem;padding:2rem;max-width:20rem;width:100%;box-shadow:0 32px 64px rgba(0,52,101,0.2);border:1px solid rgba(255,255,255,0.8);text-align:center">
            <div style="width:96px;height:96px;margin:0 auto 1.5rem;background:linear-gradient(135deg,#003465 0%,#004b8d 100%);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 24px 48px rgba(0,52,101,0.2)">
              <span class="material-symbols-outlined" style="font-size:48px;color:white">ice_skating</span>
            </div>
            <h2 style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:1.5rem;color:#003465;margin-bottom:0.75rem">Tu as tué le pinguin ?</h2>
            <p style="color:#424750;margin-bottom:2rem;line-height:1.5">Secoue toi pour le ramener sur sa banquise !</p>
            <a href="?reset_confirm=1" id="penguin-reset-btn" style="display:flex;align-items:center;justify-content:center;gap:0.75rem;width:100%;padding:1rem 1.5rem;background:linear-gradient(135deg,#003465 0%,#004b8d 100%);color:white;font-weight:700;border-radius:9999px;text-decoration:none;border:1px solid rgba(255,255,255,0.2);box-shadow:0 10px 20px rgba(0,52,101,0.3)">
              <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">vibration</span>
              Réinitialiser (Secouer)
            </a>
            <a href="?cancel=1" style="display:block;margin-top:1rem;color:#424750;font-size:0.875rem;text-decoration:none">Annuler</a>
          </div>
        </div>
        <script>
        (function(){
          var overlay = document.getElementById('penguin-reset-overlay');
          var path = window.location.pathname || '/';

          if (window.DeviceMotionEvent) {
            var lastShake = 0;
            window.addEventListener('devicemotion', function(e) {
              var a = e.accelerationIncludingGravity;
              var total = Math.abs(a.x||0) + Math.abs(a.y||0) + Math.abs(a.z||0);
              if (total > 25 && Date.now() - lastShake > 1500) {
                lastShake = Date.now();
                window.location.href = path + '?reset_confirm=1';
              }
            }, true);
          }

          overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
              window.location.href = path + '?cancel=1';
            }
          });
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )


def render_header(user: dict[str, Any]) -> None:
    """TopAppBar fidèle au HTML : logo, Jour X, avatar."""
    days = int(user["days"])
    st.markdown(
        f"""
        <header class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-xl shadow-[0px_24px_48px_rgba(0,52,101,0.06)]">
          <div class="flex justify-between items-center px-6 h-16 w-full">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary" style="font-size: 28px;">ice_skating</span>
              <span class="font-headline font-black text-2xl tracking-tight text-primary">Penguin</span>
            </div>
            <div class="flex items-center gap-4">
              <span class="font-headline font-bold text-lg text-primary bg-primary/5 px-3 py-1 rounded-full border border-primary/10">Jour {days}</span>
              <div class="w-10 h-10 rounded-full bg-surface-container-highest flex items-center justify-center">
                <span class="material-symbols-outlined text-primary">person</span>
              </div>
            </div>
          </div>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_stats_card(fauna: dict[str, int]) -> None:
    """Conversion Legend / Wildlife Stats Card - fidèle au HTML."""
    st.markdown(
        f"""
        <div class="w-full max-w-md bg-white/40 border border-white/60 p-4 rounded-lg mb-6 backdrop-blur-sm grid grid-cols-4 gap-2 text-center">
          <div class="flex flex-col items-center">
            <span class="material-symbols-outlined text-secondary text-xl">flutter_dash</span>
            <span class="text-[10px] font-bold mt-1">{fauna["gulls"]}</span>
            <span class="text-[8px] uppercase text-on-surface-variant">Mouettes</span>
          </div>
          <div class="flex flex-col items-center border-l border-white/60">
            <span class="material-symbols-outlined text-primary text-xl">ice_skating</span>
            <span class="text-[10px] font-bold mt-1">{fauna["penguins"]}</span>
            <span class="text-[8px] uppercase text-on-surface-variant">Penguin</span>
          </div>
          <div class="flex flex-col items-center border-l border-white/60">
            <span class="material-symbols-outlined text-blue-800 text-xl">water_ec</span>
            <span class="text-[10px] font-bold mt-1">{fauna["orcas"]}</span>
            <span class="text-[8px] uppercase text-on-surface-variant">Orque</span>
          </div>
          <div class="flex flex-col items-center border-l border-white/60">
            <span class="material-symbols-outlined text-error text-xl">sailing</span>
            <span class="text-[10px] font-bold mt-1">{fauna["sharks"]}</span>
            <span class="text-[8px] uppercase text-on-surface-variant">Requin</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bento_grid() -> None:
    """Bento Grid Info Section - Océan, Danger."""
    st.markdown(
        """
        <div class="grid grid-cols-2 gap-4 w-full max-w-md">
          <div class="bg-surface-container-low p-5 rounded-lg flex flex-col gap-2">
            <span class="material-symbols-outlined text-secondary">waves</span>
            <span class="font-headline font-bold text-on-surface">Océan</span>
            <span class="text-xs text-on-surface-variant">-2°C Arctique</span>
          </div>
          <div class="bg-surface-container-low p-5 rounded-lg flex flex-col gap-2">
            <span class="material-symbols-outlined text-amber-800">warning</span>
            <span class="font-headline font-bold text-on-surface">Danger</span>
            <span class="text-xs text-on-surface-variant">Requin & Orque</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_banquise(user: dict[str, Any]) -> None:
    """Vue Banquise : structure fidèle au HTML fourni."""
    days = int(user["days"])
    fauna = breakdown_days(days)

    render_header(user)
    st.markdown(
        """
        <main class="flex-grow pt-24 pb-32 px-6 flex flex-col items-center justify-start relative overflow-hidden">
          <div class="absolute top-40 -left-20 w-64 h-64 bg-surface-container-low rounded-xl rotate-12 -z-10" style="position:absolute;top:10rem;left:-5rem;width:16rem;height:16rem;background:#f0f4f8;border-radius:0.75rem;transform:rotate(12deg);z-index:-1"></div>
          <div class="absolute bottom-60 -right-20 w-80 h-80 bg-surface-container-highest rounded-xl -rotate-6 -z-10" style="position:absolute;bottom:15rem;right:-5rem;width:20rem;height:20rem;background:#dfe3e7;border-radius:0.75rem;transform:rotate(-6deg);z-index:-1"></div>
        """,
        unsafe_allow_html=True,
    )
    render_stats_card(fauna)
    render_banquise_scene(int(user["id"]), fauna)
    render_bento_grid()
    st.markdown("</main>", unsafe_allow_html=True)


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
            st.stop()

        current_user = get_user_by_id(int(st.session_state["user_id"]))
        if current_user is None:
            logout()
            st.error("Session invalide. Reconnecte-toi.")
            st.stop()

        user_id = int(current_user["id"])

        if "reset_confirm" in st.query_params:
            set_user_days(user_id, 0)
            st.session_state["show_reset_modal"] = False
            st.query_params.clear()
            st.rerun()

        if "cancel" in st.query_params:
            st.session_state["show_reset_modal"] = False
            st.query_params.clear()
            st.rerun()

        if "tab" in st.query_params:
            t = st.query_params.get("tab", "Banquise")
            if t in ("Banquise", "Amis", "Profil"):
                st.session_state["tab"] = t
            st.query_params.clear()
            st.rerun()

        if st.session_state.get("show_reset_modal", False):
            render_reset_modal_overlay()
            st.stop()

        tab = st.session_state.get("tab", "Banquise")

        render_header(current_user)

        if tab == "Banquise":
            render_banquise(current_user)
        elif tab == "Amis":
            render_amis(current_user)
        else:
            render_profil(current_user, cookie_manager)

        st.markdown(
            f"""
            <nav class="fixed bottom-0 left-0 w-full flex justify-around items-center px-4 pb-6 pt-3 bg-white/80 backdrop-blur-xl shadow-[0px_-12px_32px_rgba(0,52,101,0.04)] rounded-t-[2rem] z-50" style="position:fixed;bottom:0;left:0;right:0;display:flex;justify-content:space-around;align-items:center;padding:0.75rem 1rem 1.5rem;background:rgba(255,255,255,0.8);backdrop-filter:blur(24px);box-shadow:0 -12px 32px rgba(0,52,101,0.04);border-radius:2rem 2rem 0 0;z-index:50">
              <a href="?tab=Banquise" style="display:flex;flex-direction:column;align-items:center;padding:0.5rem 1.25rem;border-radius:9999px;text-decoration:none;color:{"#003465" if tab == "Banquise" else "#64748b"};background:{"#003465" if tab == "Banquise" else "transparent"};color:{"white" if tab == "Banquise" else "#64748b"}">
                <span class="material-symbols-outlined" style="font-size:24px">home</span>
                <span style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;margin-top:4px">Banquise</span>
              </a>
              <a href="?tab=Amis" style="display:flex;flex-direction:column;align-items:center;padding:0.5rem 1.25rem;border-radius:9999px;text-decoration:none;color:{"#003465" if tab == "Amis" else "#64748b"};background:{"#003465" if tab == "Amis" else "transparent"};color:{"white" if tab == "Amis" else "#64748b"}">
                <span class="material-symbols-outlined" style="font-size:24px">group</span>
                <span style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;margin-top:4px">Amis</span>
              </a>
              <a href="?tab=Profil" style="display:flex;flex-direction:column;align-items:center;padding:0.5rem 1.25rem;border-radius:9999px;text-decoration:none;color:{"#003465" if tab == "Profil" else "#64748b"};background:{"#003465" if tab == "Profil" else "transparent"};color:{"white" if tab == "Profil" else "#64748b"}">
                <span class="material-symbols-outlined" style="font-size:24px">person</span>
                <span style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;margin-top:4px">Profil</span>
              </a>
            </nav>
            """,
            unsafe_allow_html=True,
        )
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
