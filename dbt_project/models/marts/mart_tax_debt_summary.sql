select
    max(data_as_of_date) as data_as_of_date,
    count(*) as tax_debtor_count,
    sum(tax_debt_amount) as total_tax_debt_amount,
    max(tax_debt_amount) as max_tax_debt_amount,
    count(*) filter (where is_estonian_registry_code) as estonian_registry_code_count,
    count(*) filter (where not is_estonian_registry_code) as non_estonian_registry_code_count
from {{ ref('stg_mta_tax_debts') }}
where tax_debt_amount is not null
