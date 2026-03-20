# Penguin 🐧

Application **Penguin** – expédition polaire sur banquise. Interface Streamlit inspirée du thème arctique.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

L'app s'ouvre dans le navigateur (par défaut http://localhost:8501).

## Pages

| Page | Description |
|------|-------------|
| **Banquise** (accueil) | Jour 1, stats faune, iceberg, popup "Tu as tué le pinguin ?" |
| **Vue Illustrée** | Jour 256, écosystème (manchots, goélands, orque), détails faune |
| **Profil** | Avatar, stats (jours survécus, poissons), paramètres |
| **Amis** | Communauté, colonie, suggestions glacées |

## Structure

```
Penguin/
├── app.py              # Page d'accueil
├── utils.py            # CSS et utilitaires partagés
├── pages/
│   ├── 1_Vue_Illustree.py
│   ├── 2_Profil.py
│   └── 3_Amis.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

## Déploiement

Compatible Streamlit Cloud, Hugging Face Spaces, ou tout hébergeur supportant Streamlit.
