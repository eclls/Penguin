"""Utilitaires partagés pour l'app Penguin."""
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


def inject_penguin_css():
    """Injecte le CSS commun Penguin dans la page."""
    st.markdown(
        """
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <style>
        .material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
        .stApp { background-color: #f6fafe !important; }
        .penguin-card { background: rgba(255,255,255,0.9); border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,52,101,0.08); }
        .penguin-primary { color: #003465; }
        .penguin-headline { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; }
        .penguin-body { font-family: 'Be Vietnam Pro', sans-serif; }
    </style>
    """,
        unsafe_allow_html=True,
    )


def icon(name: str, size: int = 24, fill: bool = False) -> str:
    """Retourne le HTML d'une icône Material Symbols."""
    fill_val = 1 if fill else 0
    return f'<span class="material-symbols-outlined" style="font-size:{size}px; font-variation-settings:\'FILL\' {fill_val};">{name}</span>'
