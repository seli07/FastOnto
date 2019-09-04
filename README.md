# FastOnto
This code extracts individual ontology ids from snomed, Loinc and RxNorm for further ontological modelling
This code set is inspired and modified from quickumls by Luca soldni et al

steps to use this repository:
1) Install simstrings from Chokkan pip install simstring-pure
2) pip install leveldb numpy unidecode nltk spacy
3) Obtain a spacy corpus with python -m spacy download en
4) you must first obtain a license from the National Library of Medicine; then you should download all UMLS files.  For this project, we need loinc.csv and snomed.txt (specific information will e provided shortly)
