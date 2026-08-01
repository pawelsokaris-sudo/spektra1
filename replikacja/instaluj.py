"""Instalator srodowiska replikacji SPEKTRA-1 (uruchamia agent, nie czlowiek).

Tworzy wirtualne srodowisko i instaluje ZAMROZONE wersje bibliotek. Agent
prowadzacy replikacje NIE dobiera wersji sam - roznica w narzedziu unieważnia
porownywalnosc pomiarow.

    python replikacja/instaluj.py

Idempotentny: ponowne uruchomienie tylko weryfikuje. Nic nie instaluje
globalnie, nie tworzy uslug, nie uruchamia niczego w tle.
"""

import json
import platform
import subprocess
import sys
import venv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VENV = REPO / ".venv-spektra"
REQ = Path(__file__).resolve().parent / "requirements-replikacja.txt"
RAPORT = Path(__file__).resolve().parent / "RAPORT-INSTALACJA.json"


def python_z_venv():
    return VENV / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")


def uruchom(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def main():
    if sys.version_info < (3, 11):
        print(f"STOP: potrzebny Python 3.11+, jest {platform.python_version()}.\n"
              f"Agencie: zainstaluj nowszego Pythona (pyenv/brew/oficjalny instalator)\n"
              f"i uruchom ten skrypt ponownie. Nie angazuj w to operatora maszyny.")
        return 1

    if not VENV.exists():
        print(f"[instalacja] tworze srodowisko: {VENV}", flush=True)
        venv.EnvBuilder(with_pip=True).create(VENV)
    py = python_z_venv()

    print("[instalacja] instaluje ZAMROZONE wersje (to potrwa kilka minut)", flush=True)
    r = uruchom([str(py), "-m", "pip", "install", "--quiet", "--upgrade", "pip"])
    r = uruchom([str(py), "-m", "pip", "install", "--quiet", "-r", str(REQ)])
    if r.returncode != 0:
        print("[instalacja] BLAD instalacji:\n" + (r.stderr or "")[-2000:])
        print("\nAgencie: jesli to konflikt wersji dla tej platformy, ZAPISZ to\n"
              "w raporcie i zakoncz. Nie podmieniaj wersji na wlasna reke -\n"
              "zamrozone wersje sa czescia protokolu.")
        return 1

    kod = ("import json,platform,importlib.metadata as m;"
           "pk=['torch','transformers','accelerate','tokenizers','huggingface_hub',"
           "'safetensors','numpy','scipy','pandas','pyarrow','PyYAML'];"
           "d={p:(m.version(p) if True else None) for p in pk};"
           "import torch;"
           "d['_python']=platform.python_version();"
           "d['_system']=platform.platform();"
           "d['_cuda']=torch.cuda.is_available();"
           "d['_mps']=bool(getattr(torch.backends,'mps',None) and torch.backends.mps.is_available());"
           "print(json.dumps(d))")
    r = uruchom([str(py), "-c", kod])
    if r.returncode != 0:
        print("[instalacja] BLAD weryfikacji:\n" + (r.stderr or "")[-1500:])
        return 1
    info = json.loads(r.stdout.strip().splitlines()[-1])

    oczekiwane = {}
    for linia in REQ.read_text(encoding="utf-8").splitlines():
        linia = linia.strip()
        if linia and not linia.startswith("#") and "==" in linia:
            k, v = linia.split("==")
            oczekiwane[k] = v

    zgodne, rozjazd = True, []
    for pakiet, wersja in oczekiwane.items():
        jest = info.get(pakiet, "BRAK")
        if pakiet == "torch":
            ok = jest.split("+")[0] == wersja        # sufiks platformowy dozwolony
        else:
            ok = jest == wersja
        if not ok:
            zgodne = False
            rozjazd.append(f"{pakiet}: jest {jest}, oczekiwano {wersja}")

    urzadzenie = "cuda" if info["_cuda"] else ("mps" if info["_mps"] else "cpu")
    wynik = {"zgodne_wersje": zgodne, "rozjazd": rozjazd, "urzadzenie": urzadzenie,
             "wersje": info, "venv": str(VENV)}
    RAPORT.write_text(json.dumps(wynik, indent=2), encoding="utf-8")

    print(f"[instalacja] Python {info['_python']} | {info['_system']}")
    print(f"[instalacja] urzadzenie obliczeniowe: {urzadzenie}")
    print(f"[instalacja] wersje zamrozone: {'ZGODNE' if zgodne else 'ROZJAZD'}")
    for r_ in rozjazd:
        print(f"    - {r_}")
    print(f"[instalacja] raport: {RAPORT}")
    print("\nNastepny krok: python -m replikacja.stan   (pokaze etap i co dalej)")
    return 0 if zgodne else 1


if __name__ == "__main__":
    sys.exit(main())
