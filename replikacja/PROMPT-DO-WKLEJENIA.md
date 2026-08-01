# Do przekazania właścicielowi maszyny (jedna wiadomość)

*Poniższy tekst wystarczy wysłać. Człowiek wkleja go swojemu Claude Code
i wraca do swoich spraw.*

---

Cześć! Prośba na jakieś 10 minut Twojej uwagi (reszta dzieje się sama).

Prowadzimy prerejestrowane badanie naukowe nad modelami językowymi i chcemy
sprawdzić, czy Twoja maszyna nadaje się do powtórzenia naszych pomiarów.
To na razie **tylko test sprzętu**, nie sam pomiar — kilkanaście minut liczenia
plus pobranie 8 GB modelu.

Wklej to swojemu Claude Code i zatwierdzaj, o co poprosi:

> Sklonuj https://github.com/pawelsokaris-sudo/spektra1 i przeczytaj plik
> `replikacja/README-DLA-AGENTA.md` — to instrukcja napisana dla Ciebie.
> Najpierw pokaż mi `replikacja/DLA-WLASCICIELA-MASZYNY.md`, bo chcę wiedzieć,
> co będzie się liczyć na moim komputerze. Potem wykonaj kwalifikację sprzętu
> według instrukcji, samodzielnie rozstrzygając wszystko, co jest w Twoim
> zakresie. Angażuj mnie wyłącznie tam, gdzie instrukcja to wyraźnie
> przewiduje. Na końcu odeślij wynik tak, jak opisuje sekcja o odsyłaniu.

Twój Claude może poprosić Cię o dwie rzeczy: zgodę na zajęcie ~10 GB dysku
oraz — jeśli tak wyjdzie — o jedno kliknięcie akceptacji licencji modelu
Gemma na huggingface.co. Poza tym nie powinien Cię o nic pytać; jeśli pyta,
to znaczy, że nasza instrukcja jest niedopracowana i chętnie o tym usłyszymy.

Z Twojej maszyny wychodzi wyłącznie raport techniczny: model procesora, ilość
pamięci, wersje bibliotek, czasy i wyniki testów numerycznych. Żadnego kodu,
żadnych plików, żadnych danych osobowych. Repozytorium jest publiczne, badanie
też — możesz wszystko podejrzeć przed uruchomieniem.

Jeśli chcesz sam sprawdzić, co to właściwie robi — wszystko jest opisane
po ludzku w `replikacja/DLA-WLASCICIELA-MASZYNY.md` w tym repo: co badamy,
co liczy Twój komputer, co z niego wychodzi, jak zatrzymać, jak odinstalować.
W dowolnej chwili `python -m replikacja.stan` pokaże, na jakim etapie jesteśmy.

Nic nie startuje samo, nic nie działa w tle, nic nie wysyła się bez komendy.

Jeśli test wypadnie negatywnie, to też jest dobry wynik — o to w nim chodzi.
