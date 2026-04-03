# POC Avantages Sportifs

## 1. Contexte du projet

Ce projet a été réalisé dans le cadre du projet OpenClassrooms **"Gérez un projet d'infrastructure"**.

Le contexte est celui de l'entreprise fictive **Sport Data Solution**. Juliette, cofondatrice de l'entreprise, veut lancer un **POC** pour tester une solution d'avantages sportifs pour les salariés.

L'idée est de vérifier si la solution est faisable, quelles données il faut collecter, et quel serait le coût pour l'entreprise.

Le projet couvre tout le cycle de traitement des données :
- chargement des fichiers source ;
- création des tables métier ;
- nettoyage ;
- simulation d'activités sportives ;
- contrôle des trajets domicile-travail ;
- calcul des avantages ;
- tests qualité ;
- monitoring ;
- dashboards Metabase ;
- démonstration live ;
- envoi d'un message Slack.

---

## 2. Objectifs du POC

Le POC doit répondre à trois questions simples :

1. **Est-ce que la solution est faisable techniquement ?**
2. **Quelles données doit-on collecter ?**
3. **Quel est l'impact financier pour l'entreprise ?**

Deux avantages sont testés dans le projet.

### 2.1 Prime sportive
Un salarié peut toucher une **prime de 5 % de son salaire annuel brut** s'il vient au bureau avec un mode de déplacement sportif.

### 2.2 5 jours bien-être
Un salarié peut obtenir **5 jours bien-être** s'il a une pratique sportive régulière en dehors du travail.

Dans ce projet, la règle retenue est :
- **au moins 15 activités sportives sur l'année**.

### 2.3 Contrôle des trajets
Les trajets domicile → bureau sont contrôlés avec **Google Maps API**.

Règles utilisées :
- **Marche/Running** : maximum **15 km** ;
- **Vélo/Trottinette/Autres** : maximum **25 km**.

### 2.4 Slack
Une activité sportive peut générer automatiquement un message dans Slack pour encourager l'émulation entre les salariés.

---

## 3. Stack technique

### Langage
- **Python 3.12**

### Base de données
- **PostgreSQL 16**

### Conteneurs
- **Docker**
- **Docker Compose**

### Visualisation
- **Metabase**

### APIs externes
- **Google Maps API** pour le contrôle des trajets ;
- **Slack Incoming Webhook** pour le message de démonstration.

### Bibliothèques principales
- `pandas`
- `openpyxl`
- `sqlalchemy`
- `psycopg2-binary`
- `python-dotenv`
- `requests`
- `faker`

---

## 4. Vue d'ensemble de la solution

```text
Fichiers Excel RH + Sport
        ↓
Chargement brut dans PostgreSQL
        ↓
Création des tables métier
        ↓
Nettoyage et standardisation
        ↓
Simulation de 12 mois d'activités sportives
        ↓
Contrôle des trajets avec Google Maps
        ↓
Calcul des avantages salariés
        ↓
Contrôles qualité
        ↓
Monitoring (pipeline, volumétrie, KPI historisés)
        ↓
Dashboards Metabase + message Slack de démonstration
```

---

## 5. Architecture fonctionnelle

### Sources d'entrée
- `Données RH.xlsx`
- `Données Sportive.xlsx`

### Traitements principaux
- chargement brut ;
- construction des tables métier ;
- nettoyage ;
- simulation des activités ;
- contrôle des trajets ;
- calcul des avantages ;
- tests qualité ;
- monitoring et historisation des KPI.

### Sorties
- tables métier dans PostgreSQL ;
- vues SQL pour dashboards ;
- dashboards Metabase ;
- message Slack ;
- démonstration live.

---

## 6. Structure du projet

```text
.
├── data/
│   ├── raw/
│   │   ├── Données RH.xlsx
│   │   ├── Données Sportive.xlsx
│   │   └── Note de cadrage POC Avantages Sportifs.pdf
│   └── processed/
├── sql/
│   ├── 01_schema.sql
│   ├── 02_private_dashboard_views.sql
│   ├── 03_public_dashboard_views.sql
│   ├── 04_monitoring.sql
│   ├── 05_roles_and_permissions.sql
│   └── 06_constraints.sql
├── src/
│   ├── db.py
│   ├── load_raw_data.py
│   ├── build_business_tables.py
│   ├── clean_business_data.py
│   ├── simulate_sport_activities.py
│   ├── load_reward_parameters.py
│   ├── check_commutes.py
│   ├── calculate_rewards.py
│   ├── run_quality_checks.py
│   ├── capture_kpi_snapshot.py
│   ├── capture_table_volumes.py
│   ├── run_full_pipeline.py
│   ├── send_slack_message.py
│   ├── demo_add_activity.py
│   ├── demo_show_status.py
│   ├── demo_run_live.py
│   └── demo_reset.py
├── docker-compose.yml
├── requirements.txt
├── setup_project.sh
├── .env.example
└── README.md
```

---

## 7. Rôle de chaque fichier

## 7.1 Fichiers à la racine

### `README.md`
Document principal du projet.

### `docker-compose.yml`
Démarre PostgreSQL et Metabase.

### `requirements.txt`
Liste les dépendances Python.

### `.env.example`
Modèle des variables d'environnement à renseigner.

### `setup_project.sh`
Applique tout le SQL dans le bon ordre.

---

## 7.2 Dossier `data/raw/`

### `Données RH.xlsx`
Contient les données RH de départ.

### `Données Sportive.xlsx`
Contient les déclarations sportives de départ.

### `Note de cadrage ... .pdf`
Document métier de référence.

---

## 7.3 Dossier `sql/`

### `01_schema.sql`
Crée les tables principales :
- `rh_raw`
- `sport_raw`
- `employees`
- `employee_sports`
- `reward_parameters`
- `commute_checks`
- `sport_activities`
- `reward_results`
- `quality_checks_results`
- `pipeline_runs`
- `table_volume_history`

### `02_private_dashboard_views.sql`
Crée les vues utilisées par le dashboard privé RH / direction.

### `03_public_dashboard_views.sql`
Crée les vues utilisées par le dashboard public, sans données sensibles.

### `04_monitoring.sql`
Crée les éléments liés au monitoring :
- vues de suivi du pipeline ;
- vues de qualité ;
- vues de volumétrie ;
- table `kpi_history` ;
- vues `vw_latest_kpi_snapshot` et `vw_kpi_history`.

### `05_roles_and_permissions.sql`
Crée les rôles SQL et applique les droits d'accès :
- `role_analytics` pour le dashboard public ;
- `role_rh_admin` pour le dashboard privé et le monitoring.

### `06_constraints.sql`
Ajoute des contraintes SQL pour renforcer la cohérence des données :
- valeurs autorisées pour `commute_mode` ;
- montants non négatifs ;
- statuts autorisés ;
- cohérence des dates ;
- unicité de certains champs ;
- clés étrangères entre tables.

---

## 7.4 Dossier `src/`

### `db.py`
Centralise la connexion à PostgreSQL.

### `load_raw_data.py`
Charge les fichiers Excel dans `rh_raw` et `sport_raw`.

### `build_business_tables.py`
Construit `employees` et `employee_sports` à partir des tables brutes.

Ce script fait aussi la **normalisation minimale obligatoire** avant insertion en base, surtout pour `commute_mode`, afin de respecter les contraintes SQL.

### `clean_business_data.py`
Fait un nettoyage complémentaire sur les données métier déjà chargées.

### `simulate_sport_activities.py`
Génère un historique cohérent d'activités sportives sur 12 mois.

### `load_reward_parameters.py`
Charge les paramètres métier :
- taux de prime ;
- seuil de 15 activités ;
- seuils de distance.

### `check_commutes.py`
Contrôle les trajets domicile-travail avec Google Maps.

### `calculate_rewards.py`
Calcule les avantages salariés :
- prime sportive ;
- éligibilité aux 5 jours bien-être ;
- coût estimé.

### `run_quality_checks.py`
Lance les tests qualité et stocke le résultat dans `quality_checks_results`.

### `capture_kpi_snapshot.py`
Enregistre un snapshot des KPI métier dans `kpi_history`.

### `capture_table_volumes.py`
Enregistre la volumétrie des tables dans `table_volume_history`.

### `run_full_pipeline.py`
Exécute tout le pipeline dans le bon ordre et journalise chaque étape dans `pipeline_runs`.

### `send_slack_message.py`
Envoie un message Slack basé sur la dernière activité sportive.

### `demo_add_activity.py`
Ajoute des activités de démonstration pour faire passer un salarié au seuil de 15 activités.

### `demo_show_status.py`
Affiche l'état avant / après du salarié utilisé pour la démonstration.

### `demo_run_live.py`
Lance toute la démo live :
- état avant ;
- ajout des activités ;
- recalcul ;
- contrôles qualité ;
- snapshot KPI ;
- volumétrie ;
- Slack ;
- état après.

### `demo_reset.py`
Supprime les activités de démonstration et remet l'état initial.

---

## 8. Installation

## 8.1 Prérequis
- Python 3.12
- Docker
- Docker Compose

## 8.2 Créer l'environnement Python

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 8.3 Configurer les variables d'environnement

Créer un fichier `.env` à partir de `.env.example`.

Exemple :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sport_data
DB_USER=sport_user
DB_PASSWORD=sport_password

COMPANY_ADDRESS=1362 Avenue des Platanes, 34970 Lattes, France

PRIME_RATE=0.05
MIN_ACTIVITIES_FOR_WELLBEING=15
MAX_DISTANCE_WALK_RUN_KM=15
MAX_DISTANCE_BIKE_OTHER_KM=25

SLACK_WEBHOOK_URL=
GOOGLE_MAPS_API_KEY=
```

## 8.4 Démarrer l'infrastructure

```bash
docker compose up -d
```

---

## 9. Initialisation SQL

Appliquer tout le SQL avec une seule commande :

```bash
./setup_project.sh
```

Ce script applique :
1. `01_schema.sql`
2. `02_private_dashboard_views.sql`
3. `03_public_dashboard_views.sql`
4. `04_monitoring.sql`
5. `05_roles_and_permissions.sql`
6. `06_constraints.sql`

---

## 10. Exécution du pipeline

## 10.1 Lancer tout le pipeline

```bash
python3 src/run_full_pipeline.py
```

Ordre d'exécution :
1. `load_raw_data.py`
2. `build_business_tables.py`
3. `clean_business_data.py`
4. `simulate_sport_activities.py`
5. `load_reward_parameters.py`
6. `check_commutes.py`
7. `calculate_rewards.py`
8. `run_quality_checks.py`
9. `capture_kpi_snapshot.py`
10. `capture_table_volumes.py`

## 10.2 Lancer les scripts séparément

Exemple :

```bash
python3 src/load_raw_data.py
python3 src/build_business_tables.py
python3 src/calculate_rewards.py
```

---

## 11. Monitoring

Le monitoring est basé sur PostgreSQL + Metabase.

### Tables et vues utilisées
- `pipeline_runs`
- `quality_checks_results`
- `table_volume_history`
- `kpi_history`
- `vw_pipeline_status`
- `vw_quality_summary`
- `vw_latest_table_volumes`
- `vw_table_volume_history`
- `vw_monitoring_last_success`
- `vw_monitoring_failed_steps`
- `vw_monitoring_failed_quality_checks`
- `vw_latest_kpi_snapshot`
- `vw_kpi_history`

### Ce que le monitoring permet de suivre
- l'état des étapes du pipeline ;
- le nombre d'échecs ;
- les contrôles qualité ;
- la volumétrie des tables ;
- l'évolution de certains KPI métier dans le temps.

---

## 12. Dashboards Metabase

Le projet utilise **Metabase** comme outil de restitution, en remplacement d'un outil de type Power BI.

### Dashboard 1 — Public
**Objectif :** montrer une vue globale sans données sensibles.

Exemples de KPI :
- nombre total de salariés ;
- salariés pratiquant un sport ;
- nombre total d'activités ;
- taux de participation ;
- éligibilité au trajet sportif ;
- éligibilité aux 5 jours bien-être.

### Dashboard 2 — Privé RH / Direction
**Objectif :** suivre l'impact financier détaillé et les données RH.

Exemples de KPI :
- coût total des primes ;
- salariés éligibles à la prime ;
- salariés éligibles aux 5 jours ;
- tableau détaillé par salarié.

### Dashboard 3 — Monitoring du pipeline
**Objectif :** suivre l'état d'exécution et la volumétrie.

Exemples de KPI :
- dernière exécution réussie ;
- nombre d'étapes en échec ;
- contrôles qualité ;
- volumétrie actuelle ;
- historique des KPI.

### Connexions Metabase utilisées

#### `SPORT_DATA_PUBLIC`
- utilisateur SQL : `role_analytics`
- accès aux vues publiques uniquement

#### `SPORT_DATA_PRIVATE`
- utilisateur SQL : `role_rh_admin`
- accès aux vues privées et au monitoring

---

## 13. Sécurité et séparation des accès

Le projet sépare les accès SQL avec deux rôles :

### `role_analytics`
Accès seulement aux vues publiques.

### `role_rh_admin`
Accès aux vues privées et au monitoring.

Cela permet d'appliquer une logique de **moindre privilège**.

---

## 14. Démonstration live

## 14.1 Objectif
Montrer en direct qu'un salarié passe de **0 activité** à **15 activités**, puis devient éligible aux **5 jours bien-être**.

## 14.2 Vérifier l'état avant

```bash
python3 src/demo_show_status.py
```

## 14.3 Lancer la démo

```bash
python3 src/demo_run_live.py
```

Ce script :
- affiche l'état avant ;
- ajoute les activités de démonstration ;
- relance le calcul ;
- relance les contrôles qualité ;
- enregistre un snapshot KPI ;
- met à jour la volumétrie ;
- envoie un message Slack ;
- affiche l'état après.

## 14.4 Revenir à l'état initial

```bash
python3 src/demo_reset.py
```

---

## 15. Résultats attendus

À la fin du pipeline, on obtient :
- une base PostgreSQL structurée ;
- des vues SQL pour la restitution ;
- trois dashboards Metabase ;
- un monitoring des exécutions ;
- une historisation de certains KPI ;
- une démo live reproductible ;
- un message Slack de démonstration.

---

## 16. Limites du projet

Ce projet est un **POC**.

Cela veut dire que certaines parties restent simples :
- pas d'orchestrateur complet type Airflow ou Kestra ;
- pas de scheduling automatique ;
- dashboards Metabase à reconstruire manuellement si l'environnement Metabase est réinitialisé ;
- utilisation de données simulées à la place d'une vraie connexion Strava.

---

## 17. Pistes d'amélioration

Quelques améliorations possibles :
- brancher une vraie API sportive comme Strava ;
- ajouter un scheduler ou un orchestrateur ;
- historiser encore plus finement les KPI ;
- exporter ou sauvegarder automatiquement les dashboards Metabase ;
- renforcer encore la gestion des secrets et des droits SQL.

---

## 18. Conclusion

Ce projet permet de démontrer un pipeline de données de bout en bout autour d'un cas métier simple et concret.

La solution mise en place couvre :
- l'ingestion des données ;
- la transformation ;
- la simulation ;
- le contrôle métier ;
- le calcul des avantages ;
- les tests qualité ;
- le monitoring ;
- la démonstration live ;
- la restitution dans Metabase.

Le projet est donc adapté à un **POC fonctionnel**, démontrable et compréhensible.
