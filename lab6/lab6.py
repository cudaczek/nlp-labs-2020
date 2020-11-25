import pprint
import requests
import networkx as nx
import matplotlib.pyplot as plt


def get_synset_id(sense_id):
    synset = requests.get(f'http://api.slowosiec.clarin-pl.eu/plwordnet-api/senses/{sense_id}/synset')
    return synset.json()['id']


def get_words(synset_id, only_first_sense=False):
    synonyms = []
    r = requests.get(f'http://api.slowosiec.clarin-pl.eu/plwordnet-api/synsets/{synset_id}/senses')
    for synset in r.json():
        if (only_first_sense and synset['senseNumber'] == 1) or not only_first_sense:
            word = synset['lemma']['word']
            synonyms.append(word)
    return synonyms


def search_senses_ids(lemma, senseNumber=None):
    r = requests.get('http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/search', params={'lemma': lemma})
    if r.json()['totalElements'] == 0:
        return None
    if senseNumber is not None:
        return [sense['id'] for sense in r.json()['content'] if sense['senseNumber'] == senseNumber][0]
    return [sense['id'] for sense in r.json()['content']]


def get_relation(sense_id):
    r = requests.get(f'http://api.slowosiec.clarin-pl.eu/plwordnet-api/synsets/{sense_id}/relations')
    return r.json()


# Find all meanings of the szkoda noun and display all their synonyms.
def find_all_meanings_of_word(word):
    senses_ids = search_senses_ids(word)
    synonyms = set()
    for sense in senses_ids:
        sense_id = get_synset_id(sense)
        synonyms_list = get_words(sense_id)
        synonyms.update(set(synonyms_list))
    pprint.pprint(synonyms)


find_all_meanings_of_word("szkoda")
# {'żałować', 'uszczerbek', 'strata', 'szkoda', 'żal', 'utrata'}


# Find closure of hypernymy relation for the first meaning of the wypadek drogowy expression.
# Create diagram of the relations as a directed graph.
def find_closure_of_hyperonymy(expression):
    expression_id = search_senses_ids(expression, 1)
    synset_id = get_synset_id(expression_id)
    ids = [synset_id]

    hypernymy = lambda synset: synset['relation']['name'] == 'hiperonimia'

    for id in ids:
        relation_ids = [rel['synsetFrom']['id'] for rel in get_relation(id) if hypernymy(rel)]
        for i in relation_ids:
            if i not in ids:
                ids.append(i)
    return ids


def show_hypenymy_graph(ids):
    G = nx.DiGraph()
    i = 0

    labels = {}

    words_levels = []
    for id in ids:
        words = get_words(id)
        words_level = []
        for word in words:
            G.add_node(i)
            labels[i] = word
            words_level.append((i, word))
            i += 1
        words_levels.append(words_level)

    i = 0
    for j, lvl in enumerate(words_levels):
        if j < len(words_levels) - 1:
            for word in lvl:
                for next_word in words_levels[j + 1]:
                    G.add_edge(next_word[0], word[0])

    pos = nx.fruchterman_reingold_layout(G)

    plt.figure(figsize=(10, 10))

    plt.axis('off')
    nx.draw_networkx_nodes(G, pos,
                           node_color='r',
                           node_size=800,
                           alpha=0.8)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12)
    nx.draw_networkx_edges(G, pos,
                           width=5, alpha=0.5, edge_color='b')
    plt.savefig("wypadek_drogowy.png")
    plt.show()


expression = 'wypadek drogowy'
show_hypenymy_graph(find_closure_of_hyperonymy(expression))


# Find direct hyponyms of wypadek1 noun.


def find_direct_hyponyms(expression):
    expression_id = search_senses_ids(expression, 1)
    synset_id = get_synset_id(expression_id)
    hyponyms = lambda synset: synset['relation']['name'] == 'hiponimia'
    synsetTo = lambda synset: synset['synsetTo']['id'] == synset_id

    relation_ids = [rel['synsetFrom']['id'] for rel in get_relation(synset_id) if hyponyms(rel) and synsetTo(rel)]
    result = []
    for i in relation_ids:
        result += get_words(i)
    return result


# Find second-order hyponyms of the same noun.
def find_second_order_hyponyms(direct_hyponyms):
    second_order_hyponyms = []
    for hyponym in direct_hyponyms:
        hyponyms = find_direct_hyponyms(hyponym)
        # print(hyponym, hyponyms)
        second_order_hyponyms += hyponyms
    return second_order_hyponyms


expression = "wypadek"
direct_hyponyms = find_direct_hyponyms(expression)
pprint.pprint(direct_hyponyms)
# ['zawał']
# ['tąpnięcie']
# ['katastrofa']
# ['wykolejenie']
# ['zakrztuszenie', 'zachłyśnięcie']
# ['wypadek komunikacyjny']
# ['katastrofa budowlana']
second_order_hyponyms = find_second_order_hyponyms(direct_hyponyms)
pprint.pprint(second_order_hyponyms)
# [
# ====== katastrofa =================
# 'porażka',
#  'przegrana',
#  'klęska',
#  'strata',
#  'utrata',
#  'szkoda',
#  'uszczerbek',
#  'wpadka',
#  'wtopa',
#  'antysztuka',
#  'pudło',
# ========== wykolejenie =============
#  'zepsucie',
#  'rozkład',
#  'rozkład moralny',
#  'staczanie się',
#  'upadek',
#  'degrengolada',
#  'anomia',
# ==== wypadek komunikacyjny ==========
#  'wypadek drogowy']


# Display as a directed graph (with labels for the edges) semantic relations between the following groups of lexemes:
# szkoda2, strata1, uszczerbek1, szkoda majątkowa1, uszczerbek na zdrowiu1, krzywda1, niesprawiedliwość1, nieszczęście2.
# wypadek1, wypadek komunikacyjny1, kolizja2, zderzenie2, kolizja drogowa1, bezkolizyjny2, katastrofa budowlana1, wypadek drogowy1.

a = [("szkoda", 2),
     ("strata", 1),
     ("uszczerbek", 1),
     ("szkoda majątkowa", 1),
     ("uszczerbek na zdrowiu", 1),
     ("krzywda", 1),
     ("niesprawiedliwość", 1),
     ("nieszczęście", 2)]

b = [("wypadek", 1),
     ("wypadek komunikacyjny", 1),
     ("kolizja", 2),
     ("zderzenie", 2),
     ("kolizja drogowa", 1),
     ("bezkolizyjny", 2),
     ("katastrofa budowlana", 1),
     ("wypadek drogowy", 1)]


def get_semantic_relation_in_groups(lista, group_id):
    a_ids = []
    for word in lista:
        expression_id = search_senses_ids(word[0], word[1])
        if expression_id is None:
            # "szkoda majątkowa" can't be found and omitted
            continue
        synset_id = get_synset_id(expression_id)
        a_ids.append(synset_id)

    relations = set()
    for synset_id in a_ids:
        relations.update(
            {(rel['synsetFrom']['id'], rel['synsetTo']['id'], rel['relation']['name']) for rel in
             get_relation(synset_id)})

    G = nx.MultiDiGraph()
    edge_labels = dict()
    list_a_words = [w[0] for w in lista]
    for rel in relations:
        words = get_words(rel[0])
        next_words = get_words(rel[1])
        for word in words:
            for next_word in next_words:
                if word in list_a_words and next_word in list_a_words:
                    G.add_edge(next_word, word)
                    edge_labels.update({(next_word, word): rel[2]})
                if word in list_a_words and word not in list(G.nodes()):
                    G.add_node(word)

    pos = nx.fruchterman_reingold_layout(G)
    plt.figure(figsize=(10, 10))

    plt.axis('off')
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            connectionstyle='arc3, rad = 0.1',
            labels={node: node for node in G.nodes()})

    hipernyms = list(map(lambda kv: kv[0], list(filter(lambda kv: kv[1] == 'hiperonimia',
                                                       edge_labels.items()))))
    hyponyms = list(map(lambda kv: kv[0], list(filter(lambda kv: kv[1] == 'hiponimia',
                                                      edge_labels.items()))))
    nx.draw_networkx_edges(G, pos, edgelist=hipernyms,
                           edge_color='blue',
                           connectionstyle='arc3, rad = 0.1', label='Hiperonimia')
    nx.draw_networkx_edges(G, pos, edgelist=hyponyms,
                           edge_color='green',
                           connectionstyle='arc3, rad = 0.1', label='Hiponimia')
    plt.plot([0], [0], color='blue', label='Hiperonimia')
    plt.plot([0], [0], color='green', label='Hiponimia')
    plt.legend()
    plt.savefig(f"analiza_relacji_{group_id}.png")
    plt.show()


get_semantic_relation_in_groups(a, "a")
get_semantic_relation_in_groups(b, "b")


# Find the value of Leacock-Chodorow semantic similarity measure between following pairs of lexemes:
# szkoda2 - wypadek1,
# kolizja2 - szkoda majątkowa1,
# nieszczęście2 - katastrofa budowlana1.

import nltk

from nltk.corpus import wordnet as wn

# Downloaded polish wordnet!
# nltk.download()


def get_synset_wn(name, index=None):
    return wn.synsets(name)[index] if index is not None else wn.synsets(name)


result = [
    (s1, s2, wn.lch_similarity(s1, s2))
    for (s1, s2) in [
        (get_synset_wn("szkoda", 1), get_synset_wn("wypadek", 0)),
        (get_synset_wn("kolizja", 1), get_synset_wn("szkoda", 1)),
        (get_synset_wn("nieszczęście", 0), get_synset_wn("katastrofa", 1))
    ]
]

# szkoda majątkowa - nie znaleziona
# katastrofa budowlana - nie znalezniona

pprint.pprint(result)
# [(Synset('uszczerbek.n.01'), Synset('katastrofa.n.02'), 2.0794415416798357),
#  (Synset('kolizja.n.02'), Synset('uszczerbek.n.01'), 1.9252908618525775),
#  (Synset('cios.n.02'), Synset('katastrofa.n.02'), 2.4849066497880004)]
