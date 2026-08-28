# External data (manual/proprietary inputs)

This folder stores external inputs used by the notebooks, especially
`code/03_validation/Validation_Analyses_final.ipynb`.

## What should be placed here

### 1) LSEG / Refinitiv Data & Analytics extracts
Used to enrich firm-year MAP data with fundamentals, ESG, returns, deals, and ownership.

Expected files referenced in notebooks:
- `LSEG_variable_df_final.pkl` (financial + ESG variables)
- `Monthly_Returns_with_Date.pkl` (monthly stock returns)
- `Ownership_top_20_investors.pkl` (raw ownership pulls)
- `Ownership_measures_final.pkl` (constructed ownership measures)

Notes:
- Retrieval is done through `lseg.data` API calls in the collection/validation workflow.
- Access requires an active LSEG subscription/session.
- The financial + ESG variables to be downloaded are listed in `LSEG_variables_list_final.csv`.

### 2) ISS Incentive Lab data
Used to derive CEO compensation and incentive-related controls.

Expected source files:
- `ParticipantFY.csv`
- `SumComp.csv`

Expected derived file:
- `ISS_CEO_Compensation_final.pkl`

### 3) DISCERN patent data
Used for innovation/proxy variables in the validation analyses.

Notebook reference indicates DISCERN v2.0.1 from Zenodo and expects:
- `discern_firm_panel_1980_2021.csv`
- `Patent_Panel_Data_2015.csv`

Expected derived file:
- `DISCERN_2012_2021.pkl`

## Existing short note (kept for continuity)
DISCERN and ISS files should be placed in this folder. LSEG data are retrieved via notebooks and stored here as intermediate/final extracts.
