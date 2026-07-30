# DEP — Zlecenie 01: Rekonesans maszyny pomiarowej SPEKTRA-1

**Od:** chat prowadzący SPEKTRA-1
**Maszyna:** komputer syna Pawła z kartą RTX (dostęp SSH — dane dostępowe ma Paweł/DEP)
**Charakter:** WYŁĄCZNIE ODCZYT. Niczego nie instalować, nie zmieniać, nie aktualizować.

## CO (komendy i co mają odpowiedzieć)

1. **GPU:** `nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv`
   → dokładny model karty, VRAM, sterownik, compute capability.
2. **CUDA toolkit (jeśli jest):** `nvcc --version` (brak = też ważna informacja).
3. **System:** wersja OS (Windows/Linux?), RAM (`free -h` lub `systeminfo`), CPU.
4. **Dysk:** wolne miejsce na partycji roboczej (potrzebujemy ~40–60 GB na wagi
   modelu + obraz kontenera + cache HF + wyniki parquet).
5. **Python:** `python --version` / `python3 --version`; czy jest conda/venv/uv.
6. **Docker:** `docker --version`; czy działa z GPU (`docker info` — nvidia runtime?).
   Na Windows: czy jest WSL2.
7. **Gemma — jak jest postawiona:** `ollama list` (jeśli Ollama), katalogi LM Studio,
   `~/.cache/huggingface/` — czy są już jakieś wagi HF i które.
   KONTEKST: pomiar wymaga wag HF przez `transformers` z `output_hidden_states=True`;
   Ollama NIE nadaje się do pomiaru. Istniejąca instalacja nas nie blokuje — chcemy
   tylko wiedzieć, co tam jest i ile miejsca zajmuje.
8. **Sieć:** czy maszyna ma swobodny dostęp do huggingface.co (pobranie wag).

## GDZIE

Wynik zapisz jako `ops/rekonesans-maszyna-pomiarowa.md` w repo
`C:\Users\pawel\projects\spektra1` (albo przekaż Pawłowi tekst raportu do wklejenia).

## WERYFIKACJA

Raport zawiera wszystkie 8 punktów; przy każdym surowe wyjście komendy + jedno
zdanie interpretacji. Braki (np. nie ma Dockera) to poprawna odpowiedź, nie błąd.

## ROLLBACK

Nie dotyczy — zlecenie nie zmienia stanu maszyny.

## PO CO (kontekst decyzji, które od tego zależą)

- wersja PyTorch/CUDA do lockfile'a i kontenera (T1) — zależy od karty i sterownika,
- wybór wariantu Gemmy do pieczęci — zależy od VRAM (bf16 + hidden_states 1024 tok.),
- czy pomiar pójdzie w kontenerze Docker czy w venv z lockfile (protokół dopuszcza
  pieczęć lockfile + obraz kontenera; bez Dockera na maszynie trzeba to omówić).
