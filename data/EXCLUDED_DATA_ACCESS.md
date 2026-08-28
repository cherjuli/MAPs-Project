# Excluded data access notes

The datasets below are not committed because of file size, licensing, or redistribution restrictions. Obtain them from the original provider, keep them outside version control, and preserve the filenames expected by the notebooks.

## Raw SEC 10-K filing text

SEC filings are public and can be downloaded without a subscription or API key.

1. Review the [SEC developer resources](https://www.sec.gov/about/developer-resources) and [EDGAR API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).
2. Run `code/01_data_collection/Downloading_and_Parsing_Filings_final.ipynb` to retrieve and parse the filings required by this project.
3. Store the downloaded raw filing files locally in `data/10-K/`.
4. Run `code/01_data_collection/Preprocessing_Filings_final.ipynb` to create the downstream corpora.

Automated downloads must follow the SEC's fair-access guidance, including use of an identifying user agent and reasonable request rates. Do not commit the downloaded filing corpus.

## LSEG Data & Analytics inputs

LSEG data are proprietary and require an institutional or individual subscription with the relevant content entitlements.

- Ask your institution's library, research-data service, or LSEG administrator whether you have access to [LSEG Workspace](https://www.lseg.com/en/data-analytics/products/workspace) and the required financial, ESG, returns, deals, and ownership content.
- The project retrieves data with the [LSEG Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/quick-start). A desktop session requires a valid Workspace login and the Workspace desktop application to be running; direct platform access requires separately issued platform credentials.
- Use `data/External/LSEG_variables_list_final.csv` as the list of financial and ESG variables to request.
- Run the relevant collection and validation cells to produce the files expected in `data/External/`, including:
  - `LSEG_variable_df_final.pkl`
  - `Monthly_Returns_with_Date.pkl`
  - `Ownership_top_20_investors.pkl`
  - `Ownership_measures_final.pkl`

If your account cannot retrieve a field, ask your LSEG administrator to confirm that the field is included in your license. LSEG source extracts must not be redistributed through this repository.

## ISS Incentive Lab data

ISS Incentive Lab is licensed data. This project uses the U.S. dataset and expects the raw tables `ParticipantFY.csv` and `SumComp.csv`.

1. Check whether your institution provides access through [Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/iss-esg/).
2. In WRDS, open the ISS data products and select **ISS Incentive Lab** (U.S.), then download/export the `ParticipantFY` and `SumComp` tables as CSV files. The original analysis used dataset version `20250201`; use that version when available, or document the newer snapshot used for replication.
3. Save the files as:
   - `data/External/ParticipantFY.csv`
   - `data/External/SumComp.csv`
4. Run the ISS section of `code/03_validation/Validation_Analyses_final.ipynb` to generate `data/External/ISS_CEO_Compensation_final.pkl`.

If ISS Incentive Lab is not listed in your WRDS account, contact your institutional WRDS representative, library, or data-services team to request entitlement. These files cannot be shared by the project maintainers unless the recipient has appropriate licensed access.

## DISCERN patent data

DISCERN is available from the project's public [Zenodo record](https://zenodo.org/records/13619821).

1. Open the Zenodo record and download DISCERN version **2.0.1**, which is the version used in the original analysis.
2. Extract or select these two files:
   - `discern_firm_panel_1980_2021.csv`
   - `Patent_Panel_Data_2015.csv`
3. Place them at:
   - `data/External/discern_firm_panel_1980_2021.csv`
   - `data/External/Patent_Panel_Data_2015.csv`
4. Run the DISCERN section of `code/03_validation/Validation_Analyses_final.ipynb`. It merges and filters the source tables and writes `data/External/DISCERN_2012_2021.pkl`.

If Zenodo publishes a newer version, use version 2.0.1 for exact replication or record the version and download date when deliberately updating the analysis.

## Local-data checklist

Before running the validation notebook, confirm that the required files exist under `data/External/` with the exact names and capitalization shown above. Keep provider documentation, license terms, dataset version numbers, and download dates with your replication records, but never commit credentials or restricted source data.
