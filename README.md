# Projet 12 - Gérez un projet d’infrastructure  
## Option B - Créez et automatisez une architecture de données

## 1. Présentation du projet

Ce projet a été réalisé dans le cadre de la formation **Data Engineer** chez **OpenClassrooms**.

Le contexte est celui de l’entreprise fictive **Sport Data Solution**. L’objectif est de construire un **POC** pour tester une solution capable de :

- suivre la pratique sportive des salariés ;
- calculer automatiquement les avantages accordés ;
- estimer le coût financier pour l’entreprise ;
- publier les activités sportives dans Slack ;
- afficher les principaux indicateurs dans un dashboard.

Le projet repose sur des **fichiers Excel sources**, une **base PostgreSQL**, un **pipeline Python**, l’API **Google Maps**, **Slack** et **Metabase** pour la partie reporting.

---

## 2. Besoin métier

Sport Data Solution souhaite encourager la pratique du sport chez ses salariés.

Deux avantages sont testés dans ce POC :

### Prime sportive
Un salarié peut recevoir une prime de **5 % de son salaire annuel brut** s’il vient au bureau en utilisant un mode de déplacement sportif.

Exemples :
- marche ;
- course à pied ;
- vélo ;
- trottinette.

### 5 journées bien-être
Un salarié peut obtenir **5 jours bien-être** s’il pratique une activité sportive régulière en dehors du travail.

Dans ce projet, la règle retenue est :
- **au moins 15 activités sportives sur l’année**.

### Contrôle des trajets
Le projet doit aussi vérifier si les déclarations domicile → bureau sont cohérentes.

Les règles utilisées sont :
- **Marche / Running** : maximum **15 km** ;
- **Vélo / Trottinette / Autres** : maximum **25 km**.

Cette validation est faite avec l’API **Google Maps**.

### Slack
Chaque nouvelle activité sportive peut générer automatiquement un message dans un channel Slack.

### Reporting
Les principaux KPI doivent être visualisables dans un outil de reporting. Dans ce projet, **Metabase** est utilisé comme équivalent fonctionnel d’un outil type Power BI.

---

## 3. Objectifs du POC

Le POC doit permettre de :

- tester la faisabilité technique de la solution ;
- identifier les données utiles à collecter ;
- calculer l’impact financier de la prime sportive ;
- simuler un historique cohérent d’activités sportives sur 12 mois ;
- automatiser un pipeline simple et rejouable ;
- contrôler la qualité des données ;
- suivre l’exécution du pipeline ;
- restituer les résultats dans un dashboard clair.

---

## 4. Stack technique

### Langage
- **Python 3.12**

### Base de données
- **PostgreSQL 16**

### Conteneurisation
- **Docker**
- **Docker Compose**

### Exploration de la base
- **DBeaver**

### APIs externes
- **Google Maps API** : validation des trajets domicile → bureau
- **Slack Incoming Webhook** : publication des activités sportives

### Visualisation
- **Metabase**

### Principales bibliothèques Python
- `pandas`
- `openpyxl`
- `sqlalchemy`
- `psycopg2-binary`
- `python-dotenv`
- `requests`
- `faker`

### Pourquoi ces choix
Ces outils ont été retenus parce qu’ils sont :
- simples à mettre en place ;
- adaptés à un POC ;
- faciles à expliquer pendant une soutenance ;
- suffisants pour couvrir tout le besoin métier.

---

## 5. Architecture de la solution

### Vue d’ensemble

```text
Fichiers Excel RH + Sport
        ↓
Chargement brut dans PostgreSQL
        ↓
Nettoyage et transformation
        ↓
Création des tables métier
        ↓
Simulation des activités sportives sur 12 mois
        ↓
Contrôle des trajets avec Google Maps
        ↓
Calcul des avantages salariés
        ↓
Tests qualité + monitoring
        ↓
Publication Slack + Dashboard Metabase
```

### Outils utilisés dans le flux

```text
Excel → Python → PostgreSQL → Google Maps / Slack → Metabase
```

---

## 6. Structure du projet

```text
12_Gérez_un_projet_dinfrastructure/
├── data/
│   ├── raw/
│   │   ├── Données RH.xlsx
│   │   ├── Données Sportive.xlsx
│   │   └── Note de cadrage POC Avantages Sportifs.pdf
│   └── processed/
├── sql/
│   ├── schema.sql
│   └── dashboard_views.sql
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
│   ├── run_full_pipeline.py
│   ├── send_slack_message.py
│   └── demo_add_activity.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 7. Modèle de données

Le projet s’appuie sur trois niveaux de tables.

### A. Tables brutes
- `rh_raw`
- `sport_raw`

Elles conservent les fichiers sources sous une forme proche de l’origine.

### B. Tables métier
- `employees`
- `employee_sports`
- `sport_activities`
- `commute_checks`
- `reward_results`

Elles servent au traitement métier.

### C. Tables de pilotage
- `reward_parameters`
- `pipeline_runs`
- `quality_checks_results`

Elles servent au suivi du pipeline et à la qualité des données.

### Vues pour le reporting
- `vw_kpi_summary`
- `vw_activities_by_month`
- `vw_top_sports`
- `vw_commute_status`
- `vw_employee_rewards`

---

## 8. Règles métier implémentées

### Prime sportive
La prime est accordée si :
- le salarié utilise un mode de déplacement sportif ;
- le trajet domicile → bureau est validé par Google Maps ;
- le taux de prime est stocké dans `reward_parameters`.

### Journées bien-être
Le salarié obtient **5 jours** s’il atteint au moins **15 activités sportives** sur l’année.

### Paramètres modifiables
Les paramètres sont stockés dans le fichier `.env` puis chargés dans la base :
- `PRIME_RATE`
- `MIN_ACTIVITIES_FOR_WELLBEING`
- `MAX_DISTANCE_WALK_RUN_KM`
- `MAX_DISTANCE_BIKE_OTHER_KM`

Cela permet de rejouer le calcul sans modifier le code métier.

---

## 9. Préparation de l’environnement

### Prérequis
- macOS, Linux ou Windows
- Python 3.12
- Docker Desktop
- Git

### Cloner le projet
```bash
git clone <url-du-repo>
cd 12_Gérez_un_projet_dinfrastructure
```

### Créer l’environnement virtuel
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Créer le fichier `.env`
À partir de `.env.example`, crée un fichier `.env` à la racine du projet.

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

### Lancer les conteneurs
```bash
docker compose up -d
```

---

## 10. Initialisation de la base

### Création des tables SQL de base
```bash
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/schema.sql
```

### Création des vues pour le dashboard
```bash
docker exec -i sport_data_postgres psql -U sport_user -d sport_data < sql/dashboard_views.sql
```

---

## 11. Exécution du pipeline

Le projet peut être lancé étape par étape ou via un script global.

### Étapes individuelles

#### 1. Chargement brut des fichiers Excel
```bash
python3 src/load_raw_data.py
```
Crée et alimente :
- `rh_raw`
- `sport_raw`

#### 2. Création des tables métier
```bash
python3 src/build_business_tables.py
```
Crée et alimente :
- `employees`
- `employee_sports`

#### 3. Nettoyage des données métier
```bash
python3 src/clean_business_data.py
```
Normalise :
- les modes de déplacement ;
- les sports déclarés ;
- certaines valeurs manquantes.

#### 4. Simulation des activités sportives
```bash
python3 src/simulate_sport_activities.py
```
Alimente la table `sport_activities` avec un historique simulé sur 12 mois.

#### 5. Chargement des paramètres métier
```bash
python3 src/load_reward_parameters.py
```
Alimente la table `reward_parameters`.

#### 6. Contrôle des trajets domicile → bureau
```bash
python3 src/check_commutes.py
```
Alimente la table `commute_checks` avec le résultat de validation.

#### 7. Calcul des avantages salariés
```bash
python3 src/calculate_rewards.py
```
Alimente la table `reward_results`.

#### 8. Contrôles qualité
```bash
python3 src/run_quality_checks.py
```
Alimente la table `quality_checks_results`.

### Exécution complète du pipeline
```bash
python3 src/run_full_pipeline.py
```

Ce script exécute toutes les étapes dans l’ordre et journalise chaque exécution dans `pipeline_runs`.

---

## 12. Contrôles qualité

Le projet contient des contrôles automatiques sur les principales tables.

Exemples :
- `employees` non vide ;
- `employee_id` unique ;
- `commute_mode` dans la liste autorisée ;
- dates des activités cohérentes ;
- distances non négatives ;
- activités reliées à un salarié existant ;
- `reward_results` avec le bon nombre de lignes ;
- montants de prime non négatifs ;
- jours bien-être égaux à `0` ou `5`.

Les résultats sont stockés dans :
- `quality_checks_results`

---

## 13. Monitoring

Le projet suit l’exécution des étapes du pipeline dans la table :
- `pipeline_runs`

Pour chaque étape, on enregistre :
- le nom ;
- le statut ;
- le nombre de lignes traitées ;
- un message.

Cela permet de rejouer le pipeline et de vérifier qu’il s’exécute correctement.

---

## 14. Dashboard Metabase

### Lancer Metabase
Une fois `docker compose up -d` exécuté, Metabase est disponible à l’adresse :

```text
http://localhost:3000
```

### Connexion à PostgreSQL dans Metabase
Utiliser les paramètres suivants :
- Host : `host.docker.internal` (ou `localhost` selon la configuration Docker)
- Port : `5432`
- Database : `sport_data`
- User : `sport_user`
- Password : `sport_password`

### Vues utilisées pour le dashboard
- `vw_kpi_summary`
- `vw_activities_by_month`
- `vw_top_sports`
- `vw_commute_status`
- `vw_employee_rewards`

### KPI suivis
- coût total estimé des primes ;
- nombre total d’activités ;
- nombre total de salariés ;
- salariés éligibles à la prime ;
- salariés éligibles aux 5 jours ;
- total de jours bien-être accordés ;
- activité par mois ;
- sports les plus pratiqués ;
- validation des trajets domicile-bureau ;
- détail des avantages par salarié.

### Remarque sur l’outil de reporting
La visualisation a été réalisée avec **Metabase**. Dans ce projet, Metabase est utilisé comme **équivalent fonctionnel** d’un outil type Power BI.

---

## 15. Slack

Le projet utilise un **Incoming Webhook Slack** pour publier automatiquement la dernière activité sportive enregistrée.

### Script utilisé
```bash
python3 src/send_slack_message.py
```

### Fonctionnement
Le script :
- lit la dernière activité de `sport_activities` ;
- construit un message lisible ;
- l’envoie dans le channel Slack configuré dans `.env`.

---

## 16. Démonstration live

Deux démonstrations ont été préparées.

### A. Changement du taux de prime
Modifier dans `.env` :

```env
PRIME_RATE=0.06
```

Puis relancer :

```bash
python3 src/load_reward_parameters.py
python3 src/calculate_rewards.py
```

Résultat attendu :
- le coût total estimé des primes change dans Metabase.

### B. Ajout d’une activité sportive
Le script ci-dessous permet d’ajouter des activités de démonstration :

```bash
python3 src/demo_add_activity.py
python3 src/calculate_rewards.py
python3 src/send_slack_message.py
```

Résultat attendu :
- nouvelle activité ajoutée dans la base ;
- message envoyé dans Slack ;
- mise à jour du reporting dans Metabase.

---

## 17. Vérifications utiles

### Vérifier que le pipeline tourne
```bash
python3 src/run_full_pipeline.py
```

### Vérifier les tables dans PostgreSQL
```bash
docker exec -it sport_data_postgres psql -U sport_user -d sport_data -c "\dt"
```

### Vérifier les vues
```bash
docker exec -it sport_data_postgres psql -U sport_user -d sport_data -c "\dv"
```

---

## 18. Points forts du projet

- pipeline clair et rejouable ;
- séparation entre tables brutes, métier et reporting ;
- intégration d’une API externe utile pour le besoin métier ;
- publication automatique dans Slack ;
- dashboard simple et lisible ;
- tests qualité ;
- monitoring des exécutions.

---

## 19. Limites actuelles

- les activités sportives sont simulées et non récupérées depuis une API sportive réelle ;
- le POC repose sur des fichiers Excel et non sur une source temps réel ;
- le dashboard est réalisé dans Metabase et non dans Power BI ;
- la validation des trajets dépend de la qualité des adresses fournies ;
- l’orchestration reste simple et pourrait être renforcée avec un orchestrateur dédié.

---

## 20. Améliorations possibles

- connecter une API sportive réelle ;
- ajouter une vraie historisation des changements de paramètres ;
- industrialiser l’orchestration avec Airflow, Kestra ou un outil équivalent ;
- renforcer la sécurité des secrets ;
- ajouter plus de tests automatisés ;
- déployer la solution sur un environnement cloud.

---

## 21. Auteur

Projet réalisé dans le cadre du **Projet 12 - Gérez un projet d’infrastructure** de la formation **Data Engineer OpenClassrooms**.

Nom et prénom : **[À compléter]**
