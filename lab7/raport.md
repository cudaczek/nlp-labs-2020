# Word embeddings

## Zadania
Rozwiązania zadań znajdują się w pliku lab7.py. 

Wizualizacje wyników metody tSNE można zobaczyć w plikach slowa.png oraz slowa300.png.

## Answer the following questions:
- Compare results for all experiments with respect to the employed models (100 and 300-d)?

W niektóych przypadkach rezultaty różnią się znacząco, jednak często mają sporo wspólnych wyników słów podobnych w czołówce.
W przypadku skrótów ("kpk") o wiele lepiej sobie razi model 300, potrafi rozwinąć w miarę poprawnie ten skrót, model 100 radzi sobie nieco gorzej. 
W przypadku wersji 100d wartości scora znalezionych haseł są zwykle większe niż wartości dla wersji 300d. 


- Compare results for single words and MWEs.

W przypadku MWE prawie zawsze w czołówce słów zwracane są słowa, które są częścią danego MWE.
Natomiast pojedyncze słowa pozwalają na wykrycie sensownych słów posiadających podobne znaczenie do zadanego 
lub będące w silnej relacji do tego słowa. 

- How the results for MWEs could be improved?
Jeśli chce się unikać zwracania dokładnie tych samych słów, warto być może wyeliminować je ze zbioru przeszukiwanego.

- Are the results for albegraic operations biased?

Bywają dość śmieszne rezultaty jak dla "przedszkolanka + mężczyzna - kobieta", które zwraca między innymi słowo "siedmiolatek",
który przedszkole już raczej skończył, ale też na pewno nie jest opiekunem dzieci młodszych w przedszkolu. 
Trudno zresztą się temu dziwić, ponieważ w języku polskim nie ma określenia na "mężczyznę, który wykonuje zawód przedszkolanki",
oba modele były przygotowywane za zbiorze polskich słów i ciężko oczekiwać, żeby zwracały w odpowiedzi nowe/inne słowa.
=> odpowiedź brzmi: tak.

- According to t-SNE: do representations of similar word cluster together?

Generalnie tak, słowa posiadające wyraźne związki znaczeniowe, znajdują się stosunkowo blisko (przynajmniej w przypadku tych zaobserwowanych przykładów),
tworzą mini-klastry.
