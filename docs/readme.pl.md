<p align="center">
  <img src="screenshot.png" alt="Snake CLI uruchomiony w oknie terminala" width="840">
</p>

<h1 align="center">Snake Cli v 1.5py</h1>

<p align="center">
  Klasyczny Snake w terminalu — czysty Python, zero zależności, pięć poziomów i zapisywany rekord.
</p>

<p align="center">
  <a href="../README.md">English</a> •
  <a href="README.pl.md"><b>Polski</b></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="Platforma" src="https://img.shields.io/badge/Platforma-Windows%20%7C%20Linux%20%7C%20macOS-5C2D91?style=flat-square&logo=windows-terminal&logoColor=white">
  <img alt="Zależności" src="https://img.shields.io/badge/Zale%C5%BCno%C5%9Bci-brak-0078D4?style=flat-square">
  <img alt="Licencja" src="https://img.shields.io/badge/Licencja-MIT-107C10?style=flat-square">
</p>

---

## Przegląd

**Snake Cli v 1.5py** to lekka, terminalowa wersja klasyka z salonów gier. Prowadzisz węża po ograniczonej planszy,
zbierasz jagody, aby rosnąć, omijasz przeszkody i własny ogon, a także ścigasz rekord zapisywany między sesjami.

Gra jest napisana w czystym Pythonie na bazie standardowej biblioteki `curses`, więc cały projekt to kilka
małych, czytelnych modułów — łatwych do przeczytania i zmiany, bez `pip install` na Pythonie, który ma `_curses`.

## Funkcje

| | Funkcja | Opis |
|---|---|---|
| 🎮 | **Klasyczna rozgrywka** | Strzałki lub WASD, brak skrętu o 180°, kolizja ze ścianą, przeszkodą i własnym ciałem kończy grę. |
| 🧱 | **Pięć ręcznie zaprojektowanych poziomów** | Plain, Midwall, Pillars, Fortress i Maze — każdy z własnym układem przeszkód i prędkością. |
| ⏩ | **Rosnąca trudność** | Każdy poziom jest szybszy od poprzedniego; po piątym poziomie układ się powtarza, a tempo dalej rośnie. |
| 🏆 | **Zapisywany rekord** | Najlepszy wynik jest przechowywany w `snake_game/highscore.txt` i pokazywany w menu oraz na ekranie końca gry. |
| ◉ | **Okrągła, kolorowa grafika** | Wąż, jagoda i ściany są rysowane okrągłymi znakami z pasami kolorów. |
| 🔤 | **Awaryjny tryb tekstowy** | Terminale bez kolorów lub Unicode automatycznie dostają czytelne renderowanie ASCII. |
| 🧩 | **Mały, modułowy kod** | Poziomy, wyniki i konfiguracja mieszkają we własnych pakietach w katalogu `snake_game/`. |

## Wymagania

- **Python 3.8 lub nowszy.**
- Standardowy moduł `curses`.
  - **Linux / macOS** — dostępny w CPython od razu.
  - **Windows** — część oficjalnych instalatorów nie zawiera rozszerzenia `_curses` (widoczne na Pythonie 3.13 i 3.15).
    Użyj Pythona, który je ma (np. `py -3.14`), albo doinstaluj pakiet:
    ```powershell
    pip install windows-curses
    ```
- Terminal o rozmiarze co najmniej **20 × 50** znaków (większy jest lepszy — plansza skaluje się do okna).

## Szybki start

```powershell
# Sklonuj repozytorium
git clone https://github.com/polsoft-its/Snake_Cli_The_Game.git
cd Snake_Cli_The_Game

# Uruchom grę (na Windows wybierz Pythona z curses)
py -3.14 Snake.py
# lub
python Snake.py
```

Na Linuksie i macOS wystarczy:

```bash
python3 Snake.py
```

> [!TIP]
> W Windows najlepiej wygląda w **Windows Terminal**. Jeśli zamiast `◉ ◎ ◍` widzisz `?`, konsola nie jest w UTF-8 —
> uruchom komendę `chcp 65001` przed startem gry (albo graj dalej w trybie ASCII, który jest w pełni funkcjonalny).

## Sterowanie

| Klawisz | Akcja |
|---|---|
| <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> | Ruch węża |
| <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd> | Ruch węża (alternatywnie) |
| <kbd>Enter</kbd> / <kbd>S</kbd> | Start gry z menu głównego |
| <kbd>I</kbd> | Instrukcja |
| <kbd>Q</kbd> / <kbd>Esc</kbd> | Wyjście |
| <kbd>R</kbd> | Restart po końcu gry |
| <kbd>Q</kbd> | Wyjście z ekranu końca gry |

## Rozgrywka

- Wąż startuje w lewej połowie planszy i porusza się w prawo.
- Zjedzenie jagody daje **+1 punkt** i wydłuża węża o jeden segment.
- Osiągnięcie progu punktowego przenosi na kolejny poziom; plansza zachowuje rozmiar, a wąż długość.
- Gra kończy się, gdy głowa uderzy w zewnętrzną ramkę, przeszkodę lub własne ciało.

### Poziomy

| Poziom | Nazwa | Prędkość | Próg punktowy | Przeszkody |
|:---:|---|---:|---:|---|
| 1 | Plain | 150 ms/klatkę | 10 | brak |
| 2 | Midwall | 130 ms/klatkę | 20 | brak |
| 3 | Pillars | 110 ms/klatkę | 30 | poziomy mur |
| 4 | Fortress | 95 ms/klatkę | 40 | pusty kwadrat |
| 5 | Maze | 80 ms/klatkę | 50 | rozrzucone kolumny |
| 6+ | Ostatni układ, szybciej | −5 ms na poziom (min. 40 ms) | +10 na poziom | jak na poziomie 5 |

## Struktura projektu

```text
Snake_Cli_The_Game/
├── Snake.py                     # Punkt wejścia: UI curses, pętla gry, rysowanie
├── snake_game/
│   ├── config.py                # Ścieżki projektu i lokalizacja pliku z rekordem
│   ├── highscore.txt            # Tworzony/aktualizowany automatycznie
│   ├── levels/
│   │   └── catalog.py           # Definicje poziomów (prędkość, próg, przeszkody)
│   └── storage/
│       └── scores.py            # Odczyt i zapis rekordu
├── docs/
│   ├── screenshot.png           # Zrzut ekranu użyty w README
│   ├── README.pl.md             # Ten dokument (wersja polska)
│   └── ReadMeP.txt              # Opis skrócony w 350 znakach
└── README.md                    # Wersja angielska
```

### Jak to działa razem

- **`Snake.py`** obsługuje okno `curses`, menu główne, pętlę gry oraz funkcje rysujące
  (`draw_snake`, `draw_food`, `draw_wall`, `initialize_colors`).
- **`snake_game/levels/catalog.py`** to same dane plus `get_level(number)`, które zapętla listę poziomów
  i przyspiesza kolejne poziomy.
- **`snake_game/storage/scores.py`** czyta i zapisuje jedną liczbę z `snake_game/highscore.txt`;
  błędy są obsługiwane po cichu, więc gra nigdy nie wywala się przez problem z plikiem.
- **`snake_game/config.py`** buduje ścieżki bezwzględne od położenia pakietu, dzięki czemu plik rekordu zawsze
  znajduje się w `snake_game/`, niezależnie od katalogu roboczego.

## Konfiguracja

Większość zmian to jedna linijka:

| Co | Gdzie |
|---|---|
| Prędkość poziomu, próg punktowy, przeszkody | `snake_game/levels/catalog.py` — wpisy `Level(...)` |
| Lokalizacja pliku rekordu | `snake_game/config.py` — `HIGH_SCORE_FILE` |
| Kolory węża, jedzenia i ścian | `Snake.py` — `initialize_colors()` |
| Znaki węża, jedzenia i ścian | `Snake.py` — `HEAD_*`, `BODY_GLYPHS`, `TAIL_GLYPHS`, `FOOD_GLYPHS`, `WALL_GLYPHS` |

## Rozwiązywanie problemów

<details>
<summary><b>„The 'curses' module is not available in this Python installation”</b></summary>

Twoja instalacja Pythona nie ma rozszerzenia `_curses`. Uruchom grę Pythonem, który je zawiera
(np. `py -3.14 Snake.py`) lub zainstaluj `windows-curses`:

```powershell
pip install windows-curses
```
</details>

<details>
<summary><b>Widzę tylko <code>?</code> albo litery ASCII zamiast okrągłych znaków</b></summary>

Konsola nie używa strony kodowej UTF-8 lub nie obsługuje kolorów, więc gra celowo przełącza się na
tryb ASCII. Uruchom `chcp 65001` (Windows) lub użyj terminala UTF-8, np. Windows Terminal.
</details>

<details>
<summary><b>Plansza jest ciasna lub się nie mieści</b></summary>

Plansza wypełnia bieżące okno terminala. Powiększ okno przed startem lub użyj czcionki o mniejszej
wysokości wiersza. Minimum to 20 × 50 znaków.
</details>

<details>
<summary><b>Rekord się nie zmienił</b></summary>

Wynik jest zapisywany tylko wtedy, gdy pobije zapisany, i trafia do `snake_game/highscore.txt`.
Jeśli katalog jest tylko do odczytu, zapis celowo kończy się po cichu.
</details>

## Współtworzenie

1. Zrób fork repozytorium i utwórz gałąź funkcji (`git checkout -b feature/moj-pomysl`).
2. Utrzymuj zmiany małe i skupione; trzymaj się istniejącego układu modułów.
3. Testuj, uruchamiając grę w terminalu z kolorem i UTF-8 oraz bez nich.
4. Otwórz pull request z opisem, co i dlaczego zmieniłeś.

Pomysły pasujące do projektu: nowe układy poziomów, więcej typów przedmiotów, pauza czy legenda
znaków na ekranie.

## Licencja

Wydane na licencji **MIT** — szczegóły w repozytorium.

---

<p align="center">
  <sub><b>Snake Cli v 1.5py</b> — zbudowane w Pythonie i curses · <a href="../README.md">English</a> · <a href="#snake-cli">Na górę</a></sub>
</p>
