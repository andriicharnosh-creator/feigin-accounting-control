# Feigin Accounting Control

Pierwszy lokalny szkielet kontroli księgowej dla:

- **Feigin Electric Andrii Charnosh - JDG Polska**;
- **Feigin Electric Co Ltd - Tajlandia**;
- okresu od stycznia 2026.

## Uruchomienie lokalne

Wymagany jest Python 3.11+; projekt używa wyłącznie biblioteki standardowej.

```bash
python3 app.py
```

Otwórz `http://127.0.0.1:8000`. Port można zmienić z poziomu krótkiego skryptu Python, jeśli jest zajęty.

Testy:

```bash
python3 -m unittest discover -s tests -v
```

## Zakres i ograniczenia

- Rejestr obejmuje syntetyczne wpisy dokumentów, należności, zobowiązań, płatności i brakujących materiałów.
- Każdy wpis ma podmiot, walutę, źródło i status weryfikacji.
- Podsumowania nie łączą walut. Do wspólnego przeliczenia potrzebne są jawny kurs FX i data kursu.
- Wpisy mające status `requires_accountant_decision` wymagają ustalenia z księgowym.
- Wszystkie rekordy w `data/synthetic_records.json` są oznaczone jako syntetyczne i nie są rzeczywistymi dokumentami.
- Nie ma połączeń produkcyjnych, wysyłki, płatności ani składania deklaracji. Fakturownia jest wyłącznie zaplanowanym źródłem dla JDG.

## Przed podłączeniem rzeczywistych danych

Trzeba uzgodnić z księgowym zasady podatkowe obu podmiotów, okresy i statusy dokumentów, źródła dowodowe, kursy walut z datami oraz politykę rozliczania płatności. Następnie można zaprojektować bezpieczne mapowanie Fakturownia -> JDG, uwierzytelnianie i synchronizację tylko po akceptacji.