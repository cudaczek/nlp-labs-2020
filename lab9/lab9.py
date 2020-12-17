import json
import locale
import os
import pprint
import requests
import time

from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm
import xml.etree.ElementTree as et

data_path = "../data_lab1/"

# żeby możliwe było sortowanie alfabetyczne w języku polskim
locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")


# Sort bills according to their size and take top 50 (largest) bills.

def find_largest_files():
    largest_bills = set()
    min_len_in_largest = 0
    with tqdm(total=1179) as pbar:
        for filename in os.listdir(data_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(data_path, filename)
                content = open(filepath, 'r', encoding='utf-8').read().split()
                content = " ".join(content)
                content_size = len(content)
                if content_size > min_len_in_largest or len(largest_bills) < 50:
                    largest_bills.add((filename, len(content)))
                    min_len_in_largest = content_size
            pbar.update(1)

    largest_bills_sorted = list(sorted(largest_bills, key=lambda kv: kv[1], reverse=True))[:50]

    with open("largest_bills.json", "w") as file:
        json.dump(largest_bills_sorted, file)

    # print(len(largest_bills_sorted))

    top_50_bills = set(map(lambda kv: kv[0], largest_bills_sorted))
    return top_50_bills


top_50_bills = find_largest_files()

# Use the lemmatized and sentence split documents (from ex. 5) to identify the expressions that consist of
# consecutive words starting with a capital letter
# (you will have to look at the inflected form of the word to check its capitalization)
# that do not occupy the first position in a sentence.


user = "mojadresemail2"

url = "http://ws.clarin-pl.eu/nlprest2/base"


# kod na podstawie przykładu http://nlp.pwr.wroc.pl/redmine/projects/nlprest2/wiki/Python
def upload(file):
    with open(file, "rb") as myfile:
        doc = myfile.read()
    return requests.post(url + '/upload/', data=doc, headers={'Content-Type': 'binary/octet-stream'})


def process(data):
    doc = json.dumps(data)
    taskid = requests.post(url + '/startTask/', data=doc, headers={'Content-Type': 'application/json'}) \
        .content.decode('utf-8')
    time.sleep(0.2)
    resp = requests.get(url + '/getStatus/' + taskid).json()
    while resp["status"] == "QUEUE" or resp["status"] == "PROCESSING":
        time.sleep(0.5)
        resp = requests.get(url + '/getStatus/' + taskid).json()
    if resp["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return resp["value"]


def eval_files(bills, lpmn="any2txt|wcrft2", out_path='out/'):
    with tqdm(total=1179) as pbar:
        for filename in os.listdir(data_path):
            if filename.endswith(".txt") and filename in bills:
                filepath = os.path.join(data_path, filename)
                fileid = upload(filepath).content.decode("utf-8")
                # print("Processing: " + filename)
                data = {'lpmn': lpmn, 'user': user, 'file': fileid}
                data = process(data)
                if data is None:
                    continue
                data = data[0]["fileID"]
                content = requests.get(url + '/download' + data).content.decode('utf-8')
                with open(out_path + os.path.basename(filename) + '.ccl', "w", encoding='utf-8') as outfile:
                    outfile.write(content)
            pbar.update(1)


eval_files(top_50_bills)

# Compute the frequency of each identified expression and print 50 results with the largest number of occurrences.
def find_capitalised_expressions():
    counted_expressions = Counter({})
    out_path = 'out/'
    with tqdm(total=50) as pbar:
        for filename in os.listdir(out_path):
            if filename.endswith(".ccl"):
                filepath = os.path.join(out_path, filename)
                ccl_file = et.parse(filepath).getroot()
                for chunk in ccl_file:
                    for sentence in chunk:
                        word_in_sentence_no = 0
                        is_last_upper = False
                        expressions = []
                        for token in sentence:
                            if token.tag == 'tok':
                                real_text = token[0].text
                                text_tag = token[1][1].text
                                base = token[1][0].text
                                if word_in_sentence_no > 0 and real_text[0].isalpha() \
                                        and real_text[0].upper() == real_text[0]:
                                    if is_last_upper:
                                        expressions[-1] += " " + real_text
                                    else:
                                        expressions.append(real_text)
                                    is_last_upper = True
                                else:
                                    is_last_upper = False
                                word_in_sentence_no += 1
                    counted_expressions = counted_expressions + Counter(expressions)
            pbar.update(1)

    common_expressions = counted_expressions.most_common(50)
    pprint.pprint(common_expressions)
    return common_expressions


find_capitalised_expressions()
# [('Nr', 1266),
#  ('Art', 497),
#  ('U', 477),
#  ('Dz', 431),
#  ('Policji', 253),
#  ('Kodeksu', 217),
#  ('Skarbu Państwa', 127),
#  ('Rzeczypospolitej Polskiej', 107),
#  ('Polityki Socjalnej', 103),
#  ('Zakładu', 101),
#  ('Państwowej Straży Pożarnej', 100),
#  ('Zakład', 99),
#  ('Ministrów', 79),
#  ('Urząd Patentowy', 74),
#  ('Prawo', 57),
#  ('Funduszu Pracy', 57),
#  ('Minister Spraw Wewnętrznych', 53),
#  ('Straży Granicznej', 51),
#  ('Spraw Wewnętrznych', 51),
#  ('I', 49),
#  ('Sądu', 48),
#  ('Opieki Społecznej', 46),
#  ('Urzędu Patentowego', 45),
#  ('Państwa', 45),
#  ('Skarb Państwa', 44),
#  ('Rady Ministrów', 44),
#  ('Gospodarki Morskiej', 44),
#  ('Przepisy', 43),
#  ('Urzędzie Patentowym', 39),
#  ('Pracy', 37),
#  ('Minister', 37),
#  ('Polsce', 36),
#  ('Kodeks', 36),
#  ('Fundusz Pracy', 35),
#  ('Zakładu Ubezpieczeń Społecznych', 34),
#  ('Agencji', 34),
#  ('Finansów', 33),
#  ('II', 31),
#  ('Ministrem Finansów', 31),
#  ('Patentowy', 30),
#  ('Prezes Rady Ministrów', 30),
#  ('BGŻ SA', 30),
#  ('Pracodawca', 30),
#  ('FRD', 30),
#  ('Leśnictwa', 29),
#  ('Głównego Urzędu Statystycznego', 28),
#  ('ECU', 26),
#  ('Zasobów Naturalnych', 26),
#  ('FUS', 26),
#  ('Rady', 25)]


# Apply the NER algorithm to identify the named entities in the same set of documents (not lemmatized) using the n82 model.
# eval_files(top_50_bills, lpmn='any2txt|wcrft2|liner2({"model":"n82"})', out_path='out_n82/')

# Plot the frequency (histogram) of the coares-grained classes (e.g. nam_adj, nam_eve, nam_fac`).
def find_expressions_classes():
    out_path = 'out_n82/'
    result = dict()
    with tqdm(total=50) as pbar:
        for filename in os.listdir(out_path):
            if filename.endswith(".ccl"):
                filepath = os.path.join(out_path, filename)
                ccl_file = et.parse(filepath).getroot()
                for chunk in ccl_file:
                    for sentence in chunk:
                        sentence_stats = {}
                        expression = ""
                        for token in sentence:
                            if token.tag == 'tok':
                                for ann in token.findall("ann"):
                                    if ann.text != "0":
                                        ann_key = (ann.get("chan"), ann.text)
                                        word = token.find("orth").text
                                        values = sentence_stats.get(ann_key, [])
                                        values.append(word)
                                        sentence_stats[ann_key] = values
                        # print(sentence_stats)
                        for ann, expr in sentence_stats.items():
                            expression = " ".join(expr)
                            entity_name = ann[0]
                            val = result.get((entity_name, expression), 0)
                            result[(entity_name, expression)] = val + 1
            # print(result)
            pbar.update(1)
    return result


result = find_expressions_classes()


def plot_histogram(result):
    coares_grained_classes = dict()

    for key, val in result.items():
        coares_grained_class = "_".join(key[0].split("_")[:2])
        recent_val = coares_grained_classes.get(coares_grained_class, 0)
        coares_grained_classes[coares_grained_class] = recent_val + val

    print(coares_grained_classes)
    # {'nam_pro': 911,
    # 'nam_org': 2868,
    # 'nam_loc': 346,
    # 'nam_oth': 138,
    # 'nam_adj': 60,
    # 'nam_liv': 163,
    # 'nam_eve': 8,
    # 'nam_fac': 32}

    plt.figure(figsize=(10, 6))
    plt.title("Coarse-grained classes histogram")
    plt.bar(x=list(coares_grained_classes.keys()), height=list(coares_grained_classes.values()))
    plt.savefig("histogram.png")
    plt.show()


plot_histogram(result)

# Display 10 most frequent Named Entities for each coarse-grained type.

print(result)


def show_top_10_in_coarse_grained_classes(result):
    coarse_grained_classes = dict()

    for key, val in result.items():
        coarse_grained_class = "_".join(key[0].split("_")[:2])
        recent_val = coarse_grained_classes.get(coarse_grained_class, dict())
        recent_val.update({
            key[1]: val
        })
        coarse_grained_classes[coarse_grained_class] = recent_val
    # print(coarse_grained_classes)

    for key, val in coarse_grained_classes.items():
        print(f"------------- Top 10 for {key} -------------")
        sorted_elements = sorted(val.items(), key=lambda kv: kv[1], reverse=True)
        pprint.pprint(sorted_elements[:10])


# show_top_10_in_coarse_grained_classes(result)
# ------------- Top 10 for nam_pro -------------
# [('Dz . U .', 477),
#  ('Kodeksu postępowania administracyjnego', 19),
#  ('Kodeksu rodzinnego', 17),
#  ('Monitor Polski', 16),
#  ('Kodeksu karnego', 16),
#  ('Kodeksu postępowania karnego', 15),
#  ('Ordynacja podatkowa', 12),
#  ('Kodeksu karnego wykonawczego', 11),
#  ('Kodeksu postępowania cywilnego', 10),
#  ('Kodeksu cywilnego', 7)]
# ------------- Top 10 for nam_org -------------
# [('Skarbu Państwa', 134),
#  ('Urząd Patentowy', 104),
#  ('Rada Ministrów', 93),
#  ('Minister Spraw Wewnętrznych', 83),
#  ('Prezes Rady Ministrów', 61),
#  ('Funduszu Pracy', 54),
#  ('Skarb Państwa', 44),
#  ('Urzędu Patentowego', 41),
#  ('Urzędzie Patentowym', 36),
#  ('Minister Finansów', 35)]
# ------------- Top 10 for nam_loc -------------
# [('Rzeczypospolitej Polskiej', 143),
#  ('Polsce', 36),
#  ('Warszawie', 12),
#  ('Warszawy', 11),
#  ('Warszawa', 11),
#  ('Polski', 8),
#  ('Straż Graniczną', 7),
#  ('Rzeczpospolita Polska', 6),
#  ('Poznaniu', 6),
#  ('Wrocławiu', 6)]
# ------------- Top 10 for nam_oth -------------
# [('złotych', 63),
#  ('zł', 31),
#  ('ECU', 13),
#  ('Minister Edukacji Narodowej', 11),
#  ('Minister Spraw Wewnętrznych', 5),
#  ('PESEL', 3),
#  ('Ă - - - - - Ĺ - - - - - - - - - - - - - - - - - - - Ĺ - - - - - - - - - - - - - - - - - - - - - - - -', 2),
#  ('FUS', 2),
#  ('É - - - - - Â - - - - - - - - - - - - - - - - - - - Â - - - - - - - - - - - - - - - - - - - - - - - -', 1),
#  ('Č - - - - - Á - - - - - - - - - - - - - - - - - - - Á - - - - - - - - - - - - - - - - - - - - - - - -', 1)]
# ------------- Top 10 for nam_adj -------------
# [('polski', 22),
#  ('polskich', 9),
#  ('polskiej', 4),
#  ('polskim', 4),
#  ('polskiego', 3),
#  ('Polskiej', 2),
#  ('polską', 2),
#  ('polscy', 2),
#  ('polskimi', 2),
#  ('Wojewódzki', 2)]
# ------------- Top 10 for nam_liv -------------
# [('Gospodarki Morskiej', 39),
#  ('Straży Granicznej', 11),
#  ('Głównego Inspektora', 10),
#  ('Art', 8),
#  ('Głównym Inspektorem', 5),
#  ('Kartograficznym', 4),
#  ('III', 4),
#  ('Główny Lekarz Weterynarii', 4),
#  ('Karta Nauczyciela', 3),
#  ('Najwyższego', 3)]
# ------------- Top 10 for nam_eve -------------
# [('BGŻ SA', 2),
#  ('Monitorze Sądowym', 2),
#  ('Narodowego Spisu Powszechnego', 1),
#  ('Świętem Straży Granicznej', 1),
#  ('Generalny Konserwator Zabytków', 1),
#  ('Ochrony Roślin', 1)]
# ------------- Top 10 for nam_fac -------------
# [('Komendant Główny', 16),
#  ('Straży Granicznej', 5),
#  ('NIP', 2),
#  ('Centralnym Muzeum Pożarnictwa', 2),
#  ('Kościoła Ewangelicko - Reformowanego', 1),
#  ('Obrony Narodowej', 1),
#  ('REGON', 1),
#  ('Zakładu', 1),
#  ('Muzeum Pożarnictwa', 1),
#  ('Kościoła Ewangelicko - Metodystycznego', 1)]

# Display 50 most frequent Named Entities including their count and fine-grained type.

sorted_results = sorted(result.items(), key=lambda kv: -kv[1])
pprint.pprint(sorted_results[:50])
# [(('nam_pro_media_periodic', 'Dz . U .'), 477),
#  (('nam_loc_gpe_country', 'Rzeczypospolitej Polskiej'), 143),
#  (('nam_org_institution', 'Skarbu Państwa'), 134),
#  (('nam_org_institution', 'Urząd Patentowy'), 104),
#  (('nam_org_organization', 'Państwowej Straży Pożarnej'), 96),
#  (('nam_org_institution', 'Rada Ministrów'), 93),
#  (('nam_org_institution', 'Minister Spraw Wewnętrznych'), 83),
#  (('nam_oth_currency', 'złotych'), 63),
#  (('nam_org_institution', 'Prezes Rady Ministrów'), 61),
#  (('nam_org_institution', 'Funduszu Pracy'), 54),
#  (('nam_org_institution', 'Skarb Państwa'), 44),
#  (('nam_org_institution', 'Urzędu Patentowego'), 41),
#  (('nam_liv_person', 'Gospodarki Morskiej'), 39),
#  (('nam_org_institution', 'Urzędzie Patentowym'), 36),
#  (('nam_loc_gpe_country', 'Polsce'), 36),
#  (('nam_org_institution', 'Minister Finansów'), 35),
#  (('nam_org_institution', 'Zakładu Ubezpieczeń Społecznych'), 35),
#  (('nam_org_institution', 'Minister Pracy i Polityki Socjalnej'), 33),
#  (('nam_org_institution', 'Fundusz Pracy'), 33),
#  (('nam_oth_currency', 'zł'), 31),
#  (('nam_org_institution', 'Zakład Ubezpieczeń Społecznych'), 30),
#  (('nam_org_institution', 'Ministrem Finansów'), 29),
#  (('nam_org_institution', 'Minister Zdrowia i Opieki Społecznej'), 27),
#  (('nam_org_institution', 'Ministrem Pracy i Polityki Socjalnej'), 25),
#  (('nam_org_institution', 'Prezesa Rady Ministrów'), 24),
#  (('nam_org_institution', 'Prezesa Narodowego Banku Polskiego'), 23),
#  (('nam_org_institution', 'Ministra Spraw Wewnętrznych'), 23),
#  (('nam_adj_country', 'polski'), 22),
#  (('nam_org_institution', 'Urzędu Ochrony Państwa'), 22),
#  (('nam_org_institution', 'Prezes Urzędu'), 21),
#  (('nam_org_institution', 'Agencji'), 21),
#  (('nam_org_institution', 'Prezes Urzędu Patentowego'), 19),
#  (('nam_org_institution', 'Prezesa Urzędu Patentowego'), 19),
#  (('nam_pro_title_document', 'Kodeksu postępowania administracyjnego'), 19),
#  (('nam_org_institution', 'Minister Transportu i Gospodarki Morskiej'), 19),
#  (('nam_org_institution', 'Zakładu'), 19),
#  (('nam_org_institution', 'Prezes Głównego Urzędu Statystycznego'), 18),
#  (('nam_org_institution', 'Banku Gospodarki Żywnościowej'), 18),
#  (('nam_org_institution', 'Główny Urząd Statystyczny'), 18),
#  (('nam_org_institution', 'Straży Granicznej'), 17),
#  (('nam_pro_title_document', 'Kodeksu rodzinnego'), 17),
#  (('nam_org_institution', 'Komendanta Głównego Policji'), 17),
#  (('nam_pro_title', 'Monitor Polski'), 16),
#  (('nam_org_company', 'BGŻ SA'), 16),
#  (('nam_pro_title_document', 'Kodeksu karnego'), 16),
#  (('nam_fac_goe', 'Komendant Główny'), 16),
#  (('nam_org_institution', 'Ministra Finansów'), 15),
#  (('nam_org_institution', 'Prezesa Głównego Urzędu Statystycznego'), 15),
#  (('nam_org_institution', 'Państwowej Straży Pożarnej'), 15),
#  (('nam_pro_title_document', 'Kodeksu postępowania karnego'), 15)]
