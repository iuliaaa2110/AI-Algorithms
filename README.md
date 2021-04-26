# AI-Algorithms
 UCS, AStar and IDAStar implementation for the Inundation Problem



Problema Inundație

Considerăm o hartă dreptunghiulară cu M linii și N coloane. În hartă avem două tipuri de simboluri:

simbolul hash # - semnifică un obstacol
litera mică 'o' - semnifică un loc liber
Pe hartă există un robinet și un canal de scurgere (afișate cu bold mai sus). Dorim să eliminăm cu cost minim un număr de obstacole, astfel încât să ajungă apa de la robinet la canal. Numim "zonă" o colecție maximală de locuri libere (litere ‘o’) cu proprietatea că oricare două locuri libere sunt conectate (două locuri libere sunt conectate dacă există un drum care le leagă și care merge numai pe linie si coloană, nu și pe diagonală). Considerăm că zona în care se află robinetul este inundată. Pe măsură ce eliminăm obstacole, zona inundată se extinde. Dorim să eliminăm cu cost minim un număr de obstacole astfel încât zona inundată să se extindă până la canal și astfel apa să se scurgă (robinetul și canalul să fie în aceeași zonă).

Stări și tranziții. Cost.
O stare e dată de situația obstacolelor și a apei de pe hartă. O mutare reprezintă eliminarea unui obstacol. Deci, un succesor reprezintă o configurație nouă a hărții obținută prin unirea mai multor zone. Costul unui obstacol e 1+(numarul de obstacole imediat vecine pe linie,coloana si diagonala din jurul lui) - considerăm practic că e mai greu de dat jos cu cât e mai înconjurat de alte obstacole.

Fisierul de intrare
Programul citește din fișier:

coordonatele robinetului (linia și coloana pe care se află)
coordonatele canalului (linia și coloana)
harta (memorată sub formă de matrice)
Evident, nici robinetul și nici canlul nu se află într-o celulă cu obstacol.

Exemplu de fișier de intrare:

selecteaza textul
0 0
5 4
oooo#ooo#
##o#####o
o##oo#ooo
##oo#o#o#
oo###o##o
o###o##oo
Indicație: puteți face o preprocesare a datelor, marcând zonele din hartă (toate celulele din matrice corespunzând aceleiași zone au asociate numere identice)

.
Fișier output.
Fisierul de output va cuprinde stările hărții. Zona inundată va fi afișată cu i. Primul nod conține deja zona inundată de robinet.

1)
iiii#ooo#
##i#####o
o##oo#ooo
##oo#o#o#
oo###o##o
o###o##oo

Eliminăm obstacolul de la (1,3).
2)
iiii#ooo#
##ii####o
o##ii#ooo
##ii#o#o#
oo###o##o
o###o##oo
...






Barem (punctajul e dat in procentaje din punctajul maxim al temei; procentajul maxim este 100%):

(5%)Fișierele de input vor fi într-un folder a cărui cale va fi dată în linia de comanda. În linia de comandă se va da și calea pentru un folder de output în care programul va crea pentru fiecare fișier de input, fișierul sau fișierele cu rezultatele. Tot în linia de comandă se va da ca parametru și numărul de soluții de calculat (de exemplu, vrem primele NSOL=4 soluții returnate de fiecare algoritm). Ultimul parametru va fi timpul de timeout. Se va descrie în documentație forma în care se apelează programul, plus 1-2 exemple de apel.
(5%) Citirea din fisier + memorarea starii. Parsarea fișierului de input care respectă formatul cerut în enunț
(15%) Functia de generare a succesorilor
(5%) Calcularea costului pentru o mutare
(10%) Testarea ajungerii în starea scop (indicat ar fi printr-o funcție de testare a scopului)
(15% = 2+5+5+3 ) 4 euristici:
(2%) banala
(5%+5%) doua euristici admisibile posibile (se va justifica la prezentare si in documentație de ce sunt admisibile)
(3%) o euristică neadmisibilă (se va da un exemplu prin care se demonstrează că nu e admisibilă). Atenție, euristica neadmisibilă trebuie să depindă de stare (să se calculeze în funcție de valori care descriu starea pentru care e calculată euristica).
(10%) crearea a 4 fisiere de input cu urmatoarele proprietati:
un fisier de input care nu are solutii
un fisier de input care da o stare initiala care este si finala (daca acest lucru nu e realizabil pentru problema, aleasa, veti mentiona acest lucru, explicand si motivul).
un fisier de input care nu blochează pe niciun algoritm și să aibă ca soluții drumuri lungime micuță (ca să fie ușor de urmărit), să zicem de lungime maxim 20.
un fisier de input care să blocheze un algoritm la timeout, dar minim un alt algoritm să dea soluție (de exemplu se blochează DF-ul dacă soluțiile sunt cât mai "în dreapta" în arborele de parcurgere)
dintre ultimele doua fisiere, cel putin un fisier sa dea drumul de cost minim pentru euristicile admisibile si un drum care nu e de cost minim pentru cea euristica neadmisibila
(15%) Pentru cele NSOL drumuri(soluții) returnate de fiecare algoritm (unde NSOL e numarul de soluții dat în linia de comandă) se va afișa:
numărul de ordine al fiecărui nod din drum
lungimea drumului
costului drumului
timpul de găsire a unei soluții (atenție, pentru soluțiile de la a doua încolo timpul se consideră tot de la începutul execuției algoritmului și nu de la ultima soluție)
numărul maxim de noduri existente la un moment dat în memorie
numărul total de noduri calculate (totalul de succesori generati; atenție la DFI și IDA* se adună pentru fiecare iteratie chiar dacă se repetă generarea arborelui, nodurile se vor contoriza de fiecare dată afișându-se totalul pe toate iterațiile
între două soluții de va scrie un separator, sau soluțiile se vor scrie în fișiere diferite.
Obținerea soluțiilor se va face cu ajutorul fiecăruia dintre algoritmii studiați:

Pentru studenții de la seria CTI problema se va rula cu algoritmii: BF, DF, DFI, UCS, Greedy, A*.
Pentru studenții din seriile Mate-Info și Informatică, problema se va rula cu algoritmii: UCS, A* (varianta care dă toate drumurile), A* optimizat (cu listele open și closed, care dă doar drumul de cost minim), IDA*.
Pentru toate variantele de A* (cel care oferă toate drumurile, cel optimizat pentru o singură soluție, și IDA*) se va rezolva problema cu fiecare dintre euristici. Fiecare din algoritmi va fi rulat cu timeout, si se va opri daca depășește acel timeout (necesar în special pentru fișierul fără soluții unde ajunge să facă tot arborele, sau pentru DF în cazul soluțiilor aflate foarte în dreapta în arborele de parcurgere).
(5%) Afisarea in fisierele de output in formatul cerut
(5%) Validări și optimizari. Veți implementa elementele de mai jos care se potrivesc cu varianta de temă alocată vouă:
găsirea unui mod de reprezentare a stării, cât mai eficient
verificarea corectitudinii datelor de intrare
găsirea unor conditii din care sa reiasă că o stare nu are cum sa contina in subarborele de succesori o stare finala deci nu mai merita expandata (nu are cum să se ajungă prin starea respectivă la o stare scop)
găsirea unui mod de a realiza din starea initială că problema nu are soluții. Validările și optimizările se vor descrie pe scurt în documentație.
(5%) Comentarii pentru clasele și funcțiile adăugate de voi în program (dacă folosiți scheletul de cod dat la laborator, nu e nevoie sa comentați și clasele existente). Comentariile pentru funcții trebuie să respecte un stil consacrat prin care se precizează tipul și rolurile parametrilor, căt și valoarea returnată (de exemplu, reStructured text sau Google python docstrings).
(5%) Documentație cuprinzând explicarea euristicilor folosite. În cazul euristicilor admisibile, se va dovedi că sunt admisibile. În cazul euristicii neadmisibile, se va găsi un exemplu de stare dintr-un drum dat, pentru care h-ul estimat este mai mare decât h-ul real. Se va crea un tabel în documentație cuprinzând informațiile afișate pentru fiecare algoritm (lungimea și costul drumului, numărul maxim de noduri existente la un moment dat în memorie, numărul total de noduri). Pentru variantele de A* vor fi mai multe coloane în tabelul din documentație: câte o coloană pentru fiecare euristică. Tabelul va conține datele pentru minim 2 fișiere de input, printre care și fișierul de input care dă drum diferit pentru euristica neadmisibilă. În caz că nu se găsește cu euristica neadmisibilă un prim drum care să nu fie de cost minim, se acceptă și cazul în care cu euristica neadmisibilă se obțin drumurile în altă ordine decât crescătoare după cost, adică diferența să se vadă abia la drumul cu numărul K, K>1). Se va realiza sub tabel o comparație între algoritmi și soluțiile returnate, pe baza datelor din tabel, precizând și care algoritm e mai eficient în funcție de situație. Se vor indica pe baza tabelului ce dezavantaje are fiecare algoritm.
Doar pentru studenții de la seria CTI: se dă bonus 10% pentru implementarea Greedy și analizarea acestuia împreună cu ceilalți algoritmi.
Doar pentru studenții de la seria CTI: se dă bonus câte 10% pentru fiecare dintre următoarele optimizări pentru cazul în care se cere o singură soluție (deci în program veți avea un if care verifică dacă numărul inițial de soluții cerut era 1):
la BF să se returneze drumul imediat ce nodul scop a fost descoperit, și nu neapărat când ajunge primul în coadă
la UCS+A* (bonusul ar fi 10%+10% dacă se face pt ambele) să nu avem duplicate ale informației din noduri în coadă. În cazul în care tocmai dorim să adăugăm un nod în coadă și vedem că există informația lui deja, păstram în coadă, dintre cele 2 noduri doar pe cel cu costul cel mai mic
