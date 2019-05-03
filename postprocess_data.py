# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.5
#   kernelspec:
#     display_name: altmetrics
#     language: python
#     name: altmetrics
# ---

import pandas as pd
from pathlib import Path

output_dir = Path("output/")

researchers = pd.read_csv(output_dir / "researchers.csv", index_col="id", dtype={'ID_number':str})
phds = pd.read_csv(output_dir / "phds.csv", index_col="id")
postdocs = pd.read_csv(output_dir / "postdocs.csv", index_col="id")

# combine all multiple PhDs
merged_phds = phds.groupby("rid")[['phd_institution','phd_institution_other','phd_year','phd_type']]
merged_phds = merged_phds.apply(lambda x: x.apply(lambda y: " | ".join([str(_) for _ in y])))

# combine all multiple postgrads
merged_postdocs = postdocs.groupby("rid")[['postdoc_year', 'postdoc_status', 'postdoc_institution']]
merged_postdocs = merged_postdocs.apply(lambda x: x.apply(lambda y: " | ".join([str(_) for _ in y])))

# merge all dataframes
researchers = researchers.merge(merged_phds, left_index=True, right_index=True, how="left")
researchers = researchers.merge(merged_postdocs, left_index=True, right_index=True, how="left")
researchers = researchers.rename(columns={'id':'rid'})

researchers.to_csv(output_dir / "researchers_phds_postdocs.csv")
