import pprint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import manifold
from gensim.models import KeyedVectors

# Download polish word embeddings for word2vec github/Google drive:
# https://github.com/sdadas/polish-nlp-resources
# with 100 dimensionality
# word2vec_100 = KeyedVectors.load("word2vec/word2vec_100_3_polish.bin")
# with 300 dimensionality
word2vec_300 = KeyedVectors.load("word2vec_300_3_polish/word2vec_300_3_polish.bin")

# Using the downloaded models find the most similar words for the following expressions...
# And display 5 most similar words according to each model:
# kpk
# szkoda
# wypadek
# kolizja
# nieszczęście
# rozwód
words = ['kpk', 'szkoda', 'wypadek', 'kolizja', 'nieszczęście', 'rozwód']


def get_most_similar_words(expression):
    print(f"--------- Most similar words for {expression} ---------")
    print("word2vec_100:")
    result = word2vec_100.most_similar(positive=[expression])
    pprint.pprint(result[:5])
    print("word2vec_300:")
    result = word2vec_300.most_similar(positive=[expression])
    pprint.pprint(result[:5])
    print()


# for word in words:
#     get_most_similar_words(word)

# --------- Most similar words for kpk ---------
# word2vec_100:
# [('kilopond', 0.6665806770324707),
#  ('kpzs', 0.6363496780395508),
#  ('kpu', 0.6300562024116516),
#  ('sownarkomu', 0.6254925727844238),
#  ('wcik', 0.6224358677864075)]
# word2vec_300:
# [('ksh', 0.5774794220924377),
#  ('cywilnego', 0.5498510599136353),
#  ('postępowania', 0.5285828113555908),
#  ('kilopond', 0.5151568055152893),
#  ('kkkw', 0.48344212770462036)]
#
# --------- Most similar words for szkoda ---------
# word2vec_100:
# [('krzywda', 0.6817898750305176),
#  ('pożytek', 0.6121943593025208),
#  ('strata', 0.5968126654624939),
#  ('ryzyko', 0.5745570659637451),
#  ('uszczerbek', 0.5639551877975464)]
# word2vec_300:
# [('uszczerbek', 0.6027276515960693),
#  ('krzywda', 0.5920778512954712),
#  ('strata', 0.550269365310669),
#  ('despekt', 0.5382484197616577),
#  ('pożytek', 0.531347393989563)]
#
# --------- Most similar words for wypadek ---------
# word2vec_100:
# [('przypadek', 0.7544811964035034),
#  ('okoliczności', 0.7268072366714478),
#  ('padku', 0.6788284182548523),
#  ('incydent', 0.6418948173522949),
#  ('zdarzenie', 0.6114422082901001)]
# word2vec_300:
# [('przypadek', 0.7066895961761475),
#  ('okoliczności', 0.6121077537536621),
#  ('padku', 0.6056742072105408),
#  ('padki', 0.5596078634262085),
#  ('incydent', 0.5496981143951416)]
#
# --------- Most similar words for kolizja ---------
# word2vec_100:
# [('zderzenie', 0.8431548476219177),
#  ('awaria', 0.7090569734573364),
#  ('kraksa', 0.6777161359786987),
#  ('turbulencja', 0.6613468527793884),
#  ('poślizg', 0.6391660571098328)]
# word2vec_300:
# [('zderzenie', 0.7603178024291992),
#  ('awaria', 0.611009955406189),
#  ('kraksa', 0.5939033031463623),
#  ('turbulencja', 0.5664489269256592),
#  ('poślizg', 0.5569967031478882)]
#
# --------- Most similar words for nieszczęście ---------
# word2vec_100:
# [('niebezpieczeństwo', 0.7519958019256592),
#  ('cierpienia', 0.7408335208892822),
#  ('strapienie', 0.7345459461212158),
#  ('cierpienie', 0.7262567281723022),
#  ('utrapienie', 0.7251379489898682)]
# word2vec_300:
# [('utrapienie', 0.6610732674598694),
#  ('cierpienia', 0.6526124477386475),
#  ('niedola', 0.6478177309036255),
#  ('strapienie', 0.6300181150436401),
#  ('cierpienie', 0.6248573064804077)]
#
# --------- Most similar words for rozwód ---------
# word2vec_100:
# [('małżeństwo', 0.7646843194961548),
#  ('separacja', 0.7547168135643005),
#  ('adopcja', 0.7333694696426392),
#  ('ślub', 0.7324203848838806),
#  ('unieważnienie', 0.7096400856971741)]
# word2vec_300:
# [('separacja', 0.7053208351135254),
#  ('małżeństwo', 0.6689504384994507),
#  ('ślub', 0.6553219556808472),
#  ('rozwodowy', 0.614338219165802),
#  ('unieważnienie', 0.6127183437347412)]


# Find the most similar words for the following expressions (average the representations for each word):
# sąd najwyższy
# trybunał konstytucyjny
# szkoda majątkowy
# kodeks cywilny
# sąd rejonowy
# Display 7 most similar words according to each model.

expressions = ['sąd najwyższy', 'trybunał konstytucyjny', 'szkoda majątkowy', 'kodeks cywilny', 'sąd rejonowy']


def get_most_similiar_words_for_expression_avg(expressions):
    for expr in expressions:
        print(f"--------- Most similar words for {expr} ---------")
        print("word2vec_100:")
        word_1, word_2 = tuple(expr.split())
        result = np.array([np.mean(k) for k in zip(np.array(word2vec_100[word_1]), np.array(word2vec_100[word_2]))])
        pprint.pprint(word2vec_100.similar_by_vector(result)[:7])
        print("word2vec_300:")
        result = np.array([np.mean(k) for k in zip(np.array(word2vec_300[word_1]), np.array(word2vec_300[word_2]))])
        pprint.pprint(word2vec_300.similar_by_vector(result)[:7])
        print()


# get_most_similiar_words_for_expression_avg(expressions)
# --------- Most similar words for sąd najwyższy ---------
# word2vec_100:
# [('sąd', 0.8644266128540039),
#  ('trybunał', 0.7672435641288757),
#  ('najwyższy', 0.7527138590812683),
#  ('trybunat', 0.6843459010124207),
#  ('sędzia', 0.6718415021896362),
#  ('areopag', 0.6571060419082642),
#  ('sprawiedliwość', 0.6562486886978149)]
# word2vec_300:
# [('sąd', 0.8261206150054932),
#  ('trybunał', 0.711520791053772),
#  ('najwyższy', 0.7068409323692322),
#  ('sędzia', 0.6023203730583191),
#  ('sądowy', 0.5670486688613892),
#  ('trybunat', 0.5525928735733032),
#  ('sprawiedliwość', 0.5319530367851257)]
#
# --------- Most similar words for trybunał konstytucyjny ---------
# word2vec_100:
# [('trybunał', 0.9073251485824585),
#  ('konstytucyjny', 0.7998723387718201),
#  ('sąd', 0.7972990274429321),
#  ('bunał', 0.7729247808456421),
#  ('senat', 0.7585273385047913),
#  ('bunału', 0.7441976070404053),
#  ('trybunat', 0.7347140908241272)]
# word2vec_300:
# [('trybunał', 0.8845913410186768),
#  ('konstytucyjny', 0.7739969491958618),
#  ('sąd', 0.7300779819488525),
#  ('trybunat', 0.6758428812026978),
#  ('senat', 0.6632090210914612),
#  ('parlament', 0.6614581346511841),
#  ('bunału', 0.6404117941856384)]
#
# --------- Most similar words for szkoda majątkowy ---------
# word2vec_100:
# [('szkoda', 0.8172438144683838),
#  ('majątkowy', 0.7424530386924744),
#  ('krzywda', 0.6498408317565918),
#  ('świadczenie', 0.6419471502304077),
#  ('odszkodowanie', 0.6392182111740112),
#  ('dochód', 0.637932538986206),
#  ('wydatek', 0.6325603127479553)]
# word2vec_300:
# [('szkoda', 0.7971925735473633),
#  ('majątkowy', 0.7278684973716736),
#  ('uszczerbek', 0.5841633081436157),
#  ('korzyść', 0.5474051237106323),
#  ('krzywda', 0.5431190729141235),
#  ('majątek', 0.525060772895813),
#  ('strata', 0.5228629112243652)]
#
# --------- Most similar words for kodeks cywilny ---------
# word2vec_100:
# [('kodeks', 0.8756389617919922),
#  ('cywilny', 0.8532464504241943),
#  ('pasztunwali', 0.6438998579978943),
#  ('deksu', 0.6374959945678711),
#  ('teodozjańskim', 0.6283917427062988),
#  ('pozakodeksowy', 0.6153194904327393),
#  ('sądowo', 0.6136723160743713)]
# word2vec_300:
# [('kodeks', 0.8212110996246338),
#  ('cywilny', 0.7886406779289246),
#  ('amiatyński', 0.5660314559936523),
#  ('cywilnego', 0.5531740188598633),
#  ('deksu', 0.5472918748855591),
#  ('isps', 0.5369160175323486),
#  ('jōei', 0.5361183881759644)]
#
# --------- Most similar words for sąd rejonowy ---------
# word2vec_100:
# [('sąd', 0.8773891925811768),
#  ('prokuratura', 0.8396657705307007),
#  ('rejonowy', 0.7694871425628662),
#  ('trybunał', 0.755321204662323),
#  ('sądowy', 0.7153753042221069),
#  ('magistrat', 0.7151126861572266),
#  ('prokurator', 0.7081375122070312)]
# word2vec_300:
# [('sąd', 0.8507211208343506),
#  ('rejonowy', 0.7344856262207031),
#  ('prokuratura', 0.711697518825531),
#  ('trybunał', 0.6748420596122742),
#  ('sądowy', 0.6426382064819336),
#  ('okręgowy', 0.6349465847015381),
#  ('apelacyjny', 0.599929690361023)]

# Find the result of the following equations (5 top results, both models):
# sąd + konstytucja - kpk
# pasażer + kobieta - mężczyzna
# pilot + kobieta - mężczyzna
# lekarz + kobieta - mężczyzna
# nauczycielka + mężczyzna - kobieta
# przedszkolanka + mężczyzna - 'kobieta
# samochód + rzeka - droga

equations = [(['sąd', 'konstytucja'], ['kpk']),
             (['pasażer', 'kobieta'], ['mężczyzna']),
             (['pilot', 'kobieta'], ['mężczyzna']),
             (['lekarz', 'kobieta'], ['mężczyzna']),
             (['nauczycielka', 'mężczyzna'], ['kobieta']),
             (['przedszkolanka', 'mężczyzna'], ['kobieta']),
             (['samochód', 'rzeka'], ['droga'])]


def get_result_of_equation(positive, negative):
    print(f"--------- Result for + {positive} and - {negative} ---------")
    print("word2vec_100:")
    result = word2vec_100.most_similar(positive=positive, negative=negative)
    pprint.pprint(result[:5])
    print("word2vec_300:")
    result = word2vec_300.most_similar(positive=positive, negative=negative)
    pprint.pprint(result[:5])
    print()


# for equa in equations:
#     get_result_of_equation(equa[0], equa[1])
# --------- Result for + ['sąd', 'konstytucja'] and - ['kpk'] ---------
# word2vec_100:
# [('trybunał', 0.6436409950256348),
#  ('ustawa', 0.6028786897659302),
#  ('elekcja', 0.5823959112167358),
#  ('deklaracja', 0.5771891474723816),
#  ('dekret', 0.5759621262550354)]
# word2vec_300:
# [('trybunał', 0.5860734581947327),
#  ('senat', 0.5112544298171997),
#  ('ustawa', 0.5023636817932129),
#  ('dekret', 0.48704710602760315),
#  ('władza', 0.4868926703929901)]
#
# --------- Result for + ['pasażer', 'kobieta'] and - ['mężczyzna'] ---------
# word2vec_100:
# [('pasażerka', 0.7234811186790466),
#  ('stewardessa', 0.6305270195007324),
#  ('stewardesa', 0.6282645463943481),
#  ('taksówka', 0.619726300239563),
#  ('podróżny', 0.614517092704773)]
# word2vec_300:
# [('pasażerka', 0.6741673946380615),
#  ('stewardesa', 0.5810248255729675),
#  ('stewardessa', 0.5653151273727417),
#  ('podróżny', 0.5060371160507202),
#  ('pasażerski', 0.4896503686904907)]
#
# --------- Result for + ['pilot', 'kobieta'] and - ['mężczyzna'] ---------
# word2vec_100:
# [('nawigator', 0.6925703287124634),
#  ('oblatywacz', 0.6686224937438965),
#  ('lotnik', 0.6569937467575073),
#  ('pilotka', 0.6518791913986206),
#  ('awionetka', 0.6428645849227905)]
# word2vec_300:
# [('pilotka', 0.6108255386352539),
#  ('lotnik', 0.6020804047584534),
#  ('stewardesa', 0.5943204760551453),
#  ('nawigator', 0.5849766731262207),
#  ('oblatywacz', 0.5674178600311279)]
#
# --------- Result for + ['lekarz', 'kobieta'] and - ['mężczyzna'] ---------
# word2vec_100:
# [('lekarka', 0.7690489292144775),
#  ('ginekolog', 0.7575511336326599),
#  ('pediatra', 0.7478542923927307),
#  ('psychiatra', 0.732271671295166),
#  ('położna', 0.7268943786621094)]
# word2vec_300:
# [('lekarka', 0.7388788461685181),
#  ('pielęgniarka', 0.6719920635223389),
#  ('ginekolog', 0.658279299736023),
#  ('psychiatra', 0.6389409303665161),
#  ('chirurg', 0.6305986642837524)]
#
# --------- Result for + ['nauczycielka', 'mężczyzna'] and - ['kobieta'] ---------
# word2vec_100:
# [('uczennica', 0.7441667318344116),
#  ('studentka', 0.7274973392486572),
#  ('nauczyciel', 0.7176114916801453),
#  ('wychowawczyni', 0.7153530120849609),
#  ('koleżanka', 0.678418755531311)]
# word2vec_300:
# [('nauczyciel', 0.6561620235443115),
#  ('wychowawczyni', 0.6211140155792236),
#  ('uczennica', 0.6142012476921082),
#  ('koleżanka', 0.5501158237457275),
#  ('przedszkolanka', 0.5497692823410034)]
#
# --------- Result for + ['przedszkolanka', 'mężczyzna'] and - ['kobieta'] ---------
# word2vec_100:
# [('stażysta', 0.6987776756286621),
#  ('wychowawczyni', 0.6618361473083496),
#  ('kreślarka', 0.6590923070907593),
#  ('pielęgniarz', 0.6492814421653748),
#  ('siedmiolatek', 0.6483469009399414)]
# word2vec_300:
# [('stażysta', 0.5117638111114502),
#  ('pierwszoklasista', 0.49398648738861084),
#  ('wychowawczyni', 0.49037522077560425),
#  ('praktykant', 0.48884207010269165),
#  ('pielęgniarz', 0.4795262813568115)]
#
# --------- Result for + ['samochód', 'rzeka'] and - ['droga'] ---------
# word2vec_100:
# [('jeep', 0.6142987608909607),
#  ('buick', 0.5962571501731873),
#  ('dżip', 0.5938510894775391),
#  ('ponton', 0.580719530582428),
#  ('landrower', 0.5799552202224731)]
# word2vec_300:
# [('dżip', 0.5567235946655273),
#  ('jeep', 0.5533617734909058),
#  ('auto', 0.5478508472442627),
#  ('ciężarówka', 0.5461742281913757),
#  ('wóz', 0.5204571485519409)]

# Using the t-SNE algorithm compute the projection of the random 1000 words with the following words highlighted (both models):
# szkoda
# strata
# uszczerbek
# krzywda
# niesprawiedliwość
# nieszczęście
# kobieta
# mężczyzna
# pasażer
# pasażerka
# student
# studentka
# lekarz
# lekarka

words = np.array(['szkoda', 'strata', 'uszczerbek', 'krzywda', 'niesprawiedliwość', 'nieszczęście', 'kobieta',
                  'mężczyzna', 'pasażer', 'pasażerka', 'student', 'studentka', 'lekarz', 'lekarka'])

wv = word2vec_300
# wv = word2vec_100

def scatter_points(hue, point_labels, principal_components):
    x = np.transpose(principal_components)[0]
    y = np.transpose(principal_components)[1]
    plt.scatter(x, y, c=hue, s=100, marker='o', alpha=0.2)
    for i, text in enumerate(point_labels):
        plt.annotate(text, (x[i], y[i]), ha="center", size=8)


def plot_with_tsne(wv, words, perplexity=30, learning_rate=100.0, iterations=1000, filename='slowa300'):
    random_words = np.random.choice(list(wv.wv.vocab), 1000)
    words = np.concatenate((words, random_words))
    vecs = [wv[word] for word in words]
    tsne = manifold.TSNE(2, perplexity=perplexity, learning_rate=learning_rate, n_iter=iterations)
    results = tsne.fit_transform(vecs)
    hue = [0 for _ in range(14)] + [1 for _ in range(1000)]

    plt.figure(figsize=(30, 30))
    scatter_points(hue, words, results)
    plt.savefig(filename + '.png')
    plt.show()
    plt.clf()


plot_with_tsne(wv, words)
