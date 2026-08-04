from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


for language in ("pl", "en"):
    path = ROOT / f"pilot-{language}.html"
    require(path.exists(), f"brak {path.name}")
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8")
    require("https://" not in html and "http://" not in html, f"{path.name}: zewnętrzny URL")
    require("<script" in html and "<style" in html, f"{path.name}: brak osadzonego CSS/JS")
    require(len(re.findall(r'\bid:\s*["\'](?:pl|en)-', html)) == 5, f"{path.name}: nie ma 5 par")
    require("equally_unnatural" in html, f"{path.name}: brak czwartej odpowiedzi")
    for field in ("pair_duration_ms", "total_duration_ms", "context_returns", "display_order", "side_assignment", "screen_width", "events"):
        require(field in html, f"{path.name}: brak pola {field}")
    require("crypto.getRandomValues" in html, f"{path.name}: losowanie nie używa źródła systemowego")
    require("navigator.clipboard" in html, f"{path.name}: brak kopiowania JSON")

refs = ROOT / "referenty-obliczeniowe.md"
require(refs.exists(), "brak referenty-obliczeniowe.md")
if refs.exists():
    text = refs.read_text(encoding="utf-8")
    ids = re.findall(r"^## ((?:en|pl)-\d{2}-[^\s]+)$", text, flags=re.MULTILINE)
    require(len(ids) == 24, f"referenty: oczekiwano 24 sekcji, jest {len(ids)}")
    require(len(set(ids)) == 24, "referenty: powtórzone identyfikatory")
    for label in ("obecna:", "nowa:", "zdanie po zmianie:", "dlaczego nie jest rozmową:"):
        require(text.count(label) == 24, f"referenty: '{label}' występuje {text.count(label)} razy")

report = ROOT / "RAPORT.md"
require(report.exists(), "brak RAPORT.md")

if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PASS: kontrakt czterech wytworów spełniony")
