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

import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from pprint import pprint
from random import shuffle

import pandas as pd

try:
    get_ipython
    from tqdm import tqdm_notebook as tqdm
except:
    from tqdm import tqdm

# +
input_dir = Path("input/cvs")
output_dir = Path("output/")

files = list(input_dir.glob("*.xml"))

xml_tags = pd.read_csv("input/xml_tags.csv", sep=";", index_col="field_name")

phd_xpath = "DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO"
postdoc_xpath = "DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/POS-DOUTORADO"
publication_xpath = "PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO"


# -

tables_fields = xml_tags.reset_index().groupby("file").field_name.unique().to_dict()

# +
sample_size = 100

r_file = open(str(output_dir / "researchers.csv"), "w")
researchers = csv.writer(r_file, delimiter=',')
researchers.writerow(["id"] + list(tables_fields['researcher']) + ["n_phds", "n_postdocs", "n_articles"])

phd_file = open(str(output_dir / "phds.csv"), "w")
phds = csv.writer(phd_file, delimiter=',')
phds.writerow(["id", "rid"] + list(tables_fields['phd']))

postdoc_file = open(str(output_dir / "postdocs.csv"), "w")
postdocs = csv.writer(postdoc_file, delimiter=',')
postdocs.writerow(["id", "rid"] + list(tables_fields['postdoc']))

p_file = open(str(output_dir / "publications.csv"), "w")
publications = csv.writer(p_file, delimiter=',')
publications.writerow(["id", "rid"] + list(tables_fields['publication']))

failed_files = 1
logfile =  open("log.txt", "w")

r_id = 0
pub_id = 0
phd_id = 0
postdoc_id = 0

shuffle(files)
for f in tqdm(files[0:sample_size]):
    try:
        root = ET.parse(str(f)).getroot()
    except:
        logfile.write("{}: Couldn't read '{}'\n".format(failed_files, f.name))
        failed_files = failed_files + 1
        continue
    
    ### Researcher
    researcher_row = []
    researcher_row.append(r_id)
    for field in tables_fields['researcher']:
        tag = xml_tags.loc[field].parent_tag
        attr = xml_tags.loc[field].attribute
        if tag == "CURRICULO-VITAE":
            val = root.get(attr)
        else:
            node = root.find(tag)
            if node is not None:
                val = node.get(attr)
            else:
                val = None
        researcher_row.append(val)
    
    
    ### PhDs
    list_phds = root.findall(phd_xpath)
    researcher_row.append(len(list_phds))
    
    for phd_node in list_phds:
        row = []
        row.append(phd_id)
        row.append(r_id)
        for field in tables_fields['phd']:
            attr = xml_tags.loc[field].attribute
            val = phd_node.get(attr)
            row.append(val)
        phd_id = phd_id + 1
        phds.writerow(row)

    ### PostDocs
    list_postdocs = root.findall(postdoc_xpath)
    researcher_row.append(len(root.findall(postdoc_xpath)))
    
    for postdoc_node in root.findall(postdoc_xpath):
        row = []
        row.append(postdoc_id)
        row.append(r_id)
        for field in tables_fields['postdoc']:
            attr = xml_tags.loc[field].attribute
            val = phd_node.get(attr)
            row.append(val)
        postdoc_id = postdoc_id + 1
        postdocs.writerow(row)
    
    
    ### Publications
    list_publications = root.findall(publication_xpath)
    researcher_row.append(len(list_publications))
    for pub_node in list_publications:
        row = []
        row.append(pub_id)
        row.append(r_id)
        for field in tables_fields['publication']:
            subtag = xml_tags.loc[field].field_tag
            attr = xml_tags.loc[field].attribute
            
            node = pub_node.find(subtag)
            if node is not None:
                val = node.get(attr)
            else:
                val = None
                
            row.append(val)
        pub_id = pub_id + 1
        publications.writerow(row)
    
    researchers.writerow(researcher_row)
    r_id = r_id + 1
    
### Close file streams
logfile.close()

r_file.close()
p_file.close()
phd_file.close()
postdoc_file.close()
