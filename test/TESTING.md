# Testing Happy Hare - StepperIdlerSelector

Tento dokument popisuje jak spustit unit testy pro StepperIdlerSelector a obecně pro Happy Hare.

## Struktura testů

```
test/
├── __init__.py
├── runner.sh                           # Test runner script
├── TESTING.md                          # Tento dokument
├── components/
│   ├── __init__.py
│   ├── test_mmu_server.py             # Původní testy MMU serveru
│   └── test_stepper_idler_selector.py # NOVÉ testy pro StepperIdlerSelector
└── support/
    ├── toolchange.orig.gcode
    └── no_toolchange.orig.gcode
```

## Spuštění testů

### Všechny testy

```bash
cd ~/Happy-Hare-modified
./test/runner.sh
```

Nebo přímo pomocí Python unittest:

```bash
cd ~/Happy-Hare-modified
python3 -m unittest discover test
```

### Pouze testy pro StepperIdlerSelector

```bash
cd ~/Happy-Hare-modified
python3 -m unittest test.components.test_stepper_idler_selector
```

### Konkrétní test

```bash
cd ~/Happy-Hare-modified
python3 -m unittest test.components.test_stepper_idler_selector.TestStepperIdlerSelector.test_filament_release_moves_to_up_position
```

## Co testy pokrývají

### Unit testy (`test_stepper_idler_selector.py`)

#### Základní funkcionalita
- ✅ **Inicializace** - Správné načtení konfiguračních parametrů
- ✅ **Výpočet pozic** - Kalkulace pozic pro brány T0-T4
- ✅ **Filament drive** - Pohyb idleru na pozici brány
- ✅ **Filament release** - Pohyb idleru do UP pozice (85.0mm)
- ✅ **Homing sekvence** - Homování na endstop a pohyb do UP pozice

#### Stavové změny
- ✅ **Grip state** - Změny stavu mezi DRIVE a RELEASE
- ✅ **Výběr více bran** - Správný pohyb při přepínání mezi branami T0-T4

#### Error handling
- ✅ **Chyby při homování** - Korektní zachycení a propagace MmuError

#### Konfigurace
- ✅ **Různé gate widths** - Podpora různých vzdáleností mezi branami
- ✅ **Validace example config** - Kontrola platnosti ukázkové konfigurace

### Integrační testy
- ✅ **Registrace selector typu** - Ověření že StepperIdlerSelector je v seznamu typů
- ✅ **Konfigurace** - Validace ukázkové konfigurace

## Pokrytí kódu

Testy pokrývají tyto části `StepperIdlerSelector`:

1. **`__init__()`** - Inicializace a načtení konfigurace
2. **`filament_drive()`** - Přitlačení ložiska k bráně
3. **`filament_release()`** - Odjezd do UP pozice
4. **`_home_idler()`** - Homing sekvence
5. **Výpočet pozic** - Kalkulace z gate0_pos a gate_width

## Testovací data

Testy používají stejné hodnoty jako ukázková konfigurace:

```ini
cad_idler_gate0_pos: 5.0         # Pozice první brány (T0)
cad_idler_gate_width: 21.0       # Vzdálenost mezi branami
cad_idler_home_position: 85.0    # UP pozice (žádné ložisko v kontaktu)
idler_move_speed: 200.0          # Rychlost pohybu
idler_homing_speed: 50.0         # Rychlost homování
```

### Očekávané pozice pro jednotlivé brány

| Brána | Pozice | Výpočet |
|-------|--------|---------|
| T0    | 5.0mm  | gate0_pos |
| T1    | 26.0mm | gate0_pos + 1×gate_width |
| T2    | 47.0mm | gate0_pos + 2×gate_width |
| T3    | 68.0mm | gate0_pos + 3×gate_width |
| T4    | 89.0mm | gate0_pos + 4×gate_width |
| UP    | 85.0mm | idler_home_position |

## Interní testy Klipperu

Happy Hare také obsahuje rozsáhlé interní testy přístupné přes gcode příkaz `_MMU_TEST`.

### Dostupné interní testy

Pro seznam všech testů spusť v Klipperu:

```gcode
_MMU_TEST HELP=1
```

### Příklady užitečných testů

#### Test sync stavu
```gcode
_MMU_TEST SYNC_STATE=loop LOOP=1000
```

#### Test pohybů selectoru
```gcode
_MMU_TEST SEL_MOVE=1 MOVE=10 SPEED=200
```

#### Realistický test syncu
```gcode
_MMU_TEST REALISTIC_SYNC_TEST=1 LOOP=10
```

## Přidání nových testů

Pro přidání nových testů:

1. **Vytvoř test soubor**: `test/components/test_*.py`
2. **Implementuj test třídu**:
```python
import unittest

class TestMojeNovyFunkce(unittest.TestCase):
    def test_neco(self):
        self.assertEqual(1 + 1, 2)
```
3. **Spusť testy**: `./test/runner.sh`

## Continuous Integration

Testy by měly být spuštěny před:
- Každým commitem změn v `mmu_selector.py`
- Vytvořením pull requestu
- Release nové verze

## Troubleshooting

### Import chyby

Pokud testy selhávají s import errors:

```bash
# Ujisti se že jsi ve správném adresáři
cd ~/Happy-Hare-modified

# Spusť s Python path
PYTHONPATH=. python3 -m unittest discover test
```

### Mock chyby

Pokud vidíš chyby s mocky, ujisti se že máš nainstalované:

```bash
pip3 install mock
```

## Testování na reálném hardwaru

Pro testování na skutečné tiskárně s MMU:

1. **Zkopíruj konfiguraci**:
```bash
cp config/examples/mmu_stepper_idler_example.cfg ~/printer_data/config/mmu/mmu_parameters.cfg
```

2. **Uprav pro svůj hardware**:
   - Zkalibruj `cad_idler_gate0_pos`
   - Zkalibruj `cad_idler_gate_width`
   - Nastav správný `cad_idler_home_position`

3. **Spusť MMU_CALIBRATE_IDLER**:
```gcode
MMU_CALIBRATE_IDLER
```

4. **Otestuj pohyby**:
```gcode
MMU_SELECT GATE=0
MMU_SELECT GATE=1
# atd.
```

5. **Zkontroluj logy**:
```bash
tail -f ~/printer_data/logs/mmu.log
```

## Reference

- [Happy Hare dokumentace](https://github.com/moggieuk/Happy-Hare)
- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [Klipper testing](https://www.klipper3d.org/Debugging.html)
