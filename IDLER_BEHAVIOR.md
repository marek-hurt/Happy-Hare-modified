# Idler Behavior - StepperIdlerSelector

## Rotační Idler s Ložisky (Prusa MMU2S Style)

StepperIdlerSelector je navržen pro **rotační idler** s ložisky, kde:
- Idler je **otočný válec** s ložisky rozmístěnými po obvodu
- Každé ložisko odpovídá jedné bráně (gate)
- Idler se **natáčí** na správnou pozici, aby ložisko přitlačilo převodové kolečko

## Princip Fungování

```
┌─────────────────────────────────────────────────────────────┐
│                  Rotační Idler (válec)                      │
│                                                             │
│     Ložisko 0 ──┐                                           │
│                 │    Ložisko 1 ──┐                          │
│                 │                │                          │
│                 ▼                ▼                          │
│              ●  ●  ●  ●  ●                                  │
│            T0  T1  T2  T3  T4  (pozice)                    │
│                                                             │
│  UP pozice: ● (mimo kontakt s jakoukoliv bránou)           │
└─────────────────────────────────────────────────────────────┘
```

## Stavy Idleru

### 1. **DRIVE State** - Ložisko přitlačuje převod
Kdy: Při pohybu materiálu skrz MMU
Idler pozice: Podle aktivní brány (T0-T4)

```python
# Selector na T0 → Idler taky na T0
T0: idler_offset[0] = 5.0 mm
T1: idler_offset[1] = 25.0 mm
T2: idler_offset[2] = 46.0 mm
...
```

### 2. **RELEASE State** - Ložisko mimo kontakt
Kdy: Při posunu materiálu do extruderu
Idler pozice: `cad_idler_home_position` (např. 85.0 mm)

```python
# Materiál v extruderu → Idler v UP pozici
UP position: 85.0 mm (žádné ložisko v kontaktu)
```

## Sekvence Pohybů

### Výběr Brány (Gate Selection)
```
1. filament_release()
   └─> Idler → UP pozice (85.0 mm)

2. selector → přejede na gate T1

3. idler → přejede na gate T1 (25.0 mm)
```

### Load Filament
```
1. filament_drive()
   └─> Idler → pozice gate (např. 25.0 mm pro T1)
   └─> Ložisko přitlačí převodové kolečko

2. Gear motor → pohání filament skrz bránu

3. Filament do extruderu

4. filament_release()
   └─> Idler → UP pozice (85.0 mm)
   └─> Žádné ložisko v kontaktu
   └─> Extruder může volně pohánět filament
```

### Unload Filament
```
1. Extruder → vytáhne filament zpět

2. filament_drive()
   └─> Idler → pozice gate (např. 25.0 mm pro T1)

3. Gear motor → vytáhne filament z brány

4. filament_release()
   └─> Idler → UP pozice (85.0 mm)
```

## Implementace v Kódu

### Konfigurace Pozic

```ini
# V mmu_parameters.cfg nebo mmu.cfg

# Pozice pro každou bránu (T0-T4)
cad_idler_gate0_pos: 5.0        # První brána
cad_idler_gate_width: 21.0      # Vzdálenost mezi bránami

# UP pozice (mimo kontakt)
cad_idler_home_position: 85.0   # Žádné ložisko v kontaktu
```

### Výpočet Pozic
```python
# Automaticky vypočítáno při MMU_CALIBRATE_IDLER
idler_offsets = [
    cad_idler_gate0_pos + 0 * cad_idler_gate_width,  # 5.0
    cad_idler_gate0_pos + 1 * cad_idler_gate_width,  # 25.0
    cad_idler_gate0_pos + 2 * cad_idler_gate_width,  # 46.0
    cad_idler_gate0_pos + 3 * cad_idler_gate_width,  # 67.0
    cad_idler_gate0_pos + 4 * cad_idler_gate_width,  # 88.0
]
```

### Metody v StepperIdlerSelector

```python
def filament_drive(self):
    """Přitlačit ložisko k převodu"""
    if self.mmu.gate_selected >= 0:
        # Jet na pozici brány
        self._move_idler_to_gate(self.mmu.gate_selected)
        self.grip_state = self.mmu.FILAMENT_DRIVE_STATE

def filament_release(self, measure=False):
    """Odjet do UP pozice (mimo kontakt)"""
    # Jet na UP pozici
    self.idler_stepper.do_move(
        movepos=self.cad_idler_home_position,  # 85.0 mm
        speed=self.idler_move_speed,
        accel=self.idler_stepper.accel,
        sync=True
    )
    self.grip_state = self.mmu.FILAMENT_RELEASE_STATE
    return 0.
```

## Příklad z 3D-Druckerplausch-Klipper

### Původní Konfigurace
```python
[gcode_macro _VAR_MMU2S]
variable_idler = [5, 20, 35, 50, 65]       # Pozice T0-T4
variable_idler_home_position: 85            # UP pozice
```

### Převod na Happy-Hare StepperIdlerSelector
```ini
# mmu_parameters.cfg
cad_idler_gate0_pos: 5.0        # idler[0]
cad_idler_gate_width: 15.0      # idler[1] - idler[0] = 20 - 5
cad_idler_home_position: 85.0   # idler_home_position
```

## Homing Sekvence

```
1. Home selector → nulová pozice

2. Home idler:
   a) Jet na endstop (sensorless nebo physical)
   b) Set position = 2.0 mm (reference point)
   c) Jet na UP pozici (85.0 mm)

3. MMU je ready:
   - Selector: home pozice
   - Idler: UP pozice (mimo kontakt)
```

## Debugging

### Zkontrolovat Pozice
```gcode
# V konzoli Klipperu
GET_POSITION

# Nebo v mmu_vars.cfg
mmu_idler_offsets = [5.0, 20.0, 35.0, 50.0, 65.0]
```

### Test Pohybů
```gcode
# Test jednotlivých bran
MMU_SELECT_TOOL TOOL=0  # Idler → 5.0 mm
MMU_SELECT_TOOL TOOL=1  # Idler → 20.0 mm
...

# Test release (UP pozice)
# (voláno automaticky při load do extruderu)
```

### Kontrola UP Pozice
```python
# V mmu.log by mělo být:
"Releasing idler to UP position at 85.0mm"
"Moving idler to UP position at 85.0mm"
```

## Důležité Poznámky

⚠️ **UP pozice MUSÍ být mimo kontakt:**
- Pokud je ložisko stále v kontaktu, vytvoří odpor pro extruder
- Výsledek: špatné tisky, clogging, grinding

⚠️ **Pozice musí být přesné:**
- Pokud ložisko není správně přitlačeno, gear motor nepohne materiál
- Výsledek: load failed, unload failed

⚠️ **Kalibrace je klíčová:**
```bash
# 1. Nastav správné hodnoty CAD parametrů
# 2. Spusť kalibraci
MMU_CALIBRATE_IDLER
# 3. Ověř v mmu_vars.cfg
# 4. Test
MMU_SOAKTEST_SELECTOR LOOP=10
```

## Srovnání: Servo vs Stepper Idler

| Vlastnost | Servo Idler | Stepper Idler |
|-----------|-------------|---------------|
| Pozice gate | Úhel (např. 45°) | Lineární (mm) |
| UP pozice | Úhel (např. 180°) | Lineární (85.0 mm) |
| Přesnost | Závislá na servu | Vysoká (stepper) |
| Opakování | Může se lišit | Konzistentní |
| Kalibrace | Úhly | Pozice v mm |

---

**Autor:** marek-hurt
**Datum:** 2026-01-19
**Verze:** 1.0
