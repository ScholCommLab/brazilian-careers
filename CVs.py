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
from pprint import pprint
from pathlib import Path
import pandas as pd
from tqdm import tqdm_notebook as tqdm

data = Path("sample")
files = list(data.glob("*.xml"))

# +
persons_columns = ['ID', 'Fullname', 'Nationality', 'CountryOfBirth', 'CityOfBirth']
persons = pd.DataFrame(columns=persons_columns)

pub_columns = ['personID', 'DOI', 'title', 'year', 'journal', 'ISSN']
publications = pd.DataFrame(columns=pub_columns)

degree_columns = ['personID', 'tag', 'started', 'finished', 'code1', 'code2', 'type_of_phd', 'institute']
degrees = pd.DataFrame(columns=degree_columns)
# -

for f in tqdm(files[0:100]):
    try:
        root = ET.parse(str(f)).getroot()
    except:
        print("Couldn't read '{}' | Skipping".format(f.name))
        continue
    
    # General data
    data_node = root.find("DADOS-GERAIS")
    
    person_id = root.get('NUMERO-IDENTIFICADOR')
    full_name = data_node.get('NOME-COMPLETO')
    city_of_birth = data_node.get('CIDADE-NASCIMENTO')
    country_of_birth = data_node.get('PAIS-DE-NASCIMENTO')
    nationality = data_node.get('PAIS-DE-NACIONALIDADE')
    
    row = [person_id, full_name, nationality, country_of_birth, city_of_birth]
    persons.loc[len(persons)+1] = row
    
    # Education
    edu_node = data_node.find("FORMACAO-ACADEMICA-TITULACAO")

    for degree_tag in ["DOUTORADO", "POS-DOUTORADO"]:
        node = edu_node.find(degree_tag)
        
        if not node:
            continue

        inst = node.get("NOME-INSTITUICAO")
        started = node.get("ANO-DE-INICIO")
        finished = node.get("ANO-DE-CONCLUSAO")
        code_1 = node.get("CODIGO-INSTITUICAO-SANDUICHE")
        code_2 = node.get("CODIGO-INSTITUICAO-CO-TUTELA")
        type_of_phd = node.get("TIPO-DOUTORADO")

        row = [person_id, degree_tag, started, finished, code_1, code_2, type_of_phd, inst]
        degrees.loc[len(degrees)+1] = row
            
    # Publications
    articles = root.find("PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS")
    
    if not articles:
        continue
        
    for article in articles:
        basics = article.find("DADOS-BASICOS-DO-ARTIGO")
        details = article.find("DETALHAMENTO-DO-ARTIGO")
        
        doi = basics.find("DOI")
        year = basics.get("ANO-DO-ARTIGO")
        title = basics.get("TITULO-DO-ARTIGO")
        
        journal = details.get("TITULO-DO-PERIODICO-OU-REVISTA")
        issn = details.get("ISSN")
        
        row = [person_id, doi, year, title, journal, issn]
        publications.loc[len(publications)+1] = row

persons.sample(20)

degrees.sample(20)

publications.journal.unique()

# +
# Export
