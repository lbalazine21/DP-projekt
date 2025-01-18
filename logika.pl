labirint([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]).

ispravan_potez(X, Y) :-
    labirint(Labirint),
    nth0(Y, Labirint, Red),
    nth0(X, Red, Vrijednost),
    Vrijednost =:= 0.

pomakni(X, Y, NX, NY) :- NX is X, NY is Y - 1, ispravan_potez(NX, NY). % GORE
pomakni(X, Y, NX, NY) :- NX is X, NY is Y + 1, ispravan_potez(NX, NY). % DOLJE
pomakni(X, Y, NX, NY) :- NX is X - 1, NY is Y, ispravan_potez(NX, NY). % LIJEVO
pomakni(X, Y, NX, NY) :- NX is X + 1, NY is Y, ispravan_potez(NX, NY). % DESNO

bfs([[X, Y, Put] | _], PX, PY, Put) :- X =:= PX, Y =:= PY.
bfs([[X, Y, Put] | Ostalo], PX, PY, FinalniPut) :-
    findall(
        [NX, NY, [[NX, NY] | Put]],
        (pomakni(X, Y, NX, NY), \+ member([NX, NY], Put)),
        SljedeciKoraci
    ),
    append(Ostalo, SljedeciKoraci, NoviRed),
    bfs(NoviRed, PX, PY, FinalniPut).

najkraci_put(StartX, StartY, PX, PY, Put) :-
    bfs([[StartX, StartY, [[StartX, StartY]]]], PX, PY, PutNazad),
    reverse(PutNazad, Put).

kretanje_duha(X, Y, PX, PY, NX, NY) :-
    najkraci_put(X, Y, PX, PY, [[_, _], [NX, NY] | _]).


:- dynamic kljuc_pokupljen/1.

kljuc_pokupljen(false).

pokupi_kljuc :-
    retractall(kljuc_pokupljen(_)),
    assertz(kljuc_pokupljen(true)).

je_li_kljuc_pokupljen(Pokupljen) :-
    kljuc_pokupljen(Pokupljen).


zamrznut(TrenutnoVrijeme, VrijemeZamrzavanja, Rezultat) :-
    TrenutnoVrijeme - VrijemeZamrzavanja =< 3000,
    Rezultat = true.

zamrznut(_, _, Rezultat) :-
    Rezultat = false.


brzina_duha(normalna, Brzina) :-
    Brzina = 20.

brzina_duha(usporena, Brzina) :-
    Brzina = 60.  % Povećan broj koraka između pomaka duha

resetiraj_brzinu(Trenutno, Resetirano) :-
    (Trenutno = usporena -> Resetirano = normalna ; Resetirano = Trenutno).


provjeri_pobjedu(BrojKljuca, UkupnoKljuc, IgracX, IgracY, VrataX, VrataY, pobjeda) :-
    BrojKljuca =:= UkupnoKljuc,
    IgracX =:= VrataX,
    IgracY =:= VrataY.

provjeri_poraz(IgracX, IgracY, DuhX, DuhY, poraz) :-
    IgracX =:= DuhX,
    IgracY =:= DuhY.