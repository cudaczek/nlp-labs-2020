from collections import Counter

import requests
from tqdm import tqdm

import xml.etree.ElementTree as et

import json
import os
import time
import pprint

data_path = "../data_lab1/"


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


# eval_files(top_50_bills)

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

# find_capitalised_expressions()
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
eval_files(top_50_bills, lpmn='any2txt|wcrft2|liner2({"model":"n82"})', out_path='out_n82/')
