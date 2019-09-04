HEADERS_LOINC = ['LOINC_NUM','COMPONENT','PROPERTY','TIME_ASPCT','SYSTEM','SCALE_TYP','METHOD_TYP','CLASS','VersionLastChanged','CHNG_TYPE',
'DefinitionDescription','STATUS','CONSUMER_NAME','CLASSTYPE','FORMULA','SPECIES','EXMPL_ANSWERS','SURVEY_QUEST_TEXT','SURVEY_QUEST_SRC',
'UNITSREQUIRED','SUBMITTED_UNITS','RELATEDNAMES2','SHORTNAME','ORDER_OBS','CDISC_COMMON_TESTS','HL7_FIELD_SUBFIELD_ID','EXTERNAL_COPYRIGHT_NOTICE',
'EXAMPLE_UNITS','LONG_COMMON_NAME','UnitsAndRange','DOCUMENT_SECTION','EXAMPLE_UCUM_UNITS','EXAMPLE_SI_UCUM_UNITS','STATUS_REASON','STATUS_TEXT',
'CHANGE_REASON_PUBLIC','COMMON_TEST_RANK','COMMON_ORDER_RANK','COMMON_SI_TEST_RANK','HL7_ATTACHMENT_STRUCTURE','EXTERNAL_COPYRIGHT_LINK',
'PanelType','AskAtOrderEntry','AssociatedObservations','VersionFirstReleased','ValidHL7AttachmentRequest'
]
HEADERS_SNOMED = ['id','effectiveTime','active','moduleId','conceptId','languageCode','typeId','term','caseSignificanceId']
'''HEADERS_MRCONSO = [
    'cui', 'lat', 'ts', 'lui', 'stt', 'sui', 'ispref', 'aui', 'saui',
    'scui', 'sdui', 'sab', 'tty', 'code', 'str', 'srl', 'suppress', 'cvf'
]'''
HEADERS_MRSTY = [
    'cui', 'sty', 'hier' 'desc', 'sid', 'num'
]

NEGATIONS = {'none', 'non', 'neither', 'nor', 'no', 'not'}

ACCEPTED_SEMTYPES = {
    'T029',     # Body Location or Region
    'T023',     # Body Part, Organ, or Organ Component
    'T031',     # Body Substance
    'T060',     # Diagnostic Procedure
    'T047',     # Disease or Syndrome
    'T074',     # Medical Device
    'T200',     # Clinical Drug
    'T203',     # Drug Delivery Device
    'T033',     # Finding
    'T184',     # Sign or Symptom
    'T034',     # Laboratory or Test Result
    'T058',     # Health Care Activity
    'T059',     # Laboratory Procedure
    'T037',     # Injury or Poisoning
    'T061',     # Therapeutic or Preventive Procedure
    'T048',     # Mental or Behavioral Dysfunction
    'T046',     # Pathologic Function
    'T121',     # Pharmacologic Substance
    'T201',     # Clinical Attribute
    'T130',     # Indicator, Reagent, or Diagnostic Aid
    'T195',     # Antibiotic
    'T039',     # Physiologic Function
    'T040',     # Organism Function
    'T041',     # Mental Process
    'T170',     # Intellectual Product
    'T191'      # Neoplastic Process
}

UNICODE_DASHES = {
    u'\u002d', u'\u007e', u'\u00ad', u'\u058a', u'\u05be', u'\u1400',
    u'\u1806', u'\u2010', u'\u2011', u'\u2010', u'\u2012', u'\u2013',
    u'\u2014', u'\u2015', u'\u2053', u'\u207b', u'\u2212', u'\u208b',
    u'\u2212', u'\u2212', u'\u2e17', u'\u2e3a', u'\u2e3b', u'\u301c',
    u'\u3030', u'\u30a0', u'\ufe31', u'\ufe32', u'\ufe58', u'\ufe63',
    u'\uff0d'
}

# language with missing value
# will not have support for tokenization
LANGUAGES = {
    'BAQ': None,           # Basque
    'CHI': None,           # Chinese
    'CZE': None,           # Czech
    'DAN': 'danish',       # Danish
    'DUT': 'dutch',        # Dutch
    'ENG': 'english',      # English
    'EST': None,           # Estonian
    'FIN': 'finnish',      # Finnish
    'FRE': 'french',       # French
    'GER': 'german',       # German
    'GRE': 'greek',        # Greek
    'HEB': None,           # Hebrew
    'HUN': 'hungarian',    # Hungarian
    'ITA': 'italian',      # Italian
    'JPN': None,           # Japanese
    'KOR': None,           # Korean
    'LAV': None,           # Latvian
    'NOR': 'norwegian',    # Norwegian
    'POL': 'polish',       # Polish
    'POR': 'portoguese',   # Portuguese
    'RUS': 'russian',      # Russian
    'SCR': None,           # Croatian
    'SPA': 'spanish',      # Spanish
    'SWE': 'swedish',      # Swedish
    'TUR': 'turkish',      # Turkish
}

DOMAIN_SPECIFIC_STOPWORDS = {
    'time'
}

SPACY_LANGUAGE_MAP = {
    'ENG': 'en',
    'GER': 'de',
    'SPA': 'es',
    'POR': 'pt',
    'FRE': 'fr',
    'ITA': 'it',
    'DUT': 'nl',
    'XXX': 'xx'
}
