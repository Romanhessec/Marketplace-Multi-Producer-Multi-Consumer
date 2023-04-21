Nume: Roman Gabriel-Marian
Grupa: 333CBb

1. 
> Tema, presupunand un MPMC in Python, propune probleme in partea de sincronizare
a threadurilor, aici fiind probabil cea mai importanta parte. Astfel, toata partea
de sincronizare am implementat-o in interiorul clasei marketplace, intermediarul
dintre consumatori si producatori, deoarece facea sens atat din punct de vedere logic (implicit, daca avem un intermediar intre consumatori si producatori, este intuitiv ca acesta sa se ocupa si de bunastarea tranzactiei) cat si practic (organizarea codului era mult mai usoara daca marketplace-ul se ocupa de sincronizare). Sistemul de sincronizare presupune un lock care se apeleaza doar in functiile de care este nevoie de sincronizare, respectiv register_producer (trebuie sa ne asiguram ca producatorii primesc un id corect, in ordine), new_cart (acelasi motiv ca la register_producer), add_to_cart (din moment ce efectuez si operatii de stergere din lista, sincronizarea este necesara), remove_from_cart (acelasi motiv) si place_order (pentru printare). Cat despre organizarea datelor, folosesc un dictionar pentru producers (key = id-ul producatorului, value = lista cu produsele publicate de catre respectivul producator) si unul pentru carts (pe aceeasi gandire, key = id-ul cartului, value = lista cu produsele din cos). 

   Pentru implementarea unittestingului, testez in interiorul clasei
TestMarketplace fiecare functie din marketplace, avand grija sa trec exhaustiv prin cazurile posibile. Pentru usurinta, am ales sa las queue_size-ul fiecarui producator de doar 3.

   Pentru logging, conform cerintei, am folosit nivelul info() pentru a loga toate 
intrarile si iesirile din functii, alaturi de parametrii de intrare. Am ales sa logez si mesaje de eroare (erorr()) atunci cand a fost cazul (spre exemplu, se incearca adaugarea in cos a unui produs care nu exista in market). Ca marimea maxima a fisierului, am ales sa folosesc 25000 bytes si am adaugat si 3 fisiere de backup.

> Consider ca tema a fost utila pentru a solidifica concepte de multi-threading si de sincronizare in python cu un tip de aplicatie deja cunoscut (MPMC). De asemenea, am gasit utile si folosirea de unittesting si logging (cel putin ideea de unittesting o sa o mai folosesc si in viitor cu siguranta).

> Consider ca implementarea mea este eficienta, insa am sa imi las un safety net si am sa spun ca se putea si mai bine :).

2. Intregul enunt al temei este implementat. Functionalitati extra nu am, inafara 
de adaugarea si de mesaje de eroare la logging.

3. Resurse utilizate:
   - informatii python in general (bucle, lock-uri, etc): https://ocw.cs.pub.ro/courses/asc/laboratoare/02, https://ocw.cs.pub.ro/courses/asc/laboratoare/03
   - unittesting: https://docs.python.org/3/library/unittest.html, https://stackoverflow.com/questions/3371255/writing-unit-tests-in-python-how-do-i-start, 
   - logging: https://docs.python.org/3/howto/logging.html, https://stackoverflow.com/questions/40088496/how-to-use-pythons-rotatingfilehandler

4. Link github (privat, ofc): https://github.com/Romanhessec/Marketplace-Multi-Producer-Multi-Consumer
