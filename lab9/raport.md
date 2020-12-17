# Named Entity Recognition

Kod znajduje się w pliku lab9.py. 

Najdłuższe ustawy zapisane są w pliku largest_bills.json.

W folderach out/ i out_n82/ znajdują się zapisane wyniki przetwarzania tych ustaw przy pomocy Clarin. 

W pliku histogram.png znajduje się wizualizacja częstotliwości wystąpień poszczególnych klas NE.


## Answer the following questions:
### Which of the method (counting expressions with capital letters vs. NER) worked better for the task concerned with identification of the proper names?
Metoda znajdowania wyrażeń z dużych liter pomija nazwy własne rozpoczynające zdanie, co jest pewnym ryzykiem.
Po drugie uwzględnia wyrażenia, które nie są faktycznie nazwą własną, a są np. nazwą rozdziału (I, II, III);
dodatkowo rozbija wyrażenia posiadające znaki specjalne (bo `-`, `,`, `.` nie są z dużej litery).

Obie te metody inaczej zachowują się w kontekście nazw zagnieżdżonych: 
- jeśli wszystkie są z dużej litery i nieoddzielone znakiem specjalnym, to zostaną uznane za jedną nazwę przez pierwszy algorytm,
- NER może rozbić takie wyrażenie na części przypisując fragmenty do różnych klas.

Można powiedzieć, że metoda NER ma lepsze predyspozycje do zwrócenia pełnego, rzeczywistego obrazu wystąpień NE w tekście. 

### What are the drawbacks of the method based on capital letters?
Jak w punkcie wyżej:
- problem nazw własnych na początku zdania
- wymaga dużych liter (czyli zapisanie `Wydział Informatyki i Fizyki` nie zostanie potraktowane jako jedno wyrażenie)
- znajduje wszystko, co jest z dużej litery, nawet jeśli to nie nazwa własna
- nie uwzględnia znaków specjalnych w nazwach własnych
- problem nazw zagnieżdżonych

### What are the drawbacks of the method based on NER?
- problem nazw zagnieżdżonych (nie zawsze chcemy rozbijać na mniejsze części)
- konieczność wytrenowania modelu (otagowanie danych itd.)

### Which of the coarse-grained NER groups has the best and which has the worst results? Try to justify this observation.
Zgodnie z opisem http://clarin-pl.eu/pliki/warsztaty/Wyklad3-inforex-liner2.pdf, powinny się pojawić poniższe klasy:
- nam_adj – przymiotniki pochodzące od nazw własnych, 

W wyniku uzyskane zostały przede wszystkim różne odmiany przymionika "polski" => poprawne, aczkolwiek mało zróżnicowane,
możliwe, że nieco lepiej by było gdyby sprowadzać (przynajmniej w tym przypadku) do form podstawowych.

------------- Top 10 for nam_adj -------------
[('polski', 22),
 ('polskich', 9),
 ('polskiej', 4),
 ('polskim', 4),
 ('polskiego', 3),
 ('Polskiej', 2),
 ('polską', 2),
 ('polscy', 2),
 ('polskimi', 2),
 ('Wojewódzki', 2)]

- nam_eve – wydarzenia organizowane lub ustalone przez ludzi oraz klęski żywiołowe,

W tym wypadku nie znaleziono nawet 10 wyrażeń. Kilka z nich brzmią jak wydarzenia (Święto Śtraży Granicznej,
Narodowy Spis Powszechny, Ochrona Roślin), ale pozostałe zdecydowanie nie.

------------- Top 10 for nam_eve -------------
[('BGŻ SA', 2),
 ('Monitorze Sądowym', 2),
 ('Narodowego Spisu Powszechnego', 1),
 ('Świętem Straży Granicznej', 1),
 ('Generalny Konserwator Zabytków', 1),
 ('Ochrony Roślin', 1)]

- nam_fac – konstrukcje (budowle, budynki, pomniki) stworzone przez ludzi.

Komendant Główny jako budowla nie brzmi za dobrze. Nie znam pomnika NIP, ani REGONU.
Muezea, ZUS i Zakład pasuje do kategorii, Kościół pisany z dużej litery mógł w tekście pierwotnym odnosić się nie tyle do budynku, 
co do wspólnoty religinej => średnio poprawne wyniki.

------------- Top 10 for nam_fac -------------
[('Komendant Główny', 16),
 ('Straży Granicznej', 5),
 ('NIP', 2),
 ('Centralnym Muzeum Pożarnictwa', 2),
 ('Kościoła Ewangelicko - Reformowanego', 1),
 ('Obrony Narodowej', 1),
 ('REGON', 1),
 ('Zakładu', 1),
 ('Muzeum Pożarnictwa', 1),
 ('Kościoła Ewangelicko - Metodystycznego', 1)]

- nam_liv – istoty żywe (ludzie, postacie, zwierzęta),

Jest kilka sensownych wyników i kilka mniej (`Karta Nauczyciela, III, Art, Najwyższego, Gospodarki Morskiej`
 raczej nie można posądzić o bycie istotą żywą).

------------- Top 10 for nam_liv -------------
[('Gospodarki Morskiej', 39),
 ('Straży Granicznej', 11),
 ('Głównego Inspektora', 10),
 ('Art', 8),
 ('Głównym Inspektorem', 5),
 ('Kartograficznym', 4),
 ('III', 4),
 ('Główny Lekarz Weterynarii', 4),
 ('Karta Nauczyciela', 3),
 ('Najwyższego', 3)]


- nam_loc – toponimy (lokalizacje, jednostki geopolityczne i geograficzne),

Większość nazw faktycznie pasuje do tej kategorii. Straż Graniczna pasuje najmniej, ale miasta i państwa poprawne.

------------- Top 10 for nam_loc -------------
[('Rzeczypospolitej Polskiej', 143),
 ('Polsce', 36),
 ('Warszawie', 12),
 ('Warszawy', 11),
 ('Warszawa', 11),
 ('Polski', 8),
 ('Straż Graniczną', 7),
 ('Rzeczpospolita Polska', 6),
 ('Poznaniu', 6),
 ('Wrocławiu', 6)]


- nam_num – wyrażenia liczbowe,

Nie zostały znalezione wcale.

- nam_org – organizacje, instytucje, zespoły, zorganizowane grupy itd.

Wszystkie z Top 10 znalezionych pasują do kategorii.

------------- Top 10 for nam_org -------------
[('Skarbu Państwa', 134),
 ('Urząd Patentowy', 104),
 ('Rada Ministrów', 93),
 ('Minister Spraw Wewnętrznych', 83),
 ('Prezes Rady Ministrów', 61),
 ('Funduszu Pracy', 54),
 ('Skarb Państwa', 44),
 ('Urzędu Patentowego', 41),
 ('Urzędzie Patentowym', 36),
 ('Minister Finansów', 35)]

- nam_oth – nazwy technologii, walut, adres e-mail, strony www, itd.

Minister Edukacji Narodowej oraz Minister Spraw Wewnętrznych nie powinny być zaliczone do nazw technologii.
Pozostałe wyrażenia pasują lepiej, wyrażenia złożone z pauz są prawdopodobnie całkiem nieprzydatne.

------------- Top 10 for nam_oth -------------
[('złotych', 63),
 ('zł', 31),
 ('ECU', 13),
 ('Minister Edukacji Narodowej', 11),
 ('Minister Spraw Wewnętrznych', 5),
 ('PESEL', 3),
 ('Ă - - - - - Ĺ - - - - - - - - - - - - - - - - - - - Ĺ - - - - - - - - - - - - - - - - - - - - - - - -', 2),
 ('FUS', 2),
 ('É - - - - - Â - - - - - - - - - - - - - - - - - - - Â - - - - - - - - - - - - - - - - - - - - - - - -', 1),
 ('Č - - - - - Á - - - - - - - - - - - - - - - - - - - Á - - - - - - - - - - - - - - - - - - - - - - - -', 1)]

- nam_pro – chrematonimy (wytwory ludzkie)

Znalezione wytwory ludzkie pasują do kategorii, są to w sporej części nazwy dokumentów prawnych.

------------- Top 10 for nam_pro -------------
[('Dz . U .', 477),
 ('Kodeksu postępowania administracyjnego', 19),
 ('Kodeksu rodzinnego', 17),
 ('Monitor Polski', 16),
 ('Kodeksu karnego', 16),
 ('Kodeksu postępowania karnego', 15),
 ('Ordynacja podatkowa', 12),
 ('Kodeksu karnego wykonawczego', 11),
 ('Kodeksu postępowania cywilnego', 10),
 ('Kodeksu cywilnego', 7)]


W niektórych przypadkach można mieć spore wątpliwości co do poprawności przypisania do klas.

### Do you think NER is sufficient for identifying different occurrences of the same entity (i.e. consider "USA" and "Stany Zjednoczone" and "Stany Zjednoczone Ameryki Północnej") ? If not, can you suggest an algorithm or a tool that would be able to group such names together?
Prawdopodobie NER znajdzie wszystkie te wyrażenia, jednak nie stwierdzi, że to synonimy. 
W tym celu lepszy byłby mechanizm word2vec lub wordnet. 

### Can you think of a real world problem that would benefit the most from application of Named Entity Recognition algorithm?
- lepsze "rozumienie" tekstów przez komputery
- wsparcie dezambiguacji wyrażeń 
- automatyczne wykrywanie informacji z tekstu 
- klasyfikacja tekstów na bazie częstotliwości wystąpień różnych wyrażeń
- wykrywanie lokalizacji na podstawie wypowiedzi (pomoc dla służb ratunkowych w przypadku, 
gdy osoba zgłaszająca problem, nie umie podać szczegółowej lokalizacji tj. adresu, ale opisuje co widzi)
