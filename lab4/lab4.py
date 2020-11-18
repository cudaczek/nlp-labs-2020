# Use SpaCy tokenizer API to tokenize the text from the law corpus.
import json
import locale
import math
import os
import pprint
import spacy
import textacy
from tqdm import tqdm

from collections import Counter
from spacy.tokenizer import Tokenizer

from lab4.helpers import llr_2x2

locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

# Use SpaCy tokenizer API to tokenize the text from the law corpus.
nlp = spacy.load("pl_core_news_sm")
# Create a blank Tokenizer with just the Polish vocab
tokenizer = Tokenizer(nlp.vocab)


def is_alpha(k):
    words = k.split()
    for word in words:
        if not word.isalpha():
            return False
    return True


data_path = "../data_lab1/"


# Compute bigram counts of downcased tokens.

def get_n_grams(n, tokens):
    file_result = []
    for token in tokens:
        file_result.append(token.text)
    return [" ".join(file_result[i:i + n]) for i in range(len(tokens) - n + 1)]


def ngrams(n):
    aggregated_results = Counter({})
    with tqdm(total=1179) as pbar:
        for filename in os.listdir(data_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(data_path, filename)
                content = open(filepath, 'r', encoding='utf-8').read().split()
                content = " ".join(content).lower()  # małe litery
                tokens = tokenizer(content)
                ngrams = get_n_grams(n, tokens)
                aggregated_results = aggregated_results + Counter(ngrams)
            else:
                continue
            pbar.update(1)
    return aggregated_results


# Unigrams
def unigrams():
    with tqdm(total=1179) as pbar:
        for filename in os.listdir(data_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(data_path, filename)
                content = open(filepath, 'r', encoding='utf-8').read().split()
                content = " ".join(content).lower()  # małe litery
                tokens = tokenizer(content)
                file_result = []
                for token in tokens:
                    file_result.append(token.text)
                aggregated_results = aggregated_results + Counter(file_result)
            else:
                continue
            pbar.update(1)

    print("Cleaning the result...")
    aggregated_cleaned_results = {k: v for k, v in aggregated_results.items() if k.isalpha()}

    with open("unigrams_counter.json", 'w') as outfile:
        json.dump(aggregated_cleaned_results, outfile)


def bigrams():
    aggregated_results = ngrams(2)
    # Discard bigrams containing characters other than letters.
    # Make sure that you discard the invalid entries after computing the bigram counts.
    print("Cleaning data...")
    aggregated_cleaned_results = {k: v for k, v in aggregated_results.items()
                                  if is_alpha(k)}

    pprint.pprint(aggregated_cleaned_results)
    with open("bigrams_counter.json", 'w') as outfile:
        json.dump(aggregated_cleaned_results, outfile)


def trigrams():
    aggregated_results = ngrams(3)
    # Discard trigrams containing characters other than letters.
    print("Cleaning data...")
    aggregated_cleaned_results = {k: v for k, v in aggregated_results.items()
                                  if k.split()[0].isalpha() and k.split()[1].isalpha() and k.split()[2].isalpha}

    pprint.pprint(aggregated_cleaned_results)
    with open("trigrams_counter.json", 'w') as outfile:
        json.dump(aggregated_cleaned_results, outfile)


# unigrams()
# bigrams()

with open("bigrams_counter.json", 'r', encoding='utf-8') as json_file:
    bigrams_dict = json.load(json_file)

with open("unigrams_counter.json", 'r', encoding='utf-8') as json_file:
    unigrams_dict = json.load(json_file)

all_unigrams = sum(unigrams_dict.values())
all_bigrams = sum(bigrams_dict.values())


# Use pointwise mutual information to compute the measure for all pairs of words
def pmi(word1, word2):
    prob_word1 = unigrams_dict[word1] / float(all_unigrams)
    prob_word2 = unigrams_dict[word2] / float(all_unigrams)
    prob_word1_word2 = bigrams_dict[" ".join([word1, word2])] / float(all_bigrams)
    return math.log(prob_word1_word2 / float(prob_word1 * prob_word2), 2)


def find_top_10_by_pmi(source_dict):
    pmi_index = {}
    for bigram, freq in source_dict.items():
        word1 = bigram.split()[0]
        word2 = bigram.split()[1]
        pmi_index.update({bigram: pmi(word1, word2)})

    # Sort the word pairs according to that measure in the descending order and determine top 10 entries.
    sorted_results = sorted(pmi_index.items(), key=lambda kv: (-kv[1], locale.strxfrm(kv[0])))
    pprint.pprint(sorted_results[:10])


find_top_10_by_pmi(bigrams_dict)
"""
    Wynik:
    [('admi nistracji', 21.936400287470526),
     ('adminis tracji', 21.936400287470526),
     ('administracjami drogowymi', 21.936400287470526),
     ('aegroti suprema', 21.936400287470526),
     ('aerodynamicznej szorstkości', 21.936400287470526),
     ('agregatach pralniczych', 21.936400287470526),
     ('agricoltura biologica', 21.936400287470526),
     ('agriculture biologique', 21.936400287470526),
     ('agrotechniki nienaruszającej', 21.936400287470526),
     ('ają cyc', 21.936400287470526)]
    Bez alfabetycznego sortowania:
    [('kołowe jednoosiowe', 21.936400287470526),
     ('automatyki grzewczej', 21.936400287470526),
     ('prefabrykatów wnętrzowe', 21.936400287470526),
     ('gołe aluminiowe', 21.936400287470526),
     ('polistyrenu spienionego', 21.936400287470526),
     ('objaśnieniem figur', 21.936400287470526),
     ('wkładzie wnoszonym', 21.936400287470526),
     ('doktorem habilitowanym', 21.936400287470526),
     ('naruszonymi plombami', 21.936400287470526),
     ('uw zględnieniu', 21.936400287470526)]
Warto zauważyć, że powyższa funkcja znalazła bigramy, które występują tylko raz w całym korpusie (albo są rzadkie, albo są literówkami).
Miara PMI uzyskuje najwyższe wartości właśnie dla takich "wyjątkowych" słów.
"""


# Filter bigrams with number of occurrences lower than 5.
# Determine top 10 entries for the remaining dataset (>=5 occurrences).
def top_frequent_bigrams():
    bigrams_filtered = {k: v for k, v in bigrams_dict.items() if v >= 5}
    sorted_results = sorted(bigrams_filtered.items(), key=lambda kv: (-kv[1], locale.strxfrm(kv[0])))
    return sorted_results


pprint.pprint(top_frequent_bigrams()[:10])
"""
Wynik:
[('mowa w', 28450),
 ('których mowa', 13847),
 ('o których', 13839),
 ('z dnia', 9513),
 ('którym mowa', 9165),
 ('o którym', 9155),
 ('do spraw', 8680),
 ('i nr', 8435),
 ('dodaje się', 8190),
 ('w drodze', 7092)]
Mamy wyrażenia najczęśćiej występujące w całym korpusie.
"""

find_top_10_by_pmi(dict(top_frequent_bigrams()))
"""
Wynik:
[('grzegorz schetyna', 19.614472192583165),
 ('młyny kulowe', 19.614472192583165),
 ('najnowszych zdobyczy', 19.614472192583165),
 ('ręcznego miotacza', 19.614472192583165),
 ('świeckie przygotowujące', 19.614472192583165),
 ('zaszkodzić wynikom', 19.614472192583165),
 ('adama mickiewicza', 19.351437786749372),
 ('chromu sześciowartościowego', 19.351437786749372),
 ('chrześcijan baptystów', 19.351437786749372),
 ('mleczka makowego', 19.351437786749372)]
Dość ciekawy zestaw słów, które występują pięć razy i mają wysokie PMI.
"""


# Use log likelihood ratio (LLR) to compute the measure for all pairs of words.


def llr_measure_bigrams():
    # zapisuję bigramy do przeszukania w setach
    # przeszukiwanie każdorazowo całego słownika grozi wysoką złożonością czasową - odczyt jest szybszy
    first_words_in_bigrams = {}
    second_words_in_bigrams = {}

    with tqdm(total=len(bigrams_dict)) as pbar:
        for bigram in bigrams_dict.keys():
            word1 = bigram.split()[0]
            word2 = bigram.split()[1]
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
            word1 = bigram.split()[0]
            word2 = bigram.split()[1]
            k11 = freq
            bigrams1 = first_words_in_bigrams[word1]
            bigrams2 = second_words_in_bigrams[word2]
            k12 = sum(bigrams_dict[bi] for bi in bigrams1) - freq
            k21 = sum(bigrams_dict[bi] for bi in bigrams2) - freq
            k22 = all_bigrams - k11 - k12 - k21
            llr_index.update({bigram: llr_2x2(k11, k12, k21, k22)})
            pbar.update(1)
    # Sort the word pairs according to that measure in the descending order and display top 10 entries.

    sorted_results = sorted(llr_index.items(), key=lambda kv: (-kv[1], locale.strxfrm(kv[0])))
    pprint.pprint(sorted_results[:10])


llr_measure_bigrams()
"""
Wynik:
[('mowa w', 169420.0968855021),
 ('których mowa', 110964.59604967944),
 ('o których', 89441.49602821318),
 ('którym mowa', 71651.64390171401),
 ('dodaje się', 64785.95433424151),
 ('do spraw', 60667.23145855474),
 ('o którym', 56871.95380545885),
 ('i nr', 54795.940221138415),
 ('na podstawie', 51409.2964036467),
 ('z dnia', 49289.194381956244)]
 W wyniku otrzymaliśmy wyrażenia podobne jak dość często występujące w dokumentach.
"""

# Compute trigram counts for the whole corpus and perform the same filtering.
# trigrams()


with open("trigrams_counter.json", 'r', encoding='utf-8') as json_file:
    trigrams_dict = json.load(json_file)

all_trigrams = sum(trigrams_dict.values())


# Use PMI (with 5 occurrence threshold) and LLR to compute top 10 results for the trigrams.
# Devise a method for computing the values, based on the results for bigrams.

def pmi_for_tri(word1, word2, word3):
    prob_bigram1 = bigrams_dict[" ".join([word1, word2])] / float(all_bigrams)
    prob_bigram2 = bigrams_dict[" ".join([word2, word3])] / float(all_bigrams)
    prob_word1_word2_word3 = trigrams_dict[" ".join([word1, word2, word3])] / float(all_trigrams)
    return math.log(prob_word1_word2_word3 / float(prob_bigram1 * prob_bigram2), 2)


trigrams_frequent = {k: v for k, v in trigrams_dict.items() if v >= 5}


def find_top_10_by_pmi_tri(source_dict):
    pmi_index = {}
    for bigram, freq in source_dict.items():
        word1 = bigram.split()[0]
        word2 = bigram.split()[1]
        word3 = bigram.split()[2]
        pmi_index.update({bigram: pmi_for_tri(word1, word2, word3)})

    sorted_results = sorted(pmi_index.items(), key=lambda kv: (-kv[1], locale.strxfrm(kv[0])))
    pprint.pprint(sorted_results[:10])


find_top_10_by_pmi_tri(trigrams_frequent)
"""
Wynik:
[('akt wykonawczy wydany', 20.27320245706795),
 ('aktywa razem pasywa', 20.27320245706795),
 ('artykułu vii układu', 20.27320245706795),
 ('bankowym postępowaniem ugodowym', 20.27320245706795),
 ('betonowe lub murowane', 20.27320245706795),
 ('będący delegatami członkowie', 20.27320245706795),
 ('braku przeciwnego dowodu', 20.27320245706795),
 ('broni było dopuszczalne', 20.27320245706795),
 ('budżetu sprawozdania wojewody', 20.27320245706795),
 ('byłym i obecnym', 20.27320245706795)]
Znalezione trigramy są wyrażeniami, których można by się nawet może spodziewać, ale znów PMI wybrał wyrażenia występujące najrzadziej (czyli 5 razy).
"""


def llr_measure_trigrams():
    first_pair_in_trigrams = {}
    second_pair_in_trigrams = {}

    with tqdm(total=len(trigrams_frequent)) as pbar:
        for trigram in trigrams_frequent.keys():
            pair1 = trigram.split()[0] + " " + trigram.split()[1]
            pair2 = trigram.split()[1] + " " + trigram.split()[2]
            trigrams_set = set() if first_pair_in_trigrams.get(pair1) is None else first_pair_in_trigrams.get(pair1)
            trigrams_set.add(trigram)
            first_pair_in_trigrams.update({pair1: trigrams_set})
            trigrams_set = set() if second_pair_in_trigrams.get(pair2) is None else second_pair_in_trigrams.get(pair2)
            trigrams_set.add(trigram)
            second_pair_in_trigrams.update({pair2: trigrams_set})
            pbar.update(1)

    llr_index = {}
    with tqdm(total=len(trigrams_frequent)) as pbar:
        for trigram, freq in trigrams_frequent.items():
            pair1 = trigram.split()[0] + " " + trigram.split()[1]
            pair2 = trigram.split()[1] + " " + trigram.split()[2]
            k11 = freq
            trigrams1 = first_pair_in_trigrams[pair1]
            trigrams2 = second_pair_in_trigrams[pair2]
            k12 = sum(trigrams_frequent[tri] for tri in trigrams1) - freq
            k21 = sum(trigrams_frequent[tri] for tri in trigrams2) - freq
            k22 = all_trigrams - k11 - k12 - k21
            llr_index.update({trigram: llr_2x2(k11, k12, k21, k22)})
            pbar.update(1)
    # Sort the word pairs according to that measure in the descending order and display top 10 entries.

    sorted_results = sorted(llr_index.items(), key=lambda kv: (-kv[1], locale.strxfrm(kv[0])))
    pprint.pprint(sorted_results[:10])


llr_measure_trigrams()
"""
Wynik:
[('właściwy do spraw', 44519.42111423481),
 ('ustawie z dnia', 35194.68429852709),
 ('zastępuje się wyrazami', 32966.37148779545),
 ('ustawy z dnia', 28954.717193650504),
 ('wejścia w życie', 25658.528611202324),
 ('wprowadza się następujące', 25544.30619742281),
 ('stosuje się odpowiednio', 21424.68606838495),
 ('dni od dnia', 20655.697505435455),
 ('porozumieniu z ministrem', 17698.396728554715),
 ('wchodzi w życie', 15420.591823952534)]
 Są to wyrażenia występujące najczęściej w ustawach, nie są to nazwy własne, a raczej sformułowania wprowadzające zmiany w dokumentach prawnych,
 charakterystyczne dla języka prawniczego. 
"""
