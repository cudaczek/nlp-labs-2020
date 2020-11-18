import json
import pprint
import os
from collections import Counter

from tqdm import tqdm

from lab4.helpers import llr_2x2

data_path = "data/"


# Using the tagged corpus compute bigram statistic for the tokens containing:
#   lemmatized, downcased word
#   morphosyntactic category of the word (subst, fin, adj, etc.)
def get_n_grams(n, tokens):
    file_result = []
    for token in tokens:
        word = token[0]
        category = token[1].split(":")[0]
        file_result.append((word, category))
    return [tuple(file_result[i:i + n]) for i in range(len(tokens) - n + 1)]


def is_alpha(k):
    words = k
    for word in words:
        if not word[0].isalpha():
            return False
    return True


aggregated_results = Counter({})
with tqdm(total=1179) as pbar:
    for filename in os.listdir(data_path):
        if filename == "taggedfile0.json":
            filepath = os.path.join(data_path, filename)
            with open(filepath, 'r', encoding='utf-8') as fp:
                tagged_files = json.load(fp=fp)
                for key, val in tagged_files.items():
                    ngrams = get_n_grams(2, val)
                    aggregated_results = aggregated_results + Counter(ngrams)
                    pbar.update(1)

# Discard bigrams containing characters other than letters.
# Make sure that you discard the invalid entries after computing the bigram counts.

bigrams_dict = {k: v for k, v in aggregated_results.items() if is_alpha(k)}
all_bigrams = sum(bigrams_dict.values())


# Zapisanie na wypadek, gdyby trzeba było powtarzać => szybszy dostęp
def make_str(tuplaa):
    a = tuplaa[0]
    b = tuplaa[1]
    return a[0] + ":" + a[1] + " " + b[0] + ":" + b[1]


bigrams_dict_to_save = {make_str(k): v for k, v in aggregated_results.items() if is_alpha(k)}
with open("bigrams.json", 'w', encoding='utf-8') as f:
    json.dump(bigrams_dict_to_save, f)


# Compute LLR statistic for this dataset.


def llr_measure_bigrams():
    # zapisuję bigramy do przeszukania w setach
    # przeszukiwanie każdorazowo całego słownika grozi wysoką złożonością czasową - odczyt jest szybszy
    # saving to sets for computational complexity purpose
    first_words_in_bigrams = {}
    second_words_in_bigrams = {}

    with tqdm(total=len(bigrams_dict)) as pbar:
        for bigram in bigrams_dict.keys():
            word1 = bigram[0]
            word2 = bigram[1]
            bigrams_set = set() if first_words_in_bigrams.get(word1) is None else first_words_in_bigrams.get(word1)
            bigrams_set.add(bigram)
            first_words_in_bigrams.update({word1: bigrams_set})
            bigrams_set = set() if second_words_in_bigrams.get(word2) is None else second_words_in_bigrams.get(word2)
            bigrams_set.add(bigram)
            second_words_in_bigrams.update({word2: bigrams_set})
            pbar.update(1)

    llr_index = {}
    with tqdm(total=len(bigrams_dict)) as pbar:
        for bigram, freq in bigrams_dict.items():
            word1 = bigram[0]
            word2 = bigram[1]
            k11 = freq
            bigrams1 = first_words_in_bigrams[word1]
            bigrams2 = second_words_in_bigrams[word2]
            k12 = sum(bigrams_dict[bi] for bi in bigrams1) - freq
            k21 = sum(bigrams_dict[bi] for bi in bigrams2) - freq
            k22 = all_bigrams - k11 - k12 - k21
            llr_index.update({bigram: llr_2x2(k11, k12, k21, k22)})
            pbar.update(1)
    sorted_results = sorted(llr_index.items(), key=lambda kv: (-kv[1]))
    pprint.pprint(sorted_results[:5])
    #  [((('który', 'adj'), ('mowa', 'subst')), 248059.45596041984),
    #  ((('o', 'prep'), ('który', 'adj')), 190489.3647459643),
    #  ((('mowa', 'subst'), ('w', 'prep')), 177055.41246163473),
    #  ((('w', 'prep'), ('artykuł', 'brev')), 113606.97630033107),
    #  ((('otrzymywać', 'fin'), ('brzmienie', 'subst')), 110697.47194672914)]
    return llr_index


bigrams_with_llr = llr_measure_bigrams()

# Partition the entries based on the syntactic categories of the words,
# i.e. all bigrams having the form of w1:adj w2:subst should be placed in one partition
# (the order of the words may not be changed).
partitions = dict()

for bigram, num in bigrams_dict.items():
    (a, b) = bigram
    categories = (a[1], b[1])
    if categories in partitions.keys():
        partitions[categories]['sum'] += num
        partitions[categories]['bigrams'].add(bigram)
    else:
        partitions.update({categories: {'sum': num, 'bigrams': {bigram}}})

# Select the 10 largest partitions (partitions with the larges number of entries)

sorted_partitions_by_sum = sorted(partitions.items(), key=lambda kv: -kv[1]['sum'])
pprint.pprint([(k[0], k[1]['sum']) for k in sorted_partitions_by_sum[:10]])
# [(('prep', 'subst'), 323591),
#  (('subst', 'subst'), 280316),
#  (('subst', 'adj'), 273260),
#  (('adj', 'subst'), 188028),
#  (('subst', 'prep'), 171005),
#  (('subst', 'conj'), 84094),
#  (('conj', 'subst'), 83052),
#  (('ger', 'subst'), 81237),
#  (('prep', 'adj'), 79621),
#  (('prep', 'brev'), 66983)]


sorted_partitions_by_entries_number = sorted(partitions.items(), key=lambda kv: -len(kv[1]['bigrams']))
pprint.pprint([(k[0], len(k[1]['bigrams'])) for k in sorted_partitions_by_entries_number[:10]])
largest_categories = sorted_partitions_by_entries_number[:10]
# [(('subst', 'subst'), 45176),
#  (('subst', 'adj'), 26721),
#  (('adj', 'subst'), 25806),
#  (('subst', 'fin'), 16060),
#  (('ger', 'subst'), 15988),
#  (('prep', 'subst'), 11937),
#  (('subst', 'prep'), 11269),
#  (('subst', 'ppas'), 10485),
#  (('adj', 'fin'), 8705),
#  (('fin', 'subst'), 8661)]

# Use the computed LLR measure to select 5 bigrams for each of the largest categories.
for cat in largest_categories:
    bigrams = cat[1]['bigrams']
    sorted_bigrams = sorted(bigrams, key=lambda bigram: -bigrams_with_llr[bigram])
    print(cat[0])
    pprint.pprint(sorted_bigrams[:5])
# ('subst', 'subst')
# [(('droga', 'subst'), ('rozporządzenie', 'subst')),
#  (('skarb', 'subst'), ('państwo', 'subst')),
#  (('rada', 'subst'), ('minister', 'subst')),
#  (('terytorium', 'subst'), ('rzeczpospolita', 'subst')),
#  (('ochrona', 'subst'), ('środowisko', 'subst'))]
# ('subst', 'adj')
# [(('minister', 'subst'), ('właściwy', 'adj')),
#  (('rzeczpospolita', 'subst'), ('polski', 'adj')),
#  (('jednostka', 'subst'), ('organizacyjny', 'adj')),
#  (('samorząd', 'subst'), ('terytorialny', 'adj')),
#  (('produkt', 'subst'), ('leczniczy', 'adj'))]
# ('adj', 'subst')
# [(('który', 'adj'), ('mowa', 'subst')),
#  (('niniejszy', 'adj'), ('ustawa', 'subst')),
#  (('następujący', 'adj'), ('zmiana', 'subst')),
#  (('odrębny', 'adj'), ('przepis', 'subst')),
#  (('walny', 'adj'), ('zgromadzenie', 'subst'))]
# ('subst', 'fin')
# [(('kropka', 'subst'), ('zastępować', 'fin')),
#  (('ustawa', 'subst'), ('wchodzić', 'fin')),
#  (('treść', 'subst'), ('oznaczać', 'fin')),
#  (('minister', 'subst'), ('określić', 'fin')),
#  (('zdrowie', 'subst'), ('określić', 'fin'))]
# ('ger', 'subst')
# [(('pozbawić', 'ger'), ('wolność', 'subst')),
#  (('zasięgnąć', 'ger'), ('opinia', 'subst')),
#  (('wykonywać', 'ger'), ('zawód', 'subst')),
#  (('zawrzeć', 'ger'), ('umowa', 'subst')),
#  (('wszcząć', 'ger'), ('postępowanie', 'subst'))]
# ('prep', 'subst')
# [(('z', 'prep'), ('dzień', 'subst')),
#  (('na', 'prep'), ('podstawa', 'subst')),
#  (('do', 'prep'), ('sprawa', 'subst')),
#  (('w', 'prep'), ('droga', 'subst')),
#  (('od', 'prep'), ('dzień', 'subst'))]
# ('subst', 'prep')
# [(('mowa', 'subst'), ('w', 'prep')),
#  (('ustawa', 'subst'), ('z', 'prep')),
#  (('wniosek', 'subst'), ('o', 'prep')),
#  (('dzień', 'subst'), ('od', 'prep')),
#  (('miesiąc', 'subst'), ('od', 'prep'))]
# ('subst', 'ppas')
# [(('zasada', 'subst'), ('określić', 'ppas')),
#  (('brzmienie', 'subst'), ('nadać', 'ppas')),
#  (('ustawa', 'subst'), ('zmieniać', 'ppas')),
#  (('czyn', 'subst'), ('zabronić', 'ppas')),
#  (('warunek', 'subst'), ('określić', 'ppas'))]
# ('adj', 'fin')
# [(('obowiązany', 'adj'), ('być', 'fin')),
#  (('który', 'adj'), ('wchodzić', 'fin')),
#  (('publiczny', 'adj'), ('określić', 'fin')),
#  (('wewnętrzny', 'adj'), ('określić', 'fin')),
#  (('narodowy', 'adj'), ('określić', 'fin'))]
# ('fin', 'subst')
# [(('otrzymywać', 'fin'), ('brzmienie', 'subst')),
#  (('podlegać', 'fin'), ('kara', 'subst')),
#  (('mieć', 'fin'), ('prawo', 'subst')),
#  (('mieć', 'fin'), ('zastosowanie', 'subst')),
#  (('zachowywać', 'fin'), ('moc', 'subst'))]
