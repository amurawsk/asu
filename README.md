# Projekt ASU - pliki
## Użytkowanie
Użycie skryptu:
```bash
python main.py -x <katalog-glowny> [opcje]
```

Wymagane jest podanie katalogu głównego (X), dodatkowo można podać pozostałe katalogi (Y1, Y2, ...).

Wszystkie opcje można uzyskać wpisując
```bash
python main.py --help
```

## Funkcjonalności
Program pozwala na znalezienie i podjęcie odpowiedniej akcji wobec plików:
- pustych
- tymczasowych
- o nietypowych atrybutach
- które w nazwie mają znak mogący powodować problemy
- o tych samych zawartościach
- o tych samych nazwach
- które nie znajdują się w katalogu głównym

## Argumenty wywołania
Każdą z funkcjonalności można aktywować odpowiednim argumentem wywołania (wszystkie argumenty można podejrzeć wywołując `python main.py --help`). 

Dla każdego takiego argumentu możliwe są 3 wartości do wprowadzenia przez użytkownika:
- 'y' - program podejmie odpowiednią akcję dla danego rodzaju pliku,
- 'ask' - program po znalezieniu danego typu pliku zapyta o chęć wykonania podanej akcji
- 'no' - program nie będzie szukać danego typu pliku (opcja domyślna - dla niezdefiniowanych przez użytkownika opcji)



## Konfiguracja
Domyślny plik konfiguracyjny zawiera następującą zawartość:
```
[DEFAULT]
default_access = 755
tricky_letters = :, ", ;, *, ?, $, #, ', |, \
substitute = _
tmp = ~, .tmp
```

Program pozwala na wprowadzenie własnego pliku konfiguracyjnego (poprzez opcję `--config-file`). Musi być on jednak w odpowiednim formacie, analogicznie do domyślnego pliku. 


## Przykłady wywołań
### Wywołanie programu tylko dla pustych plików:
```bash
python main.py -x ./X -e ask
```
analogicznie:
```bash
python main.py -x ./X --empty ask
```

### Wywołanie programu dla plików tymczasowych i duplikatów
```bash
python main.py -x ./X -t ask -c ask
```

### Wywołanie programu ze zmienionym plikiem konfiguracyjnym
```bash
python main.py -x ./X --config-file path_to_custom_config -e ask
```

### Wywołanie programu dla wielu katalogów (poza katalogiem głównym)
```bash
python main.py -x ./X -d ./Y1 ./Y2 -e ask
```

### Wywołanie programu z automatyczną akcją dla plików z problematycznymi nazwami
```bash
python main.py -x ./X -p y
```
