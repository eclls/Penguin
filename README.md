# Penguin 🐧

Application Streamlit interactive de suivi de progression.

## Fonctionnalites principales

- Compteur **Jour X** avec conversion stricte :
  - `1 jour = 1 mouette`
  - `30 mouettes = 1 pingouin`
  - `6 pingouins = 1 orque`
  - `2 orques = 1 requin`
- Visualisation de la banquise (emoji dynamiques selon la progression).
- Modale d'ouverture : **"Tu as tue le pinguin ? Secoue toi"** avec reset possible.
- Authentification : creation de compte + connexion.
- Social : ajout d'amis et visualisation de leur progression.
- Ajustement manuel : definition du nombre de jours de depart.

## Installation locale

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

## Persistance des donnees

Par defaut, l'application utilise SQLite dans `data/penguin.db`.

Pour un environnement remote, tu peux definir un chemin custom :

```bash
export PENGUIN_DB_PATH=/tmp/penguin.db
```

Ou via `st.secrets` (Streamlit Cloud) :

```toml
penguin_db_path = "/mount/persistent/penguin.db"
```

## Pages

- `app.py` : connexion/inscription + banquise principale.
- `pages/1_Vue_Illustree.py` : decomposition visuelle de la progression.
- `pages/2_Profil.py` : stats utilisateur + ajustement manuel.
- `pages/3_Amis.py` : gestion des amis et progression sociale.
