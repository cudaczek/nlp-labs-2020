import json
import pprint

from tqdm import tqdm
from elasticsearch import Elasticsearch


## Load Morfologik to ElasticSearch (one document for each form)
# and use fuzzy matching to obtain the possible corrections of the 30 words with 5 occurrences that do not belong to the dictionary.

es_url = 'http://localhost:9200'  # default path to working es sevice
index_name = 'my_index_lab3'

polimorfix = './polimorfologik-2.1/polimorfologik-2.1.txt'
content = open(polimorfix, 'r', encoding='utf-8').read().split("\n")
morfologic_dict = [(c.split(";")[1]).lower() for c in content]

# %% ES index for storing acts, ES analyzer for Polish texts:
es = Elasticsearch()


def create_my_index():
    response = es.indices.create(
        index=index_name,
        body={
            "settings": {
                "analysis": {
                    "analyzer": {
                        "analyzer_lab3": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "morfologik_stem",
                                "stop"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "token": {
                        "type": "text",
                        "analyzer": "analyzer_lab3"
                    }
                }
            }
        })

    print(response)


# create_my_index()

body = []

# Indeksuję zawartość słownika morfologik do es
def bulk_indexing():
    with tqdm(total=len(morfologic_dict)) as pbar:
        for entry in morfologic_dict:
            body.append(({'index': {}}))
            body.append({"token": entry})
            pbar.update(1)
            if pbar.n % 10000 == 0:
                response = es.bulk(index=index_name, doc_type='_doc', body=body)
                print(response)
                body = []


# bulk_indexing()

with open("words_not_in_dict_2.json", 'r', encoding='utf-8') as json_file:
    words_not_in_dict = list(json.load(json_file)["words"])

## Find 30 words with 5 occurrences that do not belong to the dictionary.
print("30 words that do not appear in polimorfologik with 5 occurrences")
words_not_in_dict_with_5_occ = list(filter(lambda x: list(x.items())[0][1] == 5, words_not_in_dict))[:30]
pprint.pprint(words_not_in_dict_with_5_occ)

words_not_in_dict_with_5_occ = {k: v for element in words_not_in_dict_with_5_occ for k, v in element.items()}
for key, value in words_not_in_dict_with_5_occ.items():
    print("Looking for correction of '%s'..." % key)
    query = {
        "query": {
            "fuzzy": {
                "token": {
                    "value": key,
                    "fuzziness": "AUTO"
                    # zalecane jest wybranie fuzziness=AUTO
                }
            }
        }
    }

    response = es.search(
        index=index_name,
        doc_type="_doc",
        body=query
    )["hits"]
    if response['total']['value'] == 0:
        print("No correction found :( ")
    else:
        pprint.pprint(response['hits'][0])
    # print(response)

## Compare the results. Draw conclusions regarding:
# - the distribution of words in the corpus,
# - the number of true misspellings vs.the number of unknown words,
# - the performance of your method compared to ElasitcSearch,
# - the results provided by your method compared to ElasticSearch,
# - the validity of the obtained corrections.
