# DEP — Zlecenie 02: Środowisko pomiarowe na maszynie operatora maszyny

> **STATUS: ZATWIERDZONE DO WYKONANIA.**
> Paweł wyraził zgodę wprost 2026-07-30 („tak zgoda jest, komp czeka").
> Zgoda obejmuje instalację środowiska Pythona (~3 GB) w katalogu wymienionym niżej.
> Zakres zmian jest zamknięty listą z sekcji poniżej — cokolwiek poza nią wymaga nowej zgody.

**Maszyna:** `maszyna-pomiarowa`, `operator@[adres-LAN-A]` (adres z DHCP — patrz zlecenie 01)
**Cel:** domknąć T1 (środowisko + lockfile) i przygotować grunt pod T2 (semantyka warstw).

## Zakres zmian na maszynie (pełna lista — nic poza tym)

1. Nowy katalog `C:\Users\operator\spektra1-env\` z wirtualnym środowiskiem Pythona.
2. Pakiety pobrane do tego środowiska (~3 GB) — **poza** środowiskiem nic się nie zmienia.
3. Żadnych zmian w systemie, rejestrze, PATH, sterownikach, Ollamie ani w cache HuggingFace.

## Kroki

### 0. Test taniej wygody (przy okazji, 5 sekund)
```
ssh operator@maszyna-pomiarowa "echo OK"
```
Jeśli działa — w przyszłości łączymy się po nazwie i zmiany adresu przestają mieć
znaczenie (Paweł ma sieć meshową, rezerwacja DHCP odrzucona jako niewarta zachodu).
Jeśli nie działa — nic się nie dzieje, zostaje adres IP.

### 1. Środowisko
```
python -m venv C:\Users\operator\spektra1-env
C:\Users\operator\spektra1-env\Scripts\python.exe -m pip install --upgrade pip
```

### 2. PyTorch pod Blackwell (sm_120)
```
C:\Users\operator\spektra1-env\Scripts\python.exe -m pip install ^
  torch==2.9.1+cu128 --index-url https://download.pytorch.org/whl/cu128
```
Wersja wymuszona dwoma niezależnymi ograniczeniami z rekonesansu: Python 3.14
(koła dopiero od torch 2.9) oraz RTX 5080 = Blackwell (CUDA ≥ 12.8).

### 3. Reszta stosu
```
C:\Users\operator\spektra1-env\Scripts\python.exe -m pip install ^
  transformers accelerate numpy scipy pyarrow pandas safetensors
```

### 4. Lockfile (wchodzi do pieczęci)
```
C:\Users\operator\spektra1-env\Scripts\python.exe -m pip freeze > requirements-lock.txt
```
Zawartość przekaż w raporcie — plik trafia do repo jako część pakietu pieczęci.

### 5. Weryfikacja sprzętu i precyzji
```python
import torch
print("torch", torch.__version__, "cuda", torch.version.cuda)
print("dostepna:", torch.cuda.is_available(), "|", torch.cuda.get_device_name(0))
print("compute capability:", torch.cuda.get_device_capability(0))   # oczekiwane (12, 0)
print("bf16:", torch.cuda.is_bf16_supported())
print("VRAM total GB:", round(torch.cuda.get_device_properties(0).total_memory/2**30, 2))
```

### 6. Test wczytania modelu i ukrytych stanów (sedno T2)
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
name = "google/gemma-3-4b-it"
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(name, dtype=torch.bfloat16, device_map="cuda:0")
model.eval()
ids = tok("Test pomiaru ukrytych stanow.", return_tensors="pt").to("cuda:0")
with torch.no_grad():
    out = model(**ids, output_hidden_states=True)
print("liczba elementow hidden_states:", len(out.hidden_states))
print("ksztalt pojedynczego:", tuple(out.hidden_states[0].shape))
print("dtype:", out.hidden_states[0].dtype)
print("VRAM zajete GB:", round(torch.cuda.max_memory_allocated()/2**30, 2))
print("rewizja/commit:", getattr(model.config, "_commit_hash", "brak"))
```

### 7. Sumy kontrolne wag (do pieczęci)
Wypisz ścieżkę snapshotu w cache HF oraz SHA-256 każdego pliku `.safetensors`
i plików tokenizera. To wchodzi wprost do `config.yaml` w polach `TBD-RECON`.

## Weryfikacja (co ma być w raporcie)

Raport `ops/srodowisko-pomiarowe.md` z surowym wyjściem każdego kroku. Krytyczne
punkty do potwierdzenia: `compute capability (12, 0)`, `bf16: True`, liczba elementów
`hidden_states` (dla modelu o L blokach oczekiwane L+1 — pierwszy to embedding),
szczytowe zużycie VRAM przy jednym krótkim tekście, oraz pełny lockfile.

**Jeśli którykolwiek krok padnie — STOP i raport.** Nie obchodź problemu instalacją
czegokolwiek spoza tej listy (np. innego Pythona) bez nowej zgody.

## Rollback

Usunięcie katalogu `C:\Users\operator\spektra1-env\`. Nic poza nim nie zostało dotknięte,
więc to przywraca maszynę do stanu sprzed zlecenia. Cache HuggingFace zostaje
nienaruszony (wagi były tam już przed nami, od 2026-07-03).

## Uwaga operacyjna

Przed testem modelu upewnić się, że żaden model Ollamy nie jest załadowany do VRAM
(`ollama ps`). Ollamy nie zatrzymywać — wystarczy, żeby nie trzymała modelu w pamięci.
