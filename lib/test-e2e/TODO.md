# TODO - Refactor lib/test-e2e/test_runner.py

Questo TODO nasce dai commenti `##` presenti in `lib/test-e2e/test_runner.py`.
Obiettivo: rifare il runner come wrapper minimale e affidabile per lanciare `lib/test-e2e/stress_test_v2.py`.

## Obiettivo

- Un'unica CLI (niente subcommands) con parametri di default e override.
- Supporto al parallelismo con `-j/--parallel` (accetta anche `1`).
- Output essenziale (niente banner, niente print ridondanti).
- Path robusti dopo lo spostamento dei file (non dipendere dalla cwd dell'utente).

## Checklist operativa

1) Ripulire import

- Rimuovere import non usati.
- Tenere solo gli import necessari (es. `argparse`, `subprocess`, `sys`, `pathlib.Path`, e typing solo se serve davvero).

2) Sistemare init e path dopo lo spostamento

- Verificare che `script_dir = Path(__file__).parent` sia ancora corretto.
- Rendere l'esecuzione indipendente dalla cwd:
  - calcolare una cwd esplicita (es. repo root) e passare `cwd=...` a `subprocess.run/Popen`.
  - usare path assoluti/risolti per `stress_test_v2.py`.

3) Rimuovere API inutili

- Eliminare `run_stress_test()`.
- Far si che la funzione che gestisce l'esecuzione accetti `parallel=1` senza ramo dedicato.

4) Refactor parallel

- In `run_parallel_tests(...)`:
  - evitare `extra_args: list = None` se poi viene trattato come lista; preferire un tipo chiaro e gestire il default in modo pulito.
  - rimuovere la logica su `remaining_tests` se non serve; se si perde 1 test non e' un problema (come da commento).
  - rimuovere i seed per processo (`--seed`): non funzionano / non sono affidabili.
  - evitare print ripetuti o verbose; poche righe e basta.

5) Eliminare funzionalita' fuori scope

- Eliminare funzioni non inerenti allo scopo del runner:
  - `run_replay()`
  - `analyze_log()`
  - `find_errors()`
  - `show_stats()`
  - `clean_logs()`

6) Rifare la CLI (main)

- Ridurre i `print()` (se serve andare a capo, usare `\n` invece di molte chiamate a `print`).
- Rimuovere banner ASCII.
- Rimuovere quick/medium/intensive/overnight/seed/replay/analyze/stats/clean e tutto il sistema di subcommands.
- Niente esempi hardcoded nell'help; spiegare i parametri solo tramite `--help`.
- Esporre solo parametri di configurazione con default (da definire) e passthrough verso `stress_test_v2.py`, ad esempio:
  - `-n/--num-tests`
  - `-j/--parallel`
  - `--fps`
  - `--max-turns`
  - `--event`

7) Output

- Evitare di ripetere continuamente dove stanno i log: e' informazione nota.
- Stampare solo cio' che serve per capire che cosa sta girando e se e' andato a buon fine.

## Linee guida generali (dedotte dalle correzioni)

- Una responsabilita' per file/script: evitare comandi extra "da toolbox" se lo scopo e' solo lanciare stress test.
- Default + override: niente "modalita' speciali" con logiche duplicate.
- Output minimale e stabile: pochi `print`, niente spam.
- Niente codice inutile/duplicato: se una funzione e' duplicata o non chiara, si elimina.
- Path robusti: non assumere la cwd dell'utente; calcolare path base e passare `cwd=` ai subprocess quando opportuno.
- Evitare feature non affidabili (es. seed casuale per processo) se non garantiscono determinismo o non funzionano.
