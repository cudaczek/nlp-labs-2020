# Levenshtein distance and spelling corrections
# Odległość Levensteina i poprawa pisowni 

## Podsumowanie wniosków

Implementacja zadań 1-9 jest w pliku lab3.py

Zadanie 10 (ElasticSearch) w pliku lab3_es.py

## Zadanie 11. 
### Compare the results. Draw conclusions
- the distribution of words in the corpus:

Wykres zapisany jako lab3_task5.png. 
Na krawędziach jest dość rzadki, a w środku wyraźnie gęstszy. Większość słów znajduje się w środku wykresu. 
Na jednej krawędzi wyraźnie widać poziome linie o tej samej liczbie wystąpień. 

- the number of true misspellings vs. the number of unknown words

Spośród 30 pięciokrątnie występujących słów metoda naiwna uznała za nieznane 4 słowa (sanitarnoepidemiologicznych, badawczorozwojowych, NFOŚiGW, pozaaptecznego) 
Natomiast ES uznał za nieznane 13 słów - w szczególności większość z nich występuje w praktyce w języku polskim.

- the performance of your method compared to ElasitcSearch,

ElasticSearch wyszukuje szybciej niż naiwne liczenie, nie jest to kolosalna różnica, ale wyczuwalna. 
Zapewne jest to związane z indeksowaniem danych przez ESa.

- the results provided by your method compared to ElasticSearch and the validity of the obtained corrections.

Poniżej przedstawiam połączone logi dla ESa oraz metody naiwnej (w metodzie naiwnej wypisuję również wszystkich proponowanych kandydatów).
Metoda naiwna pomimo dość długiego czasu działania, pozwala odnajdować odpowiedzi czasem bliższe (w sensie odległości Levensteina) niż ES i czasem bardziej naturalne dla człowieka.
ES bywa mniej dokładny, ale szybszy i znajduje bardziej różnorodne hasła. 

Looking for correction of 'Agave'...
- [NAIVE] {'Agape'}
- [NAIVE] Best correction:  Agape
- [ES] No correction found :( 
- -> Metoda naiwna znalazła wiarygodne rozwiązanie

Looking for correction of 'ami'...
- [NAIVE] {'rami', 'amią', 'amii', 'agi', 'api', 'ali', 'amia', 'amic', 'nami', 'ai', 'amio', 'mai', 'amię', 'sami', 'kami', 'wami', 'ażi', 'amig', 'mi', 'am', 'amf', 'amin', 'amb', 'asi', 'amie', 'ćmi', 'amid', 'mami', 'ani'}
- [NAIVE] Best correction:  ani
- [ES] abb-ami
- -> Metoda naiwna znalazła wiele sensownych rozwiązań i za poprawne uznała to, które występowało najczęściej - spójnik ani.
- -> ES w wersji AUTO znalazł słowo, które wydaje się dość prawdopodobne, jednak znacznie odleglejsze (w rozumieniu dystansu Levensteina) niż "ani".

Looking for correction of 'anonimizacji'...
- [NAIVE] {'animizacji'}
- [NAIVE] Best correction:  animizacji
- [ES] No correction found :( 
- -> Metoda naiwna znalazła wiarygodne rozwiązanie, jednak w tym wypadku warto zauważyć, że wyraz "anonimizacji" wcale nie musi być faktycznym błędem.

Looking for correction of 'badawczorozwojowych'...
- [NAIVE] ['badawczorozwojowych']
- [NAIVE] No correction found :( 
- [ES] No correction found :( 
- -> Obie metody nie znalazły słowa poprawki i tak naprawdę nie pomyliły się, słowo to istnieje, aczkolwiek chyba częściej pojawia się w formie "badawczo-rozwojowych" bądź "badawczo rozwojowych"

Looking for correction of 'dostosowań'...
- [NAIVE] {'dostosować'}
- [NAIVE] Best correction:  dostosować
- [ES] dostosowali
- -> metody zwróciły różne rozwiązania, ES odleglejsze w sensie Levensteina, obie dość prawdopodobne, do weryfikacji konieczny byłby kontekst

Looking for correction of 'IIb'...
- [NAIVE] {'Izb', 'IIi', 'aIb', 'Ib', 'bIb', 'gIb', 'II'}
- [NAIVE] Best correction:  Izb
- [ES] No correction found :( 
- -> Trudno wyczuć bez kontekstu, jaka odpowiedź jest poprawna, być może chodziło o "rozdział IIb", ale mogło to też być zaproponowane przez algorytm naiwny "Izb" (Izba)

Looking for correction of 'izobutyl'...
- [NAIVE] {'izobutan', 'izobaty', 'izobuten', 'izobutylen'}
- [NAIVE] Best correction:  izobutan
- [ES] izobutan
- -> W tym wypadku mamy do czynienia z terminem chemicznym, obie metody zwróciły tę samą poprawkę
- -> Teoretycznie mogłaby to być literówka od np. "octanu izobutylu", jednak tego znów nie można zweryfikować bez kontekstu (i znajomości chemii).

Looking for correction of 'jed'...
- [NAIVE] {'jen', 'jeb', 'je', 'zjed', 'led', 'jedź', 'jeż', 'ted', 'jem', 'red', 'ed', 'jedz', 'jez', 'jet', 'wed', 'jod', 'jer', 'bed', 'jad', 'ued', 'jej'}
- [NAIVE] Best correction:  jej
- [ES] jad
- -> Obie propozycje są wiarygodne, najwidoczniej każda z metod nieco inaczej wyznacza prawdopodobieństwo wystąpienia słowa.

Looking for correction of 'ktrej'...
- [NAIVE] {'której', 'karej'}
- [NAIVE] Best correction:  której
- [ES] No correction found :( 
- -> To dość zaskakujący wynik, ES nie znalazł nic - w tym wypadku metoda naiwna sprawdziła się lepiej.

Looking for correction of 'naj'...
- [NAIVE] {'daj', 'nar', 'znaj', 'nap', 'nam', 'naw', 'knaj', 'saj', 'gnaj', 'faj', 'naje', 'maj', 'waj', 'taj', 'nas', 'jaj', 'gaj', 'kaj', 'raj', 'njaj', 'na', 'nad', 'aj', 'baj', 'nać', 'haj'}
- [NAIVE] Best correction:  nad
- [ES] hai
- -> Różne odpowiedzi, bez kontektu nieweryfikowalne. 

Looking for correction of 'najmnie'...
- [NAIVE] {'najmniej', 'najemnie', 'najmie', 'najmanie'}
- [NAIVE] Best correction:  najmniej
- [ES] najmanie
- -> Różne odpowiedzi, bez kontektu nieweryfikowalne. 

Looking for correction of 'naliczeń'...
- [NAIVE] {'naliczek', 'zaliczeń'}
- [NAIVE] Best correction:  zaliczeń
- [ES] naliczek
- -> ES wskazał odpowiedź, która również była kandydatem w metodzie naiwnej. Potrzebny kontekst do weryfikacji.

Looking for correction of 'nawodnień'...
- [NAIVE] {'zawodnień'}
- [NAIVE] Best correction:  zawodnień
- [ES] nienawodniająca
- -> Słowo mogło być poprawne, a nie istnieć w słowniku. Obie podpowiedzi mogą nie być poprawne. 

Looking for correction of 'nawozw'...
- [NAIVE] {'nawozi', 'nawozów', 'nawozu', 'nawozy'}
- [NAIVE] Best correction:  nawozu
- [ES] nawozowi
- -> Potrzebny kontekst do ostatecznej weryfikacji. Obie metody zaproponowały słowa o tym samym rdzeniu lecz różnych przypadkach. 

Looking for correction of 'NFOŚiGW'...
- [NAIVE] ['NFOŚiGW']
- [NAIVE] No correction found :( 
- [ES] No correction found :( 
- -> Słowo mogło nie istnieć w słowniku, to skrót.

Looking for correction of 'NUSP'...
- [NAIVE] {'NaSP'}
- [NAIVE] Best correction:  NaSP
- [ES] No correction found :( 
- -> To też mógł być skrót, stąd możliwe, że słusznie ES nie podał żadnej alternatywy. 

Looking for correction of 'odwzorowań'...
- [NAIVE] {'odwzorować'}
- [NAIVE] Best correction:  odwzorować
- [ES] nieodwzorowana
- -> Potrzebny kontekst, ES podał oddleglejszą propozycję. 

Looking for correction of 'ośc'...
- [NAIVE] {'odc', 'ośm', 'ośca', 'oc', 'oś', 'oścu', 'ośce', 'ość', 'ości'}
- [NAIVE] Best correction:  ości
- [ES] ości
- -> Obie metody zgodne.

Looking for correction of 'poddziałań'...
- [NAIVE] {'poddziały', 'poddziałach', 'poddział', 'oddziałaj', 'oddziała', 'podziałam', 'poddziałem', 'oddziałać', 'podziałaś', 'poddziałom', 'podziałaj', 'poddziałami', 'poddziału', 'podziała', 'poddziałów', 'podziałać', 'oddziałam'}
- [NAIVE] Best correction:  poddziały
- [ES] nieoddziałania
- -> Słowo mogło nie istnieć w słowniku, choć wydaje się poprawne po polsku. Obie metody znalazły coś, czego człowiek by przy tym słowie raczej nie zaproponował. 

Looking for correction of 'ponadzakładowym'...
- [NAIVE] {'pozazakładowym'}
- [NAIVE] Best correction:  pozazakładowym
-[ES] No correction found :( 
- -> Słowo mogło nie istnieć w słowniku, chociaż występuje w języku. Metoda naiwna znalazła coś w odległości Levensteina = 3.
- -> Pomimo tego, że słowo jest stosunkowo długie, to metoda naiwna z odległością 3, skutkuje błędem. 

Looking for correction of 'pozaaptecznego'...
- [NAIVE] ['pozaaptecznego']
- [NAIVE] No correction found :( 
- [ES] No correction found :( 
- -> Obie metody zgodne. Słowo istieje w języku polskim. 

Looking for correction of 'ppkt'...
- [NAIVE] {'pkt', 'pakt'}
- [NAIVE] Best correction:  pkt
- [ES] pakcie
- -> Prawdopodobnie obie metody się mylą, człowiek intuicyjnie stwierdziłby, że to skrót od "podpunkt".

Looking for correction of 'próbobiorców'...
- [NAIVE] {'pracobiorców', 'prądobiorców'}
- [NAIVE] Best correction:  pracobiorców
- [ES] No correction found :( 
- -> Słowo może istnieć w języku polskim. Być  może metoda naiwna nie powinna niczego zwrócić, jak ES.

Looking for correction of 'przepisw'...
- [NAIVE] {'przepisz', 'przepisów', 'przepis', 'przepisy', 'przepisu'}
- [NAIVE] Best correction:  przepisów
- [ES] przepisowi
- -> Człowiek, nie znając kontekstu, odczytałby to tak, jak metoda naiwna. 

Looking for correction of 'regazyfikacyjnego'...
- [NAIVE] {'niegazyfikacyjnego', 'denazyfikacyjnego', 'gazyfikacyjnego'}
- [NAIVE] Best correction:  niegazyfikacyjnego
- [ES] No correction found :( 
- -> Słowo istnieje w języku polskim, aczkolwiek w tej formie raczej rzadko. Metoda naiwna znalazła całkiem możliwego kandydata (w odległości 2), jednak prawdopodobnie się pomyliła. 

Looking for correction of 'rekapitalizacyjnej'...
- [NAIVE] {'niekapitalizacyjnej', 'kapitalizacyjnej'}
- [NAIVE] Best correction:  niekapitalizacyjnej
- [ES] No correction found :( 
- -> Analogicznie jak w przypadku powyżej. 

Looking for correction of 'rozmnożeń'...
- [NAIVE] {'rozmnoże'}
- [NAIVE] Best correction:  rozmnoże
- [ES] rozmnoży
- -> Prawdopodobnie to nie jest błąd, ale słowa brak w słowniku. 

Looking for correction of 'sanitarnoepidemiologicznych'...
- [NAIVE] ['sanitarnoepidemiologicznych']
- [NAIVE] No correction found :( 
- [ES] No correction found :( 
- -> Obie metody zgodne. Słowo istnieje w języku polskim, jednak nie ma go w słowniku. 

Looking for correction of 'sposb'...
- [NAIVE] {'sposób'}
- [NAIVE] Best correction:  sposób
- [ES] sposobach
- -> Metoda naiwna wskazała to samo, co zaproponowałby człowiek.

Looking for correction of 'teryto'...
- [NAIVE] {'teryno'}
- [NAIVE] Best correction:  teryno
- [ES] hetyto
- -> Trudno powiedzieć, to mógłby być początek słowa "tery torium" z błędną spacją w środku lub dowolna propozycja którejś z metod. 


###Posumowanie:
Obie metody bywają niedoskonałe. ElasticSearch kosztem precyzji działa szybciej, jednak na pewno lepiej poradzi sobie z wyszukiwaniem słów pokrewnych niż naiwna metoda.
Przy szukaniu błędów w pisowni metoda naiwana czasem zbyt dokładnie wyszukuje i doprowadza to do znajdowania przez nią słów całkiem o przeciwnym znaczeniiu (szczególnie to problematyczne, gdy słowa nie ma w słowniku lub odległość do niego jest zbyt duża).

