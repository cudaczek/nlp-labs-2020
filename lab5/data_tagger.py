import json
import os

import requests
from tqdm import tqdm

data_path = "../data_lab1/"

# Use the tool to tag and lemmatize the law corpus.

tagger_server = "http://localhost:9200"

with tqdm(total=1179) as pbar:
    tagged_files = dict()
    for filename in os.listdir(data_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_path, filename)
            content = open(filepath, 'r', encoding='utf-8').read().split()
            content = " ".join(content).lower()  # małe litery

            r = requests.post(tagger_server, data=content.encode("utf-8"))
            lines = r.content.decode("utf-8").split("\n")
            file_tags = []
            lines_iter = 0
            while lines_iter < len(lines):
                if lines[lines_iter] == "" or lines_iter + 1 == len(lines):
                    lines_iter += 1
                    continue
                tag_info = lines[lines_iter + 1].split()
                file_tags.append((tag_info[0], tag_info[1]))
                lines_iter += 2
            tagged_files.update({filename: file_tags})
        pbar.update(1)
with open("data/taggedfile0.json", "w") as file:
    json.dump(tagged_files, file)
