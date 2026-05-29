import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


def get_engine():
    load_dotenv(dotenv_path=Path(".env"))

    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST", "postgres")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB")

    database_url = (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    return create_engine(database_url)


@st.cache_data(ttl=300)
def load_summary() -> pd.DataFrame:
    engine = get_engine()
    query = """
        select
            data_as_of_date,
            tax_debtor_count,
            total_tax_debt_amount,
            max_tax_debt_amount,
            estonian_registry_code_count,
            non_estonian_registry_code_count
        from mart_tax_debt_summary
    """
    return pd.read_sql(query, engine)


@st.cache_data(ttl=300)
def load_top_debtors(limit: int = 20) -> pd.DataFrame:
    engine = get_engine()
    query = f"""
        select
            registry_code,
            company_name,
            tax_debt_amount,
            disputed_amount,
            scheduled_amount,
            is_estonian_registry_code
        from stg_mta_tax_debts
        where tax_debt_amount is not null
        order by tax_debt_amount desc
        limit {limit}
    """
    return pd.read_sql(query, engine)


st.set_page_config(
    page_title="Tarnijariski seire - Sprint 2",
    layout="wide",
)

st.title("Tarnijariski seire: MTA maksuvõlgade esimene töövoog")

st.write(
    "Sprint 2 minimaalne töövoog kasutab ühte andmeallikat: "
    "MTA maksuvõlglaste CSV. Andmed laaditakse PostgreSQL-i, "
    "puhastatakse dbt-ga ja kuvatakse Streamlit dashboardil."
)

summary = load_summary()

if summary.empty:
    st.warning("Kokkuvõtte tabel on tühi. Käivita esmalt pipeline ja dbt mudelid.")
    st.stop()

row = summary.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("Maksuvõlglaste arv", f"{int(row['tax_debtor_count']):,}".replace(",", " "))
col2.metric(
    "Maksuvõlg kokku",
    f"{row['total_tax_debt_amount']:,.0f} €".replace(",", " ")
)
col3.metric(
    "Suurim maksuvõlg",
    f"{row['max_tax_debt_amount']:,.0f} €".replace(",", " ")
)

st.caption(f"Andmete seis: {row['data_as_of_date']}")

st.subheader("Top 20 maksuvõlglast")

top_debtors = load_top_debtors()

st.dataframe(
    top_debtors,
    use_container_width=True,
    hide_index=True,
)

st.subheader("Top 20 maksuvõla visualiseering")

chart_data = top_debtors[["company_name", "tax_debt_amount"]].set_index("company_name")
st.bar_chart(chart_data)
