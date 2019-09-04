###usage python main_implement.py########


import spacy
nlp = spacy.load('en')
import sys
sys.path.append('/home/selineni/Desktop/new_quickSOLOR_extract_final')
from main import SOLOR
tagger = SOLOR('/home/selineni/Desktop/new_quickSOLOR_extract_final/output')
text = "878 nsg adm note ms. [**known patient lastname 3763**] is a 52yo woman who was adm to micu for bs control on insulin drip. pmh:iddmx20yrs, cva[**27**],breast ca with mastectomy 89. pt had a mva [**11-22**]: s/p sah(frontal&intracranial bleeds), left occipital non displaced fx, lower back pain, compression fx. pt was cleared to go home on [**11-27**]but returned <24hrs due to poor po intake,increased lethargy and ? failure to thrive. she was adm to the [**hospital ward name **] 5. this am, her bs was up trial name 300 and than Age at menopause her bicarb was found to be 10. she was started on iv insulin.than was also found to have access issues. she cont to have poor po intake with some nausea. she was transfered for bs control on iv insulin all:contrast dye, shell fish meds:insulin, reglan, dilaudid micu adm course: endo:the ho placed a left ej piv-pt & husband very cautious about further invasive therapy- she was quickly given 2l ivf and insuliln drip started at 2u/hr. bs up to 400 and insulin drip titrated to get bs down and dka corrected. access: [**last name **] problem. discussion around need for central access addressed with pt and husband by the house staff and attending. ultimately we will cont with piv as we rehydrate her and try to draw blood. if unable, we will readdress the issue as needed. gi:s she is sl nauseous, give zofran and she is able to tol water. gu: voids on own, able to stand, ua sent cv: vss, k 4.6, phos down and will be repleted resp: clr neuro: pt is a&ox3, mae and Memory impairment is currentl without pain. she is c/o Trial name photosensitivity but no ha. the back of her head hurts from her injuries. she can converse without difficulty but wants to [**doctor last name 65**] alot. a/p: will adjust insulin as dka clears, drawn blood as needed and able asses for pain meds replace lytes as needed.d nuero: alert and oreinted when given time to wake. moves all extremitiesoob to comode with minimal assistance. pt slept most of night c/o light and noise cause her discomfort; but denied ha. cv : nsr no ectopi vss. palp dp/pt skin warm/dry. r ej only iv fluid given through out nightsee flow sheet. insulin drip @ 3u most of night. k repleating up to 4.2 ;will monitor closely. pt unable to take 4am dose of k-phos d/t nausea. discussed with pharmacy and intern, 15mmol add to d5ns @ 150. kcl capsule givenfor repletion klor upset pt stomach. third dose of kcl not given d/t nausea. lungs:bs clear in all fields. gi : abd soft. bs present. some nausea from k-phose and kcl gu : voids clear yellow urine. u/a pending. skin :dry and intact a stable. dka resolving. r continue to monitorblood glucose, lytes,phos. continue fld as ordered. repleat k-phos i"
#print(text)
data=[]
ontology=['loinc','snomed']
for i in ontology:
    matches= tagger.match(text, i,best_match=True, ignore_syntax=False)

    stpwds = set()
    #doc = nlp(str(text,'utf-8'))
    doc =  nlp(text)
    for token in doc:
        if token.is_stop:
            stpwds.add(token.idx)

    import pandas as pd
    tagged = {}
    #data = []
    print(matches)
    for match in matches:
    #     print match
        #semtypes = set()
        term = ''
        id = ''
        ngram = ''
        mi=0
        for m in match:

            if m['similarity']>mi:
                term = m['term']
                id = m['id']
                mi=m['similarity']
                ngram = m['ngram']
        if len(term)<=2:
            continue
        if match[0]['start'] in stpwds:
            continue
        tmp=[]
        tmp.append(match[0]['start'])
        #print(tmp)
        tmp.append(match[0]['end'])
        #print(tmp)
        tmp.append(term)
        #print(tmp)
        tmp.append(id)
        #print(tmp)
    #     tmp.append(ngram)
    #     tmp.append(match[0]['preferred'])
        tmp.append(mi)
        #stypes = set()
        data.append(tmp)

        df_matches = pd.DataFrame(data=data, columns =['start','end','term','id','similarity'])
#print(df_matches)
        df_matches.to_csv('%s_out.csv'%i)
        #print(df_matches["term"])
