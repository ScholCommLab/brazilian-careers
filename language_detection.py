# -*- coding: utf-8 -*-
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

# +
import csv

import langdetect 
from langdetect import DetectorFactory
from tqdm import tqdm
import pandas as pd

# +
DetectorFactory.seed = 0

lang_map = {
    'Inglês': 'en',
    'Português': 'pt',
    'Espanhol': 'es',
    'Francês': 'fr',
    'Árabe': 'ar'
}

# +
with open("output/publications.csv", "r") as temp:
    numlines = len(temp.readlines())

input_file = open("output/publications.csv", "r")
input_reader = csv.DictReader(input_file, delimiter=',')

output_file = open("output/detected_languages.csv", "w")
csv_writer = csv.writer(output_file)
csv_writer.writerow(['id', 'article_language', 'article_title', 'detected_lang', 'lang_mapping']);
# -

for line in tqdm(input_reader, total=numlines):
    pid = line['id']
    article_language = line['article_language']
    article_title = line['article_title']
    
    detected_lang = langdetect.detect(article_title)
    
    if article_language in lang_map:
        mapped_lang = lang_map[article_language]
    else:
        mapped_lang = None
    
    csv_writer.writerow([pid, article_language, article_title, detected_lang, mapped_lang])

input_file.close()
output_file.close()

pubs = pd.read_csv("output/detected_languages.csv", index_col="id")
pubs.head()

# +
x = pubs['lang_mapping'] == pubs['detected_lang']
y = 100 * x.sum() / len(x)

print("Matching languages: {:.1f}%".format(y))
