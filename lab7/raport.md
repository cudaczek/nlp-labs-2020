# Word embeddings

## Zadania
Rozwiązania zadań znajdują się w pliku lab7.py. 

Wizualizacje wyników metody tSNE można zobaczyć w plikach slowa.png oraz slowa300.png.

## Answer the following questions:
- Compare results for all experiments with respect to the employed models (100 and 300-d)?


- Compare results for singe words and MWEs.
W przypadku MWE prawie zawsze w czołówce słów zwracane są słowa, które są częścią danego MWE.
Natomiast pojedyncze słowa pozwalają na wykrycie sensownych słów posiadających podobne znaczenie do zadanego 
lub będące w silnej relacji do tego słowa. 

- How the results for MWEs could be improved?
Jeśli chce się unikać zwracania dokładnie tych samych słów, warto być może wyeliminować je ze zbioru przeszukiwanego.

- Are the results for albegraic operations biased?

- According to t-SNE: do representations of similar word cluster together?
Generalnie tak, słowa posiadające wyraźne związki znaczeniowe, znajdują się stosunkowo blisko (przynajmniej w przypadku tych zaobserwowanych przykłądów).
