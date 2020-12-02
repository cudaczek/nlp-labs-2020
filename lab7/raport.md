# Word embeddings

## Zadania
Rozwiązania zadań znajdują się w pliku lab7.py. 

Wizualizacje wyników metody tSNE można zobaczyć w plikach slowa.png oraz slowa300.png.

## Answer the following questions:
- Compare results for all experiments with respect to the employed models (100 and 300-d)?
W niektóych przypadkach rezzultaty różnią się znacząco, jednak często mają sporo wspólnych wyników w czołówce znalezionych słów podobnych.
W przypadku skrótów ("kpk") o wiele lepiej sobie razi model 300, potrafi rozwinąć w miarę poprawnie ten skrót, model 100 radzi sobie nieco gorzej. 
W przypadku 100 wartości scora znalezionych haseł są zwykle większe niż wartości dla wersji 300. 


- Compare results for singe words and MWEs.
W przypadku MWE prawie zawsze w czołówce słów zwracane są słowa, które są częścią danego MWE.
Natomiast pojedyncze słowa pozwalają na wykrycie sensownych słów posiadających podobne znaczenie do zadanego 
lub będące w silnej relacji do tego słowa. 

- How the results for MWEs could be improved?
Jeśli chce się unikać zwracania dokładnie tych samych słów, warto być może wyeliminować je ze zbioru przeszukiwanego.

- Are the results for albegraic operations biased?
Wyraźnie inne wyniki można uzyskać korzystając ze sposobu z liczeniem średniej niż przy podziale słów na posiives/negatives.
Bywają dość śmieszne rezultaty jak dla "przedszkolanka + mężczyzna - kobieta", które zwraca między innymi słowo "siedmiolatek",
który przedszkole już raczej skończył, ale też na pewno nie jest opiekunek dzieci młodszych w przedszkolu. 

- According to t-SNE: do representations of similar word cluster together?
Generalnie tak, słowa posiadające wyraźne związki znaczeniowe, znajdują się stosunkowo blisko (przynajmniej w przypadku tych zaobserwowanych przykłądów).
