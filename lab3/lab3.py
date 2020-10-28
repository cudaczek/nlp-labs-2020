import json
import locale
import matplotlib.pyplot as plt
import os
import pprint

import spacy
from collections import Counter
from spacy.tokenizer import Tokenizer

# Ustalam encoding, który pozwoli mi sortować słowa zgodnie z kolejnością liter w polskim alfabecie.
locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

## Use SpaCy tokenizer API to tokenize the text from the law corpus.
nlp = spacy.load("pl_core_news_sm")
# Create a blank Tokenizer with just the Polish vocab
tokenizer = Tokenizer(nlp.vocab)

## Compute frequency list for each of the processed files.
# Dla każdego dokumentu zliczam liczbę wystąpień tokenu i zapisuje je w słowniku.

data_path = "../data_lab1/"
results = dict()

from tqdm import tqdm

with tqdm(total=1180) as pbar:
    for filename in os.listdir(data_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_path, filename)
            content = open(filepath, 'r', encoding='utf-8').read().split()
            content = " ".join(content)
            tokens = tokenizer(content)
            file_result = []
            for token in tokens:
                file_result.append(token.text)
            results.update({filename: Counter(file_result)})
        else:
            continue
        pbar.update(1)

## Aggregate the result to obtain one global frequency list.
# Sumuję wystąpienia tych samych tokenów w różnych słownikach, aby stworzyć listę globalnej częstotliwości wystąpień słów.
print("Aggregating the result...")
aggregated_results = sum(results.values(), Counter())

## Reject all entries that are shorter than 2 characters or contain non-letter characters (make sure to include Polish diacritics)
# Przy pomocy list comprehension wybieram z wcześniej utworzonego słownika tylko te tokeny, które są dłuższe niż dwa znaki i są złożone z samych liter.
print("Cleaning the result...")
aggregated_cleaned_results = {k: aggregated_results[k] for k in aggregated_results if len(k) > 2 and k.isalpha()}
# print(aggregated_cleaned_results)

## Make a plot in a logarithmic scale:
# - X-axis should contain the rank of a term, meaning the first rank belongs to the term with the highest number of occurrences; the terms with the same number of occurrences should be ordered by their name,
# - Y-axis should contain the number of occurrences of the term with given rank.
# Na początek sortuję zawartość słownika po liczbie wystąpień, a jeśli jest taka sama to sortuje po kluczu uwzględniając alfabet polski,
# czyli ąęćśżź (stąd drugi strybut sortowaniu korzysta ze wcześniej ustalonego encodingu).
print("Sorting the result...")
sorted_results = sorted(aggregated_cleaned_results.items(), key=lambda kv: (-kv[1], locale.strxfrm(kv[0])))


# print(sorted_results)

def plot_sorted_results():
    print("Plot...")
    # Rank ustalamy jako kolejność w posortowanej liście rezultatów,
    # a liczbę wystąpień odczytujemy wprost z pary (słowo, częstotliwość).
    x_ranks = range(1, len(sorted_results) + 1)
    y_occurances = [t[1] for t in sorted_results]

    plt.figure(figsize=(15, 15))
    plt.yscale("log")
    plt.ylabel("Occurrences")
    plt.xscale("log")
    plt.xlabel("Ranks")
    plt.plot(x_ranks, y_occurances, 'b.')
    plt.savefig("lab3_task5.png")
    plt.show()


y_occurances = [t[1] for t in sorted_results]

plot_sorted_results()

# Na powyższym wykresie widać poziome linie w momemcie, gdy jest taka sama częstotliwość słów.
# Słowa najczęściej występujące się mocniej wyróżniają, występują rzadziej.
# W środku wykresu gęstość jest znacząco większa niż przy jego końcach.

## Download polimorfologik.zip dictionary and use it to find all words that do not appear in that dictionary.

polimorfix = './polimorfologik-2.1/polimorfologik-2.1.txt'
content = open(polimorfix, 'r', encoding='utf-8').read().split("\n")
morfologic_dict = set([(c.split(";")[1]).lower() for c in content])


def find_all_words_not_in_dict_lower_letters():
    # Poniższa linijka wykonuje się przeraźliwie długo z powodu rozmiaru słownika,
    # stąd później zapisuję dane, żeby mieć do nich szybszy dostęp.
    words_not_in_dict = {"words":
                             [{res[0]: res[1]} for res in sorted_results if (res[0]).lower() not in morfologic_dict]}
    print("Words that do not appear in polimorfologik")
    pprint.pprint(words_not_in_dict)
    with open("words_not_in_dict_2.json", 'w') as outfile:
        json.dump(words_not_in_dict, outfile)


find_all_words_not_in_dict_lower_letters()

with open("words_not_in_dict_2.json", 'r', encoding='utf-8') as json_file:
    words_not_in_dict = list(json.load(json_file)["words"])

    ## Find 30 words with the highest ranks that do not belong to the dictionary.
    # W tym przypadku wystarczy wziąć 30 pierwszysch słów.
    print("30 words that do not appear in polimorfologik with highest rank")
    pprint.pprint(words_not_in_dict[:30])

    ## Find 30 words with 5 occurrences that do not belong to the dictionary.
    print("30 words that do not appear in polimorfologik with 5 occurrences")
    words_not_in_dict_with_5_occ = list(filter(lambda x: list(x.items())[0][1] == 5, words_not_in_dict))[:30]
    pprint.pprint(words_not_in_dict_with_5_occ)

## Use Levenshtein distance and the frequency list, to determine the most probable correction of the words from the second list.
# (You don't have to apply the distance directly. Any method that is more efficient than scanning the dictionary will be appreciated.)
# Zamiast sprawdzać wszystkie słowa, będę generować te, które różnią się o 1 lub 2 przy metryce Levensteina.
# w tym celu skorzystam z przykładu opisanego w https://norvig.com/spell-correct.html odpowiednio modyfikowanego

frequency_list = aggregated_cleaned_results
all_occurances = sum(y_occurances)
morfologic_dict = set(morfologic_dict)


def P(word, N=all_occurances):
    """Probability of `word`."""
    if word in frequency_list:
        return frequency_list[word] / N
    else:
        # jeśli znalezione słowo nie jest w liście częstotliwości, to przyjmuję prawdopodobieństwo 1/N
        # ponieważ to oznacza, że w morfologiku jest zatem istnieje, ale nie pojawiało się w ustawach
        return 1 / N


def correction(word):
    """Most probable spelling correction for word."""
    found_candidates = candidates(word)
    print(found_candidates)
    return max(found_candidates, key=P)


def candidates(word):
    """Generate possible spelling corrections for word."""
    if len(word) <= 8:
        return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]
    else:
        # dla dłuższych słów dopuszczam możliwość nieco większej liczby modyfikacji
        edits2_res = edits2(word)
        return known([word]) or known(edits1(word)) or known(edits2_res) or known(edits3(edits2_res)) or [word]


def known(words):
    """The subset of `words` that appear in the dictionary of WORDS."""
    return set(w for w in words if w.lower() in morfologic_dict)


def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'aąbcćdeęfghijklmnńoópqrsśtuwyzżź'  # litery spodziewane dla alfabetu polskiego
    # pomijam litery v i x
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def edits3(e2_word):
    """All edits that are three edits away from `word`."""
    return (e3 for e2 in e2_word for e3 in edits1(e2))


words_not_in_dict_with_5_occ = {k: v for element in words_not_in_dict_with_5_occ for k, v in element.items()}

for key, value in words_not_in_dict_with_5_occ.items():
    print("Looking for correction of '%s'..." % key)
    best_correction = correction(key)
    if best_correction == key:
        print("No correction found :( ")
    else:
        print("Best correction: ", best_correction)
