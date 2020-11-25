# Słowosieć
# Wordnet

Kod w całości znajduje się w pliku lab6.py.

### zadanie 4
Diagram hiperonimów dla "wypadku drogowego" zapisany jako plik wypadek_drogowy.png.

### zadanie 7
Wykresy dla grup słów znajdują się odpowiednio dla grupy pierwszej i drugiej w plikach analiza_relacji_{[a|b]}.png.

## Wyniki z zadania 9
Questions/problems:
### What is the necessary step to use the knowledge from dictionaries such as WordNet?
Konieczne jest zbudowanie takiego słownika, czyli uzupełnienie definicji, relacji etc.
W momencie, kiedy są już gotowe zasoby WordNetu, konieczna jest świadomość, że są tutaj słowa w formie podstawowej, nieodmienionej, 
a zatem potrzeba lematyzacji na słowa/wyrażenia, potrzeba poprawy literówek i konieczna jest dezambiguacja słów.
Jeżeli chodzi o polską słowosieć relacje są lepiej uzupełnione niż definicje, 
stąd istotne jest rozumienie relacji, jakie mogą zachodzić.

### Assess the value of WordNet as a resource for representing the sense of sentences (not words in isolation).
Z jednej strony możliwość korzystania z relacji między słowami wydaje się sugerować, że można lepiej pojąć sens połączonych słów, 
jednak z drugiej strony w zdaniu niezwykle istotne jest wyszczególnienie słów najważniejszych (czyli podmiotu i orzeczenia). 
Sama analiza relacji nie wskaże ważności poszczególnych słów, które wpływają na sens wypowiedzi.

Znaczenia trudniej określić niż kategorię syntaktyczną, jest o wiele więcej możliwości znaczeń niż kategorii.

Do tego dochodzi problem metaforycznego używania niektórych słów - takie znaczenie może się nie znajdować w WordNecie, 
trudno przewidzieć sens jeśli nie ma się szerszej wiedzy o świecie; 
utrudnieniem mogą być wyrażenia wielosegmentowe, które też nie wszystkie muszą się w słowosieci znajdować.

Gdyby chodziło o zamianę słów na synonimy, alborytm korzystający z WordNetu, by sobie prawdopodobnie poradził,
jednak nie oznacza to, że znałby sens.

### Discuss the problmes comming from using structured knowledge resources such as WordNet.
Przede wszystkim WordNet jest od początku do końca tworzony przez ludzi i wymaga ręcznego opisu każdego pojęcia i relacji pomiędzy słowami. 
Języki w większości są żywe i nieustannie zachodzą zmiany znaczeń, pojawiają się nowe słowa, zanikają stare.
To w połączeniu z koniecznością ręcznego uzupełniania słownika, sprawia, że jest on dość ograniczony.

Wymaga wcześniejszego ujednoznaczniania słów, bo bez tego nie ma jak korzystać z WordNetu.
Nie ma podanej częstości występowania słów, to trochę ogranicza możliwości w zakresie rozpoznawania znaczenia. 

Relacje nie jest też łatwo przedstawić jako wektor opisujący słowa, który by mógł przydać się w uczeniu maszynowym.

