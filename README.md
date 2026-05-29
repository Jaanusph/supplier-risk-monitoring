# Supplier Risk Monitoring

Andmeinseneeria kursuse lõputöö projekt.

## Eesmärk

Projekt jälgib avalike andmete põhjal Eesti ettevõtetest tarnijate riski. Sprint 2 seisus on valmis minimaalne töövoog MTA maksuvõlglaste andmete põhjal.

## Töövoog

MTA maksuvõlglaste CSV -> PostgreSQL raw tabel -> dbt transformatsioon -> Streamlit dashboard.

## Stack

- Docker Compose
- PostgreSQL
- Python
- dbt
- Streamlit

## Käivitamine

Eeldus: Docker töötab.

```bash
cp .env.example .env
bash scripts/run_sprint2_pipeline.sh
docker compose up dashboard
Dashboard:

http://localhost:8501
Sprint 2 tulemus

Dashboard näitab maksuvõlglaste arvu, maksuvõlgade kogusummat, suurimat maksuvõlga, top 20 maksuvõlglaste tabelit ja tulpdiagrammi.

Märkused

Toorandmed ei ole repos. Skript tõmbab need käivitamisel data/raw/ kausta. .env ei ole repos, repos on ainult .env.example.
