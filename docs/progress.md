# Sprint 2 progress

## Mis on valmis

- Töötab esimene minimaalne andmevoog MTA maksuvõlglaste CSV põhjal.
- Docker Compose käivitab PostgreSQL andmebaasi ja Streamlit dashboardi.
- Python pipeline tõmbab MTA CSV faili alla ja laeb selle PostgreSQL raw-tabelisse `raw_mta_tax_debts`.
- dbt loob transformeeritud vaate `stg_mta_tax_debts` ja mart-tabeli `mart_tax_debt_summary`.
- Streamlit dashboard kuvab esmased KPI-d ja top 20 maksuvõlglaste tabeli.

## Järgmised sammud

- Lisada tarnijate näidisnimekiri.
- Lisada Äriregistri lihtandmed ja ettevõtte staatuse signaal.
- Lisada tarnijapõhine riskiskoor.
- Lisada vähemalt 3 andmekvaliteedi testi.
- Viimistleda dashboard lõpliku äriküsimuse järgi.

## Mis takistab või vajab täpsustamist

- Käibe/müügitulu allikas vajab veel täpsemat kontrolli.
- Tarnijate nimekiri tuleb koostada avalike ettevõtete põhjal EMTAK koodi ja käibe/müügitulu järgi.
- Scheduler on hetkel planeeritud lõppversiooni osa; Sprint 2 töövoog käivitatakse käsitsi Docker Compose käskudega.
