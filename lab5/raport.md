# Taggowanie morfosyntaktyczne
# Morphosyntactic tagging

Tagowanie przy pomocy udostępnianych narzędzi wykonywane jest w data_tagger.py. 

Analiza otrzymanych danych z użyciem bigramów wykonywana jest w lab5. 

## Wyniki z zadania 9


#### Sumowane po liczbie wystąpień bigramów 
 [(('prep', 'subst'), 323591),
 
 (('subst', 'subst'), 280316),
 
 (('subst', 'adj'), 273260),
 
 (('adj', 'subst'), 188028),
 
 (('subst', 'prep'), 171005),
 
 (('subst', 'conj'), 84094),
 
 (('conj', 'subst'), 83052),
 
 (('ger', 'subst'), 81237),
 
 (('prep', 'adj'), 79621),
 
 (('prep', 'brev'), 66983)]
 
 
#### Sumowane po liczbie różnych bigramów
[(('subst', 'subst'), 45176),

 (('subst', 'adj'), 26721),
 
 (('adj', 'subst'), 25806),
 
 (('subst', 'fin'), 16060),
 
 (('ger', 'subst'), 15988),
 
 (('prep', 'subst'), 11937),
 
 (('subst', 'prep'), 11269),
 
 (('subst', 'ppas'), 10485),
 
 (('adj', 'fin'), 8705),
 
 (('fin', 'subst'), 8661)]


 #### Kategoria: ('subst', 'subst') -> rzeczownik, rzeczownik
[(('droga', 'subst'), ('rozporządzenie', 'subst')),

 (('skarb', 'subst'), ('państwo', 'subst')),
 
 (('rada', 'subst'), ('minister', 'subst')),
 
 (('terytorium', 'subst'), ('rzeczpospolita', 'subst')),
 
 (('ochrona', 'subst'), ('środowisko', 'subst'))]
 
#### Kategoria: ('subst', 'adj') -> rzeczownik, przymiotnik
[(('minister', 'subst'), ('właściwy', 'adj')),

 (('rzeczpospolita', 'subst'), ('polski', 'adj')),
 
 (('jednostka', 'subst'), ('organizacyjny', 'adj')),
 
 (('samorząd', 'subst'), ('terytorialny', 'adj')),
 
 (('produkt', 'subst'), ('leczniczy', 'adj'))]
 
 
#### Kategoria: ('adj', 'subst') -> przymiotnik, rzeczownik
[(('który', 'adj'), ('mowa', 'subst')),

 (('niniejszy', 'adj'), ('ustawa', 'subst')),
 
 (('następujący', 'adj'), ('zmiana', 'subst')),
 
 (('odrębny', 'adj'), ('przepis', 'subst')),
 
 (('walny', 'adj'), ('zgromadzenie', 'subst'))]
 
#### Kategoria: ('subst', 'fin') -> rzeczownik, forma nieprzeszła
[(('kropka', 'subst'), ('zastępować', 'fin')),

 (('ustawa', 'subst'), ('wchodzić', 'fin')),
 
 (('treść', 'subst'), ('oznaczać', 'fin')),
 
 (('minister', 'subst'), ('określić', 'fin')),
 
 (('zdrowie', 'subst'), ('określić', 'fin'))]
 
#### Kategoria: ('ger', 'subst') -> odsłownik, rzeczownik
[(('pozbawić', 'ger'), ('wolność', 'subst')),

 (('zasięgnąć', 'ger'), ('opinia', 'subst')),
 
 (('wykonywać', 'ger'), ('zawód', 'subst')),
 
 (('zawrzeć', 'ger'), ('umowa', 'subst')),
 
 (('wszcząć', 'ger'), ('postępowanie', 'subst'))]
 
#### Kategoria: ('prep', 'subst') -> przyimek, rzeczownik
[(('z', 'prep'), ('dzień', 'subst')),

 (('na', 'prep'), ('podstawa', 'subst')),
 
 (('do', 'prep'), ('sprawa', 'subst')),
 
 (('w', 'prep'), ('droga', 'subst')),
 
 (('od', 'prep'), ('dzień', 'subst'))]
 
#### Kategoria: ('subst', 'prep') -> rzeczownik, przyimek
[(('mowa', 'subst'), ('w', 'prep')),

 (('ustawa', 'subst'), ('z', 'prep')),
 
 (('wniosek', 'subst'), ('o', 'prep')),
 
 (('dzień', 'subst'), ('od', 'prep')),
 
 (('miesiąc', 'subst'), ('od', 'prep'))]
 
#### Kategoria: ('subst', 'ppas') -> rzeczownik, imiesłów przymiotnikwy bierny
[(('zasada', 'subst'), ('określić', 'ppas')),

 (('brzmienie', 'subst'), ('nadać', 'ppas')),
 
 (('ustawa', 'subst'), ('zmieniać', 'ppas')),
 
 (('czyn', 'subst'), ('zabronić', 'ppas')),
 
 (('warunek', 'subst'), ('określić', 'ppas'))]
 
#### Kategoria: ('adj', 'fin') -> przymiotnik, forma nieprzeszła
[(('obowiązany', 'adj'), ('być', 'fin')),

 (('który', 'adj'), ('wchodzić', 'fin')),
 
 (('publiczny', 'adj'), ('określić', 'fin')),
 
 (('wewnętrzny', 'adj'), ('określić', 'fin')),
 
 (('narodowy', 'adj'), ('określić', 'fin'))]
 
#### Kategoria: ('fin', 'subst') -> forma nieprzeszła, rzeczownik
[(('otrzymywać', 'fin'), ('brzmienie', 'subst')),

 (('podlegać', 'fin'), ('kara', 'subst')),
 
 (('mieć', 'fin'), ('prawo', 'subst')),
 
 (('mieć', 'fin'), ('zastosowanie', 'subst')),
 
 (('zachowywać', 'fin'), ('moc', 'subst'))]

 
 
## Using the results from the previous step answer the following questions:
- What types of bigrams have been found?

Jeśli liczy się sumaryczną liczbę wszystkich wystąpień bigramów należących do danej grupy,
to najwięcej jest wyrażeń przyimek+rzeczownik (faktycznie często używanych w języku polskim).
Jeśli zaś weźmie się pod uwagę liczbę różnych bigramów w danej grupie, 
to dominujące okazują się bigramy rzeczownik+rzeczownik.
W odróżnieniu od codziennego użytku, widać wśród najczęstszych z nich
wyrażenia związane mocno z tekstami o charakterze prawniczym.


- Which of the category-pairs indicate valuable multiword expressions? Do they have anything in common?
Najczęściej występujące pary kategorii zawierają dwa rzeczowniki lub rzeczownik z przymiotnikiem.
Wyniki wskazują na to, że wielowyrazowe wyrażenia zawierają najczęściej rzeczownik (subst),
czyli opisują jakąś rzecz, obiekt, instytucję.


- Which signal: LLR score or syntactic category is more useful for determining genuine multiword expressions?
Jeśli uwzględnione zostanie tylko jeden z tych, wyniki nie będą zbyt dobre:
sam LLR score (jak to już było pokazane na poprzednich labach) uwypukli znaczenie wyrażeń klasycznych dla profilu tekstu,
jednak będą to przede wszystkim wyrażenia zawierające przyimki i spójniki (używane sformułowania);
a same kategorie bez żadnego sortowania da długą listę tych wyrażeń bez konkretów.
Połączenie LLR score i kategorii syntaktycznych daje szansę wykrywać wyrażenia charakterystyczne dla danej dziedziny 
(w naszym przypadku prawniczej) - nazw własnych.


Can you describe a different use-case where the morphosyntactic category is useful for resolving a real-world problem?
 - tłumaczenia - kategorie morfosntaktyczne mogą pomagać rozróżniać różne znaczenia pojedynczego słowa
 - wyszukiwanie wyrażeń - można wykrywać najistotniejsze słowo, do którego pozostałe się odnoszą
 - transkrypcja tekstów - czasem wymowa zależy od kategorii gramatycznej
 - wykrywanie pojęć dziedzinowych (oczywiście przy użyciu dodatkowych narzędzi)
 