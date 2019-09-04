from __future__ import unicode_literals, division, print_function

# built in modules
import os
import sys
import time
import codecs
import shutil
import argparse
from six.moves import input

# project modules
from tools import countlines, IDDB, SimstringDBWriter, mkdir
from load import HEADERS_LOINC, HEADERS_SNOMED, LANGUAGES

def get_ont_iterator(path, headers,check, lang='ENG'):
    with codecs.open(path, encoding='utf-8') as f:
        for i, ln in enumerate(f):
            if check == 'loinc':
                content = dict(zip(headers, ln.strip().split(',')))
            elif check == 'snomed':
                content = dict(zip(headers, ln.strip().split('	')))
            else:
                print('enter a valid ontology')

            yield content


def extract_from_ont(ont_path,arg,header_loinc=HEADERS_LOINC,header_snomed=HEADERS_SNOMED):
    start = time.time()

    if arg.ontology == 'loinc':
        header = header_loinc
    elif arg.ontology == 'snomed':
        header = header_snomed
    else:
        print('enter a valid ontology')

    ont_extract = get_ont_iterator(ont_path,header,arg.ontology,arg.language)

    total = countlines(ont_path) # i need to add this in tools

    processed = set()
    i=0
    for content in ont_extract:
        i += 1
        if i % 100000 == 0:
            delta = time.time() - start
            status = (
                '{:,} in {:.2f} s ({:.2%}, {:.1e} s / term)'
                ''.format(i, delta, i / total, delta / i if i > 0 else 0)
            )
            print(status)

        if arg.ontology == 'loinc':
            concept_text = content['COMPONENT'].strip()
            id = content['LOINC_NUM']
        elif arg.ontology == 'snomed':
            concept_text = content['term'].strip()
            id = content['id']
        else:
            print('enter a valid ontology')

        if arg.lowercase:
            concept_text = concept_text.lower()

        if arg.normalize_unicode:
            concept_text = unidecode(concept_text)

        if (id, concept_text) in processed:
            continue
        else:
            processed.add((id, concept_text))

        yield (concept_text, id)# change this accordingly concept_text and id are imp

    '''delta = time.time() - start
    status = (
        '\nCOMPLETED: {:,} in {:.2f} s ({:.1e, is_preferred} s / term)'
        ''.format(i, delta, i / total, delta / i if i > 0 else 0)
    )
    print(status)'''

def parse_and_encode_ngrams(extracted_it, simstring_dir, ids_dir,arg):#check and modyfy
    # Create destination directories for the two databases
    mkdir(simstring_dir)
    mkdir(ids_dir)

    ss_db = SimstringDBWriter(simstring_dir,arg) # here added arg and going to tools
    ids_db = IDDB(ids_dir)

    simstring_terms = set()

    for i, (term, id) in enumerate(extracted_it, start=1):
        if term not in simstring_terms:
            ss_db.insert(term)
            simstring_terms.add(term)

        ids_db.insert(term, id) #comeback to here after reviewing main program

def sender(arg):
    if not os.path.exists(arg.destination_path):
        msg = ('Directory "{}" does not exists; should I create it? [y/N] '
               ''.format(arg.destination_path))
        create = input(msg).lower().strip() == 'y'

        if create:
            os.makedirs(arg.destination_path)
        else:
            print('Aborting.')
            exit(1)

    if len(os.listdir(arg.destination_path)) > 0:
        msg = ('Directory "{}" is not empty; should I empty it? [y/N] '
               ''.format(arg.destination_path))
        empty = input(msg).lower().strip() == 'y'
        if empty:
            shutil.rmtree(arg.destination_path)
            os.mkdir(arg.destination_path)
        else:
            print('Aborting.')
            exit(1)

    if arg.normalize_unicode:
        try:
            unidecode
        except NameError:
            err = ('`unidecode` is needed for unicode normalization'
                   'please install it via the `[sudo] pip install '
                   'unidecode` command.')
            print(err, file=sys.stderr)
            exit(1)

        flag_fp = os.path.join(arg.destination_path, 'normalize-unicode.flag')
        open(flag_fp, 'w').close()

    if arg.lowercase:
        flag_fp = os.path.join(arg.destination_path, 'lowercase.flag')
        open(flag_fp, 'w').close()

    flag_fp = os.path.join(arg.destination_path, 'language.flag')
    with open(flag_fp, 'w') as f:
        f.write(arg.language)


    if arg.ontology == 'loinc':
        pa = 'loinc.csv'
        ids_dir='loinc_ids_dir'
    elif arg.ontology == 'snomed':
        pa = 'snomed.txt'
        ids_dir='snomed_ids_dir'

    ont_path = os.path.join(arg.installation_path, pa)
    ont_iterator = extract_from_ont(ont_path,arg)#need to create this Function

    simstring_dir = os.path.join(arg.destination_path, '%s-simstring.db'%(arg.ontology))#loinc-simstring.db change to the name of db that we look
    #print(simstring_dir)
    ids_dir = os.path.join(arg.destination_path, '%sids.db'%(arg.ontology))

    parse_and_encode_ngrams(ont_iterator, simstring_dir, ids_dir,arg)

############################################################################################
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument(
        'installation_path',
        help=('Location of UMLS installation files (`MRCONSO.RRF` and '
              '`MRSTY.RRF` files)')
    )
    ap.add_argument(
        'destination_path',
        help='Location where the necessary QuickUMLS files are installed'
    )
    ap.add_argument(
        '-L', '--lowercase', action='store_true',
        help='Consider only lowercase version of tokens'
    )
    ap.add_argument(
        '-U', '--normalize-unicode', action='store_true',
        help='Normalize unicode strings to their closest ASCII representation'
    )
    ap.add_argument(
        '-E', '--language', default='ENG', choices=LANGUAGES,
        help='Extract concepts of the specified language'
    )
    ap.add_argument(
        '-O', '--ontology', default='loinc',
        help='Extract concepts of the specified ontology'
    )
    arg = ap.parse_args()

sender(arg)
