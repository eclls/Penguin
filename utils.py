"""Utilitaires partages pour l'app Penguin."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import sqlite3
from pathlib import Path
from typing import Any

import streamlit as st

# Palette de couleurs Penguin
COLORS = {
    "primary": "#003465",
    "primary_container": "#004b8d",
    "secondary": "#326578",
    "secondary_container": "#b5e7fe",
    "surface": "#f6fafe",
    "surface_container_low": "#f0f4f8",
    "surface_container_lowest": "#ffffff",
    "on_surface": "#171c1f",
    "on_surface_variant": "#424750",
    "tertiary": "#4f2b00",
    "tertiary_fixed": "#ffdcbe",
    "error": "#ba1a1a",
}

PASSWORD_ITERATIONS = 200_000


def inject_penguin_css() -> None:
    """Injecte le CSS commun Penguin dans la page."""
    st.markdown(
        """
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet"/>
    <style>
        .stApp {
            background: linear-gradient(180deg, #bde8ff 0%, #eaf7ff 35%, #f6fafe 100%) !important;
        }
        .penguin-card {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 1rem;
            border: 1px solid rgba(0, 52, 101, 0.1);
            padding: 1rem;
            box-shadow: 0 8px 30px rgba(0, 52, 101, 0.08);
        }
        .penguin-hero {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 1.25rem;
            border: 1px solid rgba(0, 52, 101, 0.1);
            box-shadow: 0 12px 30px rgba(0, 52, 101, 0.1);
            padding: 1rem 1.25rem;
        }
        .penguin-title {
            font-family: "Plus Jakarta Sans", sans-serif;
            font-weight: 800;
            color: #003465;
        }
        .penguin-muted {
            color: #4f6474;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def _db_path() -> Path:
    env_path = os.getenv("PENGUIN_DB_PATH", "").strip()
    secret_path = ""
    try:
        secret_path = str(st.secrets.get("penguin_db_path", "")).strip()
    except Exception:
        secret_path = ""

    db_path_raw = env_path or secret_path or "data/penguin.db"
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
    """Cree les tables necessaires si elles n'existent pas."""
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


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )
    return f"{salt.hex()}${pwd_hash.hex()}"


def _verify_password(password: str, encoded: str) -> bool:
    try:
        salt_hex, hash_hex = encoded.split("$", maxsplit=1)
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(hash_hex)
    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )
    return hmac.compare_digest(candidate, expected)


def register_user(username: str, password: str, starting_days: int = 0) -> tuple[bool, str]:
    """Cree un utilisateur."""
    clean_username = username.strip()
    if len(clean_username) < 3:
        return False, "Le nom d'utilisateur doit contenir au moins 3 caracteres."
    if len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caracteres."
    if starting_days < 0:
        return False, "Le nombre de jours ne peut pas etre negatif."

    try:
        with _connect() as conn:
            conn.execute(
                """
                INSERT INTO users (username, password_hash, days)
                VALUES (?, ?, ?)
                """,
                (clean_username, _hash_password(password), int(starting_days)),
            )
    except sqlite3.IntegrityError:
        return False, "Ce nom d'utilisateur existe deja."
    return True, "Compte cree avec succes."


def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    """Retourne l'utilisateur si les credentials sont valides."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
    if row is None:
        return None
    user = dict(row)
    if not _verify_password(password, user["password_hash"]):
        return None
    return user


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
    return dict(row) if row else None


def set_user_days(user_id: int, days: int) -> None:
    with _connect() as conn:
        conn.execute("UPDATE users SET days = ? WHERE id = ?", (max(0, int(days)), int(user_id)))


def add_days(user_id: int, delta: int) -> int:
    """Ajoute des jours et retourne la nouvelle valeur."""
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET days = MAX(0, days + ?) WHERE id = ?",
            (int(delta), int(user_id)),
        )
        row = conn.execute("SELECT days FROM users WHERE id = ?", (int(user_id),)).fetchone()
    return int(row["days"]) if row else 0


def breakdown_days(days: int) -> dict[str, int]:
    """Convertit les jours en mouettes, pingouins, orques et requins."""
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
    """Ajoute un ami mutuellement entre deux comptes."""
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

        conn.execute(
            "INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)",
            (int(user_id), friend_id),
        )
        conn.execute(
            "INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)",
            (friend_id, int(user_id)),
        )
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


def list_discoverable_users(user_id: int, limit: int = 12) -> list[dict[str, Any]]:
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
    """Genere un nuage d'emoji compact pour l'affichage."""
    safe_count = max(0, int(count))
    if safe_count == 0:
        return "—"
    displayed = min(safe_count, max_display)
    cloud = " ".join([emoji] * displayed)
    if safe_count > max_display:
        cloud += f"  +{safe_count - max_display}"
    return cloud
