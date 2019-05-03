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

# # Postprocessing
# - merge researchers with phds/postdocs

import pandas as pd
from pathlib import Path

output_dir = Path("output/")

researchers = pd.read_csv(output_dir / "researchers.csv", index="id", dtype={'ID_number':str})
phds = pd.read_csv(output_dir / "phds.csv", index_col="id")
postdocs = pd.read_csv(output_dir / "postdocs.csv", index_col="id")
publications = pd.read_csv(output_dir / "publications.csv", index_col="id")

merged_phds = phds.groupby("rid")[['phd_institution','phd_institution_other','phd_year','phd_type']]
merged_phds = merged_phds.apply(lambda x: x.apply(lambda y: " | ".join([str(_) for _ in y])))

merged_postdocs = postdocs.groupby("rid")[['postdoc_year', 'postdoc_status', 'postdoc_institution']]
merged_postdocs = merged_postdocs.apply(lambda x: x.apply(lambda y: " | ".join([str(_) for _ in y])))

a = researchers.merge(merged_phds, left_index=True, right_index=True, how="left")
b = a.merge(merged_postdocs, left_index=True, right_index=True, how="left")
b = b.rename(columns={'id':'rid'})

b.to_csv("output/researchers_phds_postdocs.csv")
