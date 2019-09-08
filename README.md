# FastOnto
This code extracts individual ontology ids from snomed, Loinc and RxNorm for further ontological modelling
This code set is inspired and modified from quickumls by Luca soldni et al

steps to use this repository:
1) Install simstrings from Chokkan pip install simstring-pure
2) pip install leveldb numpy unidecode nltk spacy
3) Obtain a spacy corpus with python -m spacy download en
4) you must first obtain a license from the National Library of Medicine; then you should download all UMLS files.  For this project, we need loinc.csv and snomed.txt (specific information will e provided shortly) download a copy of snomed international version and under snomedCT_internationalrf2_production_<year>/Full/Terminology convert sct2_description_Full-en_int_<year>.txt to snomed.txt in the same folder of this download.
5) from loinc_2.61_text copy loinc.csv to the same folder of this download
