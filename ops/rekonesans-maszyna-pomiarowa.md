# Rekonesans maszyny pomiarowej SPEKTRA-1

**Zlecenie:** `ops/DEP-zlecenie-01-rekonesans.md`
**Wykonał:** DEP (Claude Code w terminalu)
**Data:** 2026-07-30, ~09:50
**Charakter:** wyłącznie odczyt. Nic nie instalowano, nie zmieniano, nie aktualizowano.

## Maszyna — jak się do niej dostać

| Pole | Wartość |
|---|---|
| Nazwa hosta | `maszyna-pomiarowa` |
| Adres IP | **`[adres-LAN-A]`** (nie `[adres-LAN-B]` — patrz uwaga niżej) |
| Login SSH | `ssh operator@[adres-LAN-A]` (klucz z `C:\Users\pawel\.ssh\`, bez hasła) |
| Powłoka zdalna | domyślnie `cmd.exe` — PowerShell wołać przez `-EncodedCommand` (cudzysłowia inaczej się gubią) |

**Uwaga o adresie:** dokumentacja `actproof-layercheck\STATUS.md` podaje `[adres-LAN-B]` — ten
adres jest już nieaktualny, port 22 nie odpowiada. Maszyna dostała nowy adres z DHCP routera.
Znalazłem ją skanem podsieci po portach 22 i 11434. Zalecenie: zrobić na routerze rezerwację
DHCP dla tej maszyny, żeby adres nie wędrował między sesjami.

---

## 1. GPU

```
$ nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv
name, memory.total [MiB], driver_version, compute_cap
NVIDIA GeForce RTX 5080, 16303 MiB, 591.86, 12.0

$ nvidia-smi   (nagłówek)
NVIDIA-SMI 591.86     Driver Version: 591.86     CUDA Version: 13.1
|   0  NVIDIA GeForce RTX 5080      WDDM  |  00000000:01:00.0  On |
|  0%   44C    P8    20W / 360W  |  1621MiB / 16303MiB  |  2%  Default |
Procesy na GPU: msedgewebview2.exe, ApplicationFrameHost.exe (tylko desktop, żadnego modelu)
```

**Interpretacja:** RTX 5080 z 16 GB VRAM, architektura Blackwell (compute capability **12.0** =
`sm_120`), sterownik 591.86 obsługuje CUDA do 13.1 — czyli sterownik jest nowy i niczego nie
trzeba w nim ruszać. W momencie pomiaru zajęte było ~1,6 GB VRAM przez pulpit Windows, więc
realnie na model zostaje ~14,5 GB.

## 2. CUDA toolkit

```
$ nvcc --version
'nvcc' is not recognized as an internal or external command,
operable program or batch file.
```

**Interpretacja:** toolkitu CUDA nie ma i **nie jest potrzebny** — koła PyTorcha przywożą własne
biblioteki CUDA, wystarczy sterownik (a ten jest w porządku). Brak `nvcc` nas nie blokuje.

## 3. System, CPU, RAM

```
OS: Microsoft Windows 11 Home | build 26200 | 64-bitowy
CPU: AMD Ryzen 7 9800X3D 8-Core Processor | rdzenie 8 | wątki 16
RAM total: 61,6 GB
RAM wolne: 45,3 GB
```

**Interpretacja:** Windows 11 Home (nie Linux), mocny procesor, 61,6 GB RAM z czego 45 GB wolne —
z zapasem na ładowanie wag i trzymanie hidden_states w pamięci. Jedna rzecz do zapamiętania:
edycja **Home** oznacza brak Hyper-V w pełnej wersji, co ma znaczenie przy Dockerze (punkt 6).

## 4. Dysk

```
C: total 1906,3 GB | wolne 1506,1 GB
(jedna partycja stała, brak innych dysków)
```

**Interpretacja:** 1,5 TB wolnego przy potrzebie 40–60 GB — miejsce nie jest żadnym
ograniczeniem. Partycja robocza to `C:`.

## 5. Python i środowiska

```
$ python --version          => Python 3.14.4
$ py -0p                    => -V:3.14[-64] *  C:\Users\operator\AppData\Local\Python\pythoncore-3.14-64\python.exe
$ python -m pip --version   => pip 26.0.1 (python 3.14)
$ python -m venv --help     => działa (moduł venv obecny)

W PATH: python, python3, py, git (2.54.0), ollama, wsl
BRAK w PATH: pip (jako samodzielna komenda), conda, uv, virtualenv, docker, nvcc

$ python -m pip list
cffi 2.0.0 | cryptography 48.0.0 | idle 1.0.4 | pip 26.0.1 | pycparser 3.0 | pygame-ce 2.5.7
```

**Interpretacja:** jest **jeden** Python i jest to **3.14.4** — nietypowo świeża wersja. `venv`
działa, `pip` trzeba wołać jako `python -m pip`. Globalnie nie ma ani `torch`, ani `transformers`
— środowisko pomiarowe budujemy od zera. Nie ma condy ani uv, więc naturalny wybór to czysty
`venv` + lockfile. **To jest jedyne miejsce, gdzie wersja Pythona ma znaczenie dla T1** —
sprawdziłem u źródła i wygląda dobrze:

- PyPI: `torch` ma koła dla Windows x64 / cp314 **od wersji 2.9.0** (2.6–2.8 mają tylko cp311–cp313).
- Indeks PyTorcha: `torch-2.9.1+cu128-cp314-cp314-win_amd64.whl` istnieje (jest też cu130 i 2.11/2.13).

Czyli ścieżka `Python 3.14 + torch 2.9.1+cu128` jest realna i spełnia wymóg sm_120 (Blackwell
potrzebuje budowy CUDA ≥ 12.8; wersje cu126 i niższe **nie** obsłużą tej karty). Gdybyśmy chcieli
starszego torcha, trzeba by dostawić drugiego Pythona (3.12/3.13) — ale nie widzę po co.

## 6. Docker / WSL2

```
$ docker --version
'docker' is not recognized as an internal or external command, operable program or batch file.

$ wsl --status
Nie zainstalowano Podsystemu Windows dla systemu Linux. Możesz przeprowadzić instalację,
uruchamiając polecenie "wsl.exe --install".

$ wsl -l -v
(to samo — brak zainstalowanych dystrybucji)
```

**Interpretacja:** **Dockera nie ma i WSL2 nie ma.** Sam plik `wsl.exe` istnieje (to standardowy
komponent Windows), ale podsystem nie jest zainstalowany. To jest ta decyzja, którą zlecenie
kazało omówić: pieczęć przez obraz kontenera wymagałaby zainstalowania WSL2 + Docker Desktop na
prywatnym komputerze syna (restart, ~10 GB, zmiana konfiguracji Hyper-V na edycji Home). Ścieżka
`venv + lockfile` nie wymaga na tej maszynie **niczego** poza pobraniem pakietów. Protokół
dopuszcza oba warianty — moja rekomendacja to lockfile.

## 7. Gemma — co już stoi

```
$ ollama list
NAME             ID              SIZE      MODIFIED
qwen2.5:14b      7cdf5a0187d5    9.0 GB    7 weeks ago
gemma4:latest    c6eb396dbd59    9.6 GB    7 weeks ago
gemma3:12b       f4031aab637d    8.1 GB    7 weeks ago

Zajęte miejsce:
C:\Users\operator\.ollama                            => 24,91 GB (modele)
C:\Users\operator\AppData\Local\Programs\Ollama      => 3,00 GB (program)
C:\Users\operator\.cache\huggingface                 => 8,97 GB
   models--google--gemma-3-4b-it       => 8,04 GB  (pliki wag 4,62 GB + 3,39 GB)
   models--Qwen--Qwen2.5-0.5B-Instruct => 0,93 GB
LM Studio: BRAK (sprawdzone 4 typowe lokalizacje — żadna nie istnieje)
Ollama nasłuchuje na porcie 11434 (PID 27092), ale żaden model nie jest teraz w VRAM.
```

**Interpretacja:** dwie niezależne rzeczy. Ollama (3 modele, ~25 GB) jest tam z poprzednich
projektów i do pomiaru się nie nadaje — zgodnie ze zlecenieniem tylko ją inwentaryzuję, nie ruszam.
Natomiast **cache HuggingFace już zawiera wagi `google/gemma-3-4b-it`** (8 GB, w formacie do
`transformers`) — to jest dokładnie ten format, którego potrzebuje pomiar z
`output_hidden_states=True`. Nie ma tam jednak żadnego środowiska Pythona, które by ich używało
(globalnie brak `transformers`), więc wagi są, a narzędzia nie. Warianty większe niż 4B trzeba
będzie dociągnąć.

**Skąd te wagi:** zgodnie z `SOKARIS_ACCESS_INVENTORY.md` (sekcja „HuggingFace — token read-only")
wagi Gemma 3 4B pobrano na tę maszynę **2026-07-03**, po zaakceptowaniu licencji Google na koncie
`Pawelsokaris`. Istnieje dedykowany token read-only o nazwie `actproof-maszyna` (wartość w
inwentarzu, nie powtarzam jej tutaj). Praktyczny wniosek: **bramka licencyjna Gemmy jest już
przejęta** — dociągnięcie innych wariantów Gemmy nie będzie wymagało nowej akceptacji ani nowego
tokenu.

**Uwaga do decyzji o wariancie Gemmy:** 16 GB VRAM minus ~1,6 GB na pulpit daje ~14,5 GB. W bf16
model 4B zajmuje ~8 GB wag, więc zostaje ~6 GB na hidden_states przy 1024 tokenach — mieści się
spokojnie. Wariant 12B w bf16 (~24 GB wag) **nie wejdzie** do 16 GB bez kwantyzacji, a kwantyzacja
psuje sens pomiaru. Jeśli pieczęć ma iść na czymś większym niż 4B, to jest twarde ograniczenie
sprzętowe do przedyskutowania.

## 8. Sieć — dostęp do HuggingFace

```
$ Invoke-WebRequest https://huggingface.co/api/models/google/gemma-3-4b-it
HTTP 200 | długość odpowiedzi 9024

$ Invoke-WebRequest https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/resolve/main/config.json
resolve HTTP 200 | bajtów 659

$ Resolve-DnsName huggingface.co
2600:9000:2436:6c00:17:b174:6d00:93a1  (+2 kolejne, IPv6)

$ Invoke-WebRequest -Method Head https://cdn-lfs.huggingface.co
BŁĄD: Nie można rozpoznać nazwy zdalnej: 'cdn-lfs.huggingface.co'
```

**Interpretacja:** dostęp jest swobodny — i API, i ścieżka `resolve/` (czyli realne pobieranie
plików) zwracają HTTP 200, brak proxy i brak blokady. Nierozpoznana nazwa `cdn-lfs.huggingface.co`
to **nie** problem: HuggingFace dawno przeniósł CDN na inne hosty, a test przez `resolve/` (który
przechodzi przez prawdziwy CDN) zadziałał. Pobranie wag nie jest niczym zagrożone.

---

## Podsumowanie dla decyzji z sekcji „PO CO"

| Decyzja | Co wynika z rekonesansu |
|---|---|
| Wersja PyTorch/CUDA do lockfile'a (T1) | `torch 2.9.1+cu128` (cp314, win_amd64) z indeksu `download.pytorch.org/whl/cu128`. Minimum to CUDA 12.8 — sm_120 wymaga tego progu, starsze budowy karty nie obsłużą. Sterownik 591.86 jest wystarczający, nie ruszać. |
| Wariant Gemmy do pieczęci | 4B bezpiecznie (wagi już są w cache HF). Powyżej 4B w bf16 nie wchodzi w 16 GB VRAM — jeśli protokół wymaga większego modelu, to blokada sprzętowa do omówienia, nie techniczna. |
| Kontener czy venv | **venv + lockfile.** Brak Dockera i brak WSL2 na prywatnym Windows 11 Home; kontener oznaczałby instalację WSL2 + Docker Desktop z restartem maszyny syna. Venv nie wymaga żadnej ingerencji w system. |

## Rzeczy, które trzeba wiedzieć zanim ruszy T1

1. **Adres maszyny jest z DHCP** i już raz się zmienił (`.135` → `.104`). Przed rezerwacją na
   routerze każda sesja musi go najpierw odnaleźć.
2. **Ollama trzyma port 11434 i ~25 GB dysku.** Nie koliduje z pomiarem, ale jeśli będzie
   potrzebne VRAM w całości — trzeba pilnować, żeby żaden model Ollamy nie był załadowany.
3. **Python 3.14 to jedyny interpreter na maszynie.** Ogranicza torcha do ≥2.9.0. Jeśli protokół
   pieczęci wymaga konkretnej starszej wersji torcha, potrzebny będzie drugi Python — czyli
   instalacja, czyli osobne zlecenie i zgoda.
4. **Maszyna jest prywatnym komputerem syna Pawła.** Każda instalacja (pakiety do venv, wagi
   modelu ~8–20 GB) to ingerencja w cudzy sprzęt — warto mieć to explicite ustalone przed T1.
