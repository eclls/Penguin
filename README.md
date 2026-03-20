# Penguin 🐧

Application Streamlit **mobile-first** en **mono-fichier** (`app.py`) pour simplifier le deploiement.

## Fonctionnalites

- Authentification locale simple par pseudo (sans mot de passe).
- Compteur `Jour X`.
- Conversion stricte :
  - `1 jour = 1 mouette`
  - `30 mouettes = 1 pingouin`
  - `6 pingouins = 1 orque`
  - `2 orques = 1 requin`
- Modale d'ouverture : **"Tu as tue le pinguin ? Secoue toi"**.
- Social : ajout d'amis + progression.
- Profil : ajustement manuel du compteur.
- Navigation interne (Banquise / Vue illustree / Amis / Profil) depuis `app.py`.

## Lancement local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploiement Streamlit

Tu n'as besoin de renseigner que le fichier d'entree : **`app.py`**.

## Persistance des donnees

Base SQLite par defaut: `data/penguin.db`.

Chemin custom (remote):

```bash
export PENGUIN_DB_PATH=/tmp/penguin.db
```
