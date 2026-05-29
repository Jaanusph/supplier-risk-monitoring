with source as (
    select
        "Andmed on seisuga" as data_as_of_raw,
        "Registrikood" as registry_code_raw,
        "Nimi" as company_name_raw,
        "Maksuvõlg" as tax_debt_raw,
        "sh vaidlustatud" as disputed_amount_raw,
        "sh tasumisgraafikus" as scheduled_amount_raw,
        "Tasumisgraafiku lõppkuupäev" as payment_schedule_end_date_raw,
        "Vanima tasumata nõude tasumise tähtpäev" as oldest_unpaid_due_date_raw,
        loaded_at
    from raw_mta_tax_debts
),

cleaned as (
    select
        trim(registry_code_raw) as registry_code,
        trim(company_name_raw) as company_name,

        to_date(data_as_of_raw, 'DD.MM.YYYY') as data_as_of_date,

        nullif(replace(replace(tax_debt_raw, ' ', ''), ',', '.'), '')::numeric(14, 2)
            as tax_debt_amount,

        nullif(replace(replace(disputed_amount_raw, ' ', ''), ',', '.'), '')::numeric(14, 2)
            as disputed_amount,

        nullif(replace(replace(scheduled_amount_raw, ' ', ''), ',', '.'), '')::numeric(14, 2)
            as scheduled_amount,

        nullif(payment_schedule_end_date_raw, '')::date as payment_schedule_end_date,
        nullif(oldest_unpaid_due_date_raw, '')::date as oldest_unpaid_due_date,

        case
            when trim(registry_code_raw) ~ '^[0-9]{8}$' then true
            else false
        end as is_estonian_registry_code,

        loaded_at
    from source
)

select *
from cleaned
