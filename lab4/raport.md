# Multiword expressions identification and extraction
# Wykrywanie i identyfikacja wyrażeń 

Implementacja rozwiązań do poszczególnych zadań znajduje się w pliku lab4.py.

W folderze znajdują się też pliki zawierające n-gramy, które zostały zapisane w celu ułatwienia dostępu do danych (szybciej odczytać z pliku niż wygenerować wszystko od nowa).

## Create a table comparing the methods (separate table for bigrams and trigrams)

W przypadku bigramów zastosowałam następujące przekształcenia:

pmi(x, y) = log [ p(x, y) / (p(x) * p(y)) ] 

oraz dla LLR:

- k_11 = oba wyrazy występują
- k_12 = występuje drugi wyraz, a nie występuje pierwszy
- k_21 = występuje pierwszy wyraz, a nie występuje drugi
- k_22 = nie występuje ani pierwszy, ani drugi wyraz


Dla trigramów przyjęłam, że trigram złożony ze słów a_b_c to para bigramów a_b oraz b_c, następnie korzystałam z tych samych wzorów, ale zamiast unigramów podstawiałam bigramy. 

### Wyniki top10 dla LLR:
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
 
 Zarówno w bigramach, jak i w trigramach zostały znalezione wyrażenia często występujące w dokumentach prawnych;
 W przypadku bigramów znalezione wygrażenia często zawierają spójniki.
 Być może warto byłoby pomijać słowa jedno lub dwuliterowe, bo aktualnie bigramy z wysokim LLR nie ukazały żadnych wielowyrazowych nazw własnych, których można było oczekiwać.

### Top10 dla PMI:
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

W tym wypadku zostały znalezione parokrotnie występujące wyrażenia - gdyby nie odfiltrowywać wyrażeń rzadszych niż 5 wystąpień uzyskalibyśmy jeszcze rzadsze wyrażenia (często pojedyncze pomyłki - przykład w kodzie).


## Answer the following questions:

### Why do we have to filter the bigrams, rather than the token sequence?
Gdybyśmy odfiltrowywali znaki niealfabetyczne z sekwencji tokenów doprowadziłoby to do sytuacji, w której słowa należące na przykład do różnych zdań zostałyby połączone razem, jako bigram (kwestia interpunkcji).
Co z kolei skutkowałoby znacznym zwiększeniem liczby bigramów, z czego spora ich część nie pojawia się w języku jako spójne wyrażenie. 

W ustawach zdarza się dość często konstrukcja wymieniająca numery punktów, czy paragrafów, które niosą za sobą dużo informacji prawniczej, jednak również raczej nie należą do oczekiwanych wyrażeń.
Dodatkowo odfiltrowywanie takich tokenów na wstępnym etapie wpłynęłoby na częstotliwość wystąpień niektórych wyrażeń. 

### Which measure (PMI, PMI with filtering, LLR) works better for the bigrams and which for the trigrams?
W bigramach lepiej odfiltrować rzadkie wyrażenia, gdyż są to często po prostu literówki. 
Obie metody znajdują różne typy wyrażeń - niezależnie od tego, czy to bigramy czy trigramy. 
Na pewno lepiej odfiltrować najrzadsze wystąpienia.
 
### What types of expressions are discovered by the methods.
Generalnie jeśli oczekiwanym jest wykrycie złożonych (i niezbyt częstych) wyrażeń własnych lepiesza wydaje się miara PMI z filtrowaniem niż bez niego.
Jeśli szukane są wyrażenia charakterystyczne dla danego języka (u nas prawniczy), to lepiej ten styl zaprezentuje LLR - jeśli dodatkowo zrezygnuje się tu ze słów bardzo krótkich w wyniku można uzyskać popularne nazwy własne.

### Can you devise a different type of filtering that would yield better results?
Odfiltrowywanie wyrazów bardzo krótkich - opisane już wcześniej. 
Można byłoby też rezygnować z najpopularniejszych spójników - bo występują bardzo często generalnie w języku polskim - jeśli celem miałoby zapoznanie się z konkretnym korpusem i jego charakterysstyką, to prawdopodobnie spójniki mogłyby być zbędne. 

